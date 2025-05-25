import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrap_mfg(query):
    url = f"https://www.mfg.com/manufacturer-directory/page/1/?manufacturing_location=United+States&capability={query}&search&ep_filter_manufacturing_location=united-states&ep_filter_capability={query}"

    # Set the maximum pages to scrape
    total_pages = 2
    all_manufacturers = []

    # Custom headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CustomScraper/1.0; +http://example.com/)"
    }

    # Retry settings for rate limiting (429)
    max_retries = 5
    retry_delay = 60  # seconds to wait before retrying on 429

    # Scraping loop
    for page in range(1, total_pages + 1):
        page_url = url.replace("page/1", f"page/{page}")
        print(f"Scraping page {page}: {page_url}")
        
        retries = 0
        while retries < max_retries:
            response = requests.get(page_url, headers=headers)
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                retries += 1
                print(f"Page {page} returned 429. Retry {retries}/{max_retries} after {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to fetch page {page}: Status code {response.status_code}")
                break

        if response.status_code != 200:
            print(f"Skipping page {page} due to errors.")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        containers = soup.select("div.bg-white.container.hover-glow.p-4.mb-3")

        if not containers:
            print(f"No manufacturer containers found on page {page}. Assuming end of pages.")
            break

        print(f"Found {len(containers)} manufacturer containers on page {page}.")

        # Extract data from each manufacturer container
        for container in containers:
            name_tag = container.select_one("h2.d-inline-block.mr-4.my-0 a")
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            details_url = name_tag['href'] if name_tag and name_tag.has_attr('href') else "N/A"
            if details_url != "N/A" and details_url.startswith("/"):
                details_url = "https://www.mfg.com" + details_url

            location_tag = container.select_one("p[title='Location']")
            location = location_tag.get_text(strip=True) if location_tag else "N/A"

            rating_tag = container.select_one("strong.text-dark")
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

            desc_tag = container.select_one("div[id^='smry']")
            description = desc_tag.get_text(separator=" ", strip=True) if desc_tag else "N/A"

            capability_tags = container.select("div.d-contents.capabilities a.badge-pill.bg-secondary")
            capabilities = ", ".join([cap.get_text(strip=True) for cap in capability_tags]) if capability_tags else "N/A"

            post_tag_container = container.select_one("div.collapse.col-12.col-md-11.pl-0")
            post_tags = ", ".join([pt.get_text(strip=True) for pt in post_tag_container.select("a.badge-pill.bg-light")]) if post_tag_container else "N/A"

            manufacturer = {
                "Name": name,
                "Details URL": details_url,
                "Location": location,
                "Rating": rating,
                "Description": description,
                "Capabilities": capabilities,
                "Post Tags": post_tags
            }

            all_manufacturers.append(manufacturer)

        # Pause between pages to avoid rate limits
        time.sleep(1)
    return all_manufacturers
