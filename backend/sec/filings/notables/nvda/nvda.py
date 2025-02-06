import re
from lxml import etree

# Define the file path to the SEC filing
file_path = r"backend\sec\filings\notables\nvda\sec-edgar-filings\NVDA\10-Q\0001045810-24-000316\full-submission.txt"

def preprocess_file(file_path):
    """
    Extracts only the XBRL portion from the SEC filing and fixes XML issues.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Locate the first valid XML declaration or <XBRL> tag
    xbrl_start = content.find("<?xml")
    if xbrl_start == -1:
        xbrl_start = content.find("<XBRL>")  # Fallback if XML declaration is missing
    
    xbrl_end = content.find("</XBRL>") + len("</XBRL>")
    
    if xbrl_start == -1 or xbrl_end == -1:
        raise ValueError("XBRL section not found in the SEC filing.")

    # Extract clean XBRL content
    xbrl_content = content[xbrl_start:xbrl_end].strip()

    # Fix common XML issues
    xbrl_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xbrl_content)  # Fix unescaped "&"

    # Save the cleaned XBRL content to a new file
    temp_file = "temp-xbrl.xml"
    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(xbrl_content)

    return temp_file

def extract_segmented_revenues(file_path):
    """
    Extract segmented revenues from the XBRL content in an SEC filing.
    """
    # Preprocess the file to extract the XBRL section
    preprocessed_file = preprocess_file(file_path)

    # Parse the XBRL XML file
    tree = etree.parse(preprocessed_file)
    root = tree.getroot()

    # Define namespaces from SEC XBRL filing
    namespaces = {
        'xbrli': 'http://www.xbrl.org/2003/instance',
        'xbrldi': 'http://xbrl.org/2006/xbrldi',
        'us-gaap': 'http://fasb.org/us-gaap/2024',  # Update year if necessary
        'dei': 'http://xbrl.sec.gov/dei/2024',
        'link': 'http://www.xbrl.org/2003/linkbase',
        'iso4217': 'http://www.xbrl.org/2003/iso4217',
        'ix': 'http://www.xbrl.org/2013/inlineXBRL',
        'srt': 'http://fasb.org/srt/2024',
        'xlink': 'http://www.xbrl.org/2003/xlink',
        'nvda': 'http://www.nvidia.com/20241027',
        'country': 'http://xbrl.sec.gov/country/2024',
    }

    segmented_revenues = []

    # Locate all context elements defining segments
    for context in root.findall('.//xbrli:context', namespaces):
        explicit_member = context.find('.//xbrldi:explicitMember', namespaces)
        if explicit_member is not None:
            dimension = explicit_member.attrib.get('dimension')
            member = explicit_member.text

            # Extract context ID and reporting periods
            context_id = context.attrib.get('id')
            start_date = context.find('.//xbrli:startDate', namespaces)
            end_date = context.find('.//xbrli:endDate', namespaces)
            instant = context.find('.//xbrli:instant', namespaces)

            # Locate associated revenue values
            revenue = root.find(f".//us-gaap:Revenues[@contextRef='{context_id}']", namespaces)
            if revenue is not None:
                segmented_revenues.append({
                    'context_id': context_id,
                    'dimension': dimension,
                    'member': member,
                    'start_date': start_date.text if start_date is not None else None,
                    'end_date': end_date.text if end_date is not None else None,
                    'instant': instant.text if instant is not None else None,
                    'revenue': revenue.text
                })

    return segmented_revenues

# Run the extraction
try:
    results = extract_segmented_revenues(file_path)

    # Print the extracted segmented revenue data
    for item in results:
        print(f"Context ID: {item['context_id']}")
        print(f"Dimension: {item['dimension']}")
        print(f"Member: {item['member']}")
        print(f"Start Date: {item['start_date']}")
        print(f"End Date: {item['end_date']}")
        print(f"Instant: {item['instant']}")
        print(f"Revenue: {item['revenue']}")
        print("-" * 40)
except etree.XMLSyntaxError as e:
    print(f"XML parsing error: {e}")
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
