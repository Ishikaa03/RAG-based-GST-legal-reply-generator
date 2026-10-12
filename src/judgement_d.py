'''import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_kanoon_pdfs(search_query, max_pages=1, download_folder="kanoon_judgments"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # ---------------------------------------------------------
    # IMPORTANT: Indian Kanoon requires an active login session 
    # to download PDFs. You must extract your session cookie 
    # from your browser and paste it here.
    # ---------------------------------------------------------
    cookies = {
        # Replace this string with the actual cookie from your browser after logging in
        'session_id': '4icvw5owxdkljs6khz3covpalo0679au' 
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://indiankanoon.org/"
    }

    # Use a Session to persist the cookies and headers across all requests
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)

    base_url = "https://indiankanoon.org"
    
    for page in range(max_pages):
        print(f"\n--- Scraping Page {page + 1} ---")
        # Indian Kanoon uses 'pagenum' for pagination (starts at 0)
        search_url = f"{base_url}/search/?formInput={search_query}&pagenum={page}"
        
        try:
            response = session.get(search_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch search results: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all document links on the search results page
        doc_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Filter for links that go to a specific judgment document (e.g., /doc/123456/)
            if '/doc/' in href and '#' not in href:
                full_url = urljoin(base_url, href)
                if full_url not in doc_links:
                    doc_links.append(full_url)
        
        print(f"Found {len(doc_links)} judgments on this page.")
        
        # Download each PDF
        for i, doc_url in enumerate(doc_links, 1):
            doc_id = doc_url.strip('/').split('/')[-1]
            filepath = os.path.join(download_folder, f"judgment_{doc_id}.pdf")
            
            # Skip if the file was already downloaded in a previous run
            if os.path.exists(filepath):
                print(f"[{i}/{len(doc_links)}] Already exists: {doc_id}.pdf")
                continue
                
            print(f"[{i}/{len(doc_links)}] Downloading: {doc_id}.pdf ...")
            
            try:
                # Trigger the PDF generation by sending a POST request with {'type': 'pdf'}
                pdf_response = session.post(doc_url, data={'type': 'pdf'}, stream=True)
                
                # Verify if the site actually returned a PDF (and not a login or error page)
                content_type = pdf_response.headers.get('Content-Type', '')
                if 'application/pdf' in content_type:
                    with open(filepath, 'wb') as f:
                        for chunk in pdf_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                else:
                    print(f"  -> Skipped. PDF not available. (Check if you exceeded your monthly quota of 25 downloads or if your cookie is expired).")
            
            except requests.exceptions.RequestException as e:
                print(f"  -> Failed to download {doc_id}: {e}")
            
            # CRITICAL: A 3-second delay between requests to prevent your IP from being banned
            time.sleep(3) 

if __name__ == "__main__":
    # You can change max_pages to scrape deeper into the search results
    download_kanoon_pdfs(search_query="gst", max_pages=1)'''


import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

BASE_URL = "https://rattanadvocates.com"
PAGE_URL = "https://rattanadvocates.com/judgments-under-section-73-74-of-cgst-act/"

SAVE_DIR = "../gst_database/rattan_judgments"
os.makedirs(SAVE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def download_pdf(pdf_url):

    try:

        filename = os.path.basename(urlparse(pdf_url).path)

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        filepath = os.path.join(SAVE_DIR, filename)

        if os.path.exists(filepath):
            print("Already exists:", filename)
            return

        print("Downloading:", filename)

        response = requests.get(pdf_url, headers=HEADERS, timeout=30)

        if response.status_code == 200 and "pdf" in response.headers.get("Content-Type", ""):

            with open(filepath, "wb") as f:
                f.write(response.content)

        else:
            print("Not a PDF:", pdf_url)

        time.sleep(1)

    except Exception as e:
        print("Error:", e)


def crawl_rattan_judgments():

    print("Accessing page...")

    response = requests.get(PAGE_URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")

    pdf_links = []

    # Find all links containing download or view
    for link in soup.find_all("a", href=True):

        href = link.get("href")

        if "download" in href.lower() or href.lower().endswith(".pdf"):

            full_url = urljoin(BASE_URL, href)

            pdf_links.append(full_url)

    print("Found PDF links:", len(pdf_links))

    for pdf in pdf_links:

        download_pdf(pdf)


crawl_rattan_judgments()

print("Download complete.")