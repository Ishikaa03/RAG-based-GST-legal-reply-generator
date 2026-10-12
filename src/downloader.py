'''import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

BASE_DOMAIN = "https://gstcouncil.gov.in"
PRESS_RELEASE_LIST = "https://gstcouncil.gov.in/press-release?page={}"

SAVE_DIR = "../gst_database/gst_council_press_releases"
os.makedirs(SAVE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def download_pdf(url):

    try:

        filename = os.path.basename(urlparse(url).path)

        if not filename.endswith(".pdf"):
            return

        path = os.path.join(SAVE_DIR, filename)

        if os.path.exists(path):
            print("Already exists:", filename)
            return

        print("Downloading:", filename)

        r = requests.get(url, headers=HEADERS, timeout=30)

        if r.status_code == 200 and len(r.content) > 1000:

            with open(path, "wb") as f:
                f.write(r.content)

        else:
            print("Invalid PDF:", url)

        time.sleep(1)

    except Exception as e:
        print("Download error:", e)


def crawl_press_release_pages(max_pages=50):

    for page in range(max_pages):

        url = PRESS_RELEASE_LIST.format(page)

        print(f"\nCrawling Page {page}: {url}")

        try:

            r = requests.get(url, headers=HEADERS)

            soup = BeautifulSoup(r.text, "html.parser")

            # Find all PDF links directly
            for link in soup.find_all("a", href=True):

                href = link["href"]

                if ".pdf" in href.lower():

                    full_url = urljoin(BASE_DOMAIN, href)

                    download_pdf(full_url)

        except Exception as e:

            print("Page crawl error:", e)

        time.sleep(2)


# Run
crawl_press_release_pages(max_pages=50)

print("\nDownload complete.")'''




'''import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs(url, download_folder="gst_circulars"):
    # Create a directory to store the downloaded PDFs
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Use a User-Agent header to prevent basic anti-bot blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Connecting to {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to access the website: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all anchor tags (links)
    links = soup.find_all('a')
    pdf_links = []

    # Filter out links that end with '.pdf'
    for link in links:
        href = link.get('href')
        if href and '.pdf' in href.lower():
            # Convert relative URLs to absolute URLs
            full_url = urljoin(url, href)
            if full_url not in pdf_links:
                pdf_links.append(full_url)

    print(f"Found {len(pdf_links)} PDF files. Starting download...")

    # Download each PDF
    for i, pdf_url in enumerate(pdf_links, 1):
        # Extract the filename from the URL
        filename = pdf_url.split('/')[-1]
        
        # Handle cases where the URL might have query parameters after .pdf
        if '?' in filename:
            filename = filename.split('?')[0]
            
        filepath = os.path.join(download_folder, filename)
        
        print(f"[{i}/{len(pdf_links)}] Downloading: {filename}...")
        try:
            pdf_response = requests.get(pdf_url, headers=headers)
            pdf_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(pdf_response.content)
                
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {pdf_url}: {e}")

    print(f"\nTask Complete! All PDFs have been saved to the '{download_folder}' folder.")

if __name__ == "__main__":
    target_url = "https://cbic-gst.gov.in/hindi/circulars.html"
    download_pdfs(target_url) '''


import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_english_pdfs(url, download_folder="gst_english_notifications"):
    # Create a directory to store the downloaded PDFs
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Use a User-Agent header to prevent anti-bot blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Connecting to {url}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to access the website: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []

    # Find all tables on the page
    tables = soup.find_all('table')
    
    for table in tables:
        # Go through each row in the table
        rows = table.find_all('tr')
        for row in rows:
            # Find all cells (columns) in the row
            cols = row.find_all(['td', 'th'])
            
            # The table has 4 columns: [0] No. & Date, [1] English, [2] Hindi, [3] Subject
            # We check if the row has at least 2 columns to avoid header/year rows (like "2022")
            if len(cols) >= 2:
                english_column = cols[1] # Index 1 corresponds to the 2nd column
                
                # Find all links within the English column only
                links = english_column.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and '.pdf' in href.lower():
                        # Convert relative URLs to absolute URLs
                        full_url = urljoin(url, href)
                        if full_url not in pdf_links:
                            pdf_links.append(full_url)

    print(f"Found {len(pdf_links)} English PDF files. Starting download...")

    # Download each PDF
    for i, pdf_url in enumerate(pdf_links, 1):
        filename = pdf_url.split('/')[-1]
        
        if '?' in filename:
            filename = filename.split('?')[0]
            
        filepath = os.path.join(download_folder, filename)
        
        print(f"[{i}/{len(pdf_links)}] Downloading: {filename}...")
        try:
            pdf_response = requests.get(pdf_url, headers=headers)
            pdf_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(pdf_response.content)
                
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {pdf_url}: {e}")

    print(f"\nTask Complete! All English PDFs have been saved to the '{download_folder}' folder.")

if __name__ == "__main__":
    target_url = "https://cbic-gst.gov.in/hindi/central-tax-notifications.html"
    download_english_pdfs(target_url)