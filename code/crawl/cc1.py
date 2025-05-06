# python -m pip install warcio

import requests
import json

# For parsing URLs:
from urllib.parse import quote_plus

# For parsing WARC records:
from warcio.archiveiterator import ArchiveIterator

# The URL of the Common Crawl Index server
SERVER = 'http://index.commoncrawl.org/'

# The Common Crawl index you want to query
INDEX_NAME = 'CC-MAIN-2024-33'      # Replace with the latest index name
INDEX_NAME = 'CC-MAIN-2018-09'      # Replace with the latest index name
#{"urlkey": "com,zitbg)/", "timestamp": "20180223121849", "url": "http://zitbg.com/", "mime": "text/html", "mime-detected": "text/html", "status": "200", "digest": "UMFJXSHD6QOXPP6SGCFEG6TO6RSHPNTF", "length": "12089", "offset": "600534804", "filename": "crawl-data/CC-MAIN-2018-09/segments/1518891814700.55/warc/CC-MAIN-20180223115053-20180223135053-00227.warc.gz"}
# The URL you want to look up in the Common Crawl index
target_url = 'commoncrawl.org/faq'  # Replace with your target URL
target_url = "www.zitbg.com"

# It’s advisable to use a descriptive User-Agent string when developing your own applications.
# This practice aligns with the conventions outlined in RFC 7231. Let's use this simple one:
myagent = 'cc-get-started/1.0' #@mail.bg'(Example data retrieval script; yourname@example.com)' #cc-get-started/1.0

# Function to search the Common Crawl Index
def search_cc_index(url):
    encoded_url = quote_plus(url)
    index_url = f'{SERVER}{INDEX_NAME}-index?url={encoded_url}&output=json'
    response = requests.get(index_url, headers={'user-agent': myagent})
    print("Response from server:\r\n", response.text)
    if response.status_code == 200:
        records = response.text.strip().split('\n')
        return [json.loads(record) for record in records]
    else:
        return None

# Function to fetch content from Common Crawl
def fetch_page_from_cc(records):
    for record in records:
        offset, length = int(record['offset']), int(record['length'])
        s3_url = f'https://data.commoncrawl.org/{record["filename"]}'

        # Define the byte range for the request
        byte_range = f'bytes={offset}-{offset+length-1}'

        # Send the HTTP GET request to the S3 URL with the specified byte range
        response = requests.get(
            s3_url,
            headers={'user-agent': myagent, 'Range': byte_range},
            stream=True
        )

        if response.status_code == 206:
            # Use `stream=True` in the call to `requests.get()` to get a raw
            # byte stream, because it's gzip compressed data

            # Create an `ArchiveIterator` object directly from `response.raw`
            # which handles the gzipped WARC content

            stream = ArchiveIterator(response.raw)
            for warc_record in stream:
                if warc_record.rec_type == 'response':
                    return warc_record.content_stream().read()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None

    print("No valid WARC record found in the given records")
    return None

# Search the index for the target URL
records = search_cc_index(target_url)
if records:
    print(f"Found {len(records)} records for {target_url}")

    # Fetch the page content from the first record
    content = fetch_page_from_cc(records)
    if content:
        print(f"Successfully fetched content for {target_url}")
        # You can now process the 'content' variable as needed
        # using something like Beautiful Soup, etc
        
        print(content)
        f = open("1.html", "wb")
        f.write(content)
        f.close()
        print(type(content))
else:
    print(f"No records found for {target_url}")
