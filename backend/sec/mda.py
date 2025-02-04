import re
from edgar import set_identity, Company

def clean_number(value_str):
    """Remove commas and convert to float (numbers are assumed to be in millions)."""
    if not value_str:
        return None
    try:
        return float(value_str.replace(",", ""))
    except (ValueError, AttributeError):
        return None

def extract_segment_revenue_nvda(ticker):
    """
    For NVDA we anchor on Note 14 (Segment Information) and combine several subsequent chunks
    to capture a full context. Then we split by lines and try to extract the revenue numbers
    for each segment.
    """
    # Set your identity (required for EDGAR scraping)
    set_identity("Your Name your_email@example.com")
    company = Company(ticker)
    filings = company.get_filings(form="10-Q")
    filing = filings.latest()
    tenq = filing.obj()
    
    doc = tenq.doc
    chunks = doc.chunks
    print(f"\nProcessing {ticker} - Found {len(chunks)} chunks")
    
    # Find the chunk that includes "segment information" and combine it with several subsequent chunks
    segment_context = ""
    for i, chunk in enumerate(chunks):
        chunk_text = str(chunk)
        if "segment information" in chunk_text.lower():
            # Increase the context window to 10 chunks to try to capture the revenue table
            context_chunks = chunks[i: min(i + 10, len(chunks))]
            segment_context = "\n".join([str(c) for c in context_chunks])
            print("\nFound segment information context:")
            print(segment_context[:500] + "...\n")
            break

    if not segment_context:
        print("No segment information context found.")
        return {
            "ticker": ticker,
            "segments": {},
            "currency": "USD Millions"
        }
    
    # Define the segments of interest and their possible name variations
    segment_mappings = {
        'Data Center': ['data center', 'datacenter', 'cloud'],
        'Gaming': ['gaming', 'games'],
        'Automotive': ['automotive', 'auto', 'automobile'],
        'Professional Visualization': ['professional visualization', 'pro viz', 'quadro'],
        'Client Computing': ['client computing', 'client', 'pc'],
        'Enterprise': ['enterprise', 'data center solutions'],
        'Networking': ['networking', 'network'],
        'Embedded': ['embedded', 'iot'],
        'Software': ['software', 'saas']
    }
    
    segments = {}
    
    # Process the context line by line
    for line in segment_context.splitlines():
        line_lower = line.lower()
        for seg_name, variations in segment_mappings.items():
            # If we have already extracted a value for this segment, skip it.
            if seg_name in segments:
                continue
            for variation in variations:
                if variation.lower() in line_lower:
                    # Look for a revenue number on the line.
                    # This regex looks for an optional '$' then a number with commas (and optional decimals)
                    match = re.search(r'\$?\s*([\d,]+(?:\.\d+)?)', line)
                    if match:
                        value = clean_number(match.group(1))
                        if value is not None:
                            segments[seg_name] = value
                            # Once a match is found for this segment, break out of the variation loop.
                            break

    # Optionally, try to extract total revenue from the entire context
    total_match = re.search(
        r"total\s+revenue.*?\$?\s*([\d,]+(?:\.\d+)?)", 
        segment_context, 
        re.IGNORECASE | re.DOTALL
    )
    if total_match:
        segments["Total Revenue"] = clean_number(total_match.group(1))
    
    result = {
        "ticker": ticker,
        "segments": segments,
        "currency": "USD Millions"
    }
    return result

if __name__ == "__main__":
    tickers = ["NVDA"]
    
    for ticker in tickers:
        try:
            print("=" * 50)
            result = extract_segment_revenue_nvda(ticker)
            print(f"\nSegment Revenue Results for {result['ticker']}:")
            if not result['segments']:
                print("No segment data found")
            else:
                for segment, value in result['segments'].items():
                    print(f"{segment}: ${value:,.0f}M")
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
