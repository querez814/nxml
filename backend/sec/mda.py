
import re
from edgar import set_identity, Company

def clean_number(value_str):
    """Clean and convert string numbers to float, handling None values."""
    if not value_str:
        return None
    try:
        return float(value_str.replace(",", ""))
    except (ValueError, AttributeError):
        return None

def extract_segment_revenue(ticker):
    """
    Extract segment revenue data from a company's latest 10-Q filing.
    Handles different reporting formats and styles.
    """
    set_identity("Your Name your_email@example.com")
    company = Company(ticker)
    filings = company.get_filings(form="10-Q")
    filing = filings.latest()
    tenq = filing.obj()
    
    doc = tenq.doc
    chunks = doc.chunks
    
    # Print chunk count for debugging
    print(f"\nProcessing {ticker} - Found {len(chunks)} chunks")
    
    # Collect all relevant sections that might contain segment information
    relevant_text = ""
    
    # First pass: find the MD&A and Results sections
    for i, chunk in enumerate(chunks):
        chunk_text = str(chunk).strip()
        
        # Look for MD&A section
        if any(marker in chunk_text.lower() for marker in [
            "management's discussion",
            "results of operations",
            "segment information",
            "revenue by segment",
            "quarterly summary",
            "operating segments"
        ]):
            # Get this chunk and several following chunks
            context = []
            for j in range(i, min(i + 10, len(chunks))):
                context.append(str(chunks[j]))
            context_text = "\n".join(context)
            print(f"\nFound relevant section in chunk {i}:")
            print(context_text[:200] + "...")  # Print preview
            relevant_text += context_text + "\n"
    
    segments = {}
    
    # Different ways companies might report numbers
    number_patterns = [
        r'\$?([\d,]+\.?\d*)\s*billion',
        r'\$?([\d,]+\.?\d*)\s*million',
        r'\$?([\d,]+(?:\.?\d*)?)'
    ]
    
    # Common segment names and their variations
    segment_mappings = {
        'data center': ['data center', 'datacenter', 'cloud'],
        'gaming': ['gaming', 'games'],
        'automotive': ['automotive', 'auto', 'automobile'],
        'professional visualization': ['professional visualization', 'pro viz', 'quadro'],
        'client computing': ['client computing', 'client', 'pc'],
        'enterprise': ['enterprise', 'data center solutions'],
        'networking': ['networking', 'network'],
        'mobile': ['mobile', 'mobility'],
        'embedded': ['embedded', 'iot'],
        'software': ['software', 'saas']
    }
    
    # Search for segment revenues
    for base_segment, variations in segment_mappings.items():
        for segment_name in variations:
            for pattern in number_patterns:
                # Look for various revenue reporting formats
                search_patterns = [
                    f"{segment_name}.*?revenue.*?{pattern}",
                    f"{segment_name}.*?sales.*?{pattern}",
                    f"revenue.*?{segment_name}.*?{pattern}",
                    f"sales.*?{segment_name}.*?{pattern}"
                ]
                
                for search_pattern in search_patterns:
                    match = re.search(search_pattern, relevant_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        value = clean_number(match.group(1))
                        if value is not None:
                            # Convert billions to millions
                            if 'billion' in match.group(0).lower():
                                value *= 1000
                            segments[base_segment.title()] = value
                            break
    
    # Look for total revenue
    for pattern in number_patterns:
        total_patterns = [
            f"total.*?revenue.*?{pattern}",
            f"revenue.*?was.*?{pattern}",
            f"net revenue.*?{pattern}"
        ]
        
        for total_pattern in total_patterns:
            match = re.search(total_pattern, relevant_text, re.IGNORECASE)
            if match:
                value = clean_number(match.group(1))
                if value is not None:
                    if 'billion' in match.group(0).lower():
                        value *= 1000
                    segments['Total Revenue'] = value
                    break
    
    # Look for percentage changes
    growth_pattern = r"(?P<segment>[\w\s]+?)\s+revenue\s+(?:was\s+)?(?P<direction>up|down)\s+(?P<value>[\d.]+)%"
    for match in re.finditer(growth_pattern, relevant_text, re.IGNORECASE):
        segment = match.group("segment").strip().title()
        value = clean_number(match.group("value"))
        if value is not None:
            value = value if match.group("direction").lower() == "up" else -value
            segments[f"{segment} Growth YoY"] = value
    
    # Try to extract the period
    period_match = re.search(r"quarter(?:\s+ended)?\s+(\w+\s+\d{1,2},?\s+\d{4})", relevant_text)
    period = period_match.group(1) if period_match else None
    
    # Add metadata
    result = {
        "ticker": ticker,
        "segments": segments,
        "period": period,
        "currency": "USD Millions"
    }
    
    return result

if __name__ == "__main__":
    # Test with multiple tickers
    tickers = ["NVDA", "INTC", "AMD", "QCOM", "TXN"]
    
    for ticker in tickers:
        try:
            print(f"\n{'='*50}")
            result = extract_segment_revenue(ticker)
            print(f"\nSegment Revenue Results for {result['ticker']} - {result['period']}:")
            if not result['segments']:
                print("No segment data found")
            else:
                for segment, value in result['segments'].items():
                    if "Growth" in segment:
                        print(f"{segment}: {value:,.1f}%")
                    else:
                        print(f"{segment}: ${value:,.0f}M")
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")