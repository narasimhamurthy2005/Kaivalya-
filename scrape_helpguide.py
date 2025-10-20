import requests
from bs4 import BeautifulSoup
import os

# List of pages to scrape
urls = [
    'https://www.heart.org/en/health-topics/heart-attack'
]

# Create a folder to save scraped text files
os.makedirs("scraped_pages", exist_ok=True)

# Define headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

for url in urls:
    if not url.strip():  # Skip empty URLs
        print("Skipped empty URL")
        continue
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        continue
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all paragraph text
    content = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])
    
    # Generate a valid file name from the URL
    page_name = url.strip('/').split('/')[-1]
    filename = os.path.join("scraped_pages", f"{page_name}.txt")
    
    # Save the content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Saved content to {filename}")
