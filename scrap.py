import random
import time
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# Use undetected chromedriver to bypass detection
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")


# Initialize Selenium WebDriver with rotating proxy and user agent
driver = uc.Chrome(options=options)

def scrape_alibaba_suppliers(query):
    """Scrape supplier data from Alibaba based on the user's query."""
    supplier_data = []
    search_url = f'https://www.alibaba.com/trade/search?IndexArea=product_en&SearchText={query}&tab=supplier'

    try:
        print(f"Navigating to {search_url}")
        driver.get(search_url)
        time.sleep(random.uniform(5, 10))  # Random delay to mimic human behavior

        # Simulate scrolling
        for _ in range(random.randint(1, 3)):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(random.uniform(2, 5))

        # Create BeautifulSoup object
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all the card-title divs
        card_title_divs = soup.find_all('div', class_='card-title')

        # Loop through each card-title div
        for card_div in card_title_divs:
            detail_info_div = card_div.find('div', class_='detail-info')

            # Check if detail-info div exists and find <a> inside it
            if detail_info_div:
                a_elements = detail_info_div.find_all('a')
                
                for a in a_elements:
                    url = a['href']
                    url = url if url.startswith('http') else f"https:{url}"
                    print(f"Scraping URL: {url}")

                    one_supplier_data = scrape_supplier_page(url)
                    supplier_data.append(one_supplier_data)

    except Exception as e:
        print(f"Error scraping Alibaba: {e}")

    finally:
        driver.quit()

    return supplier_data

def scrape_supplier_page(url):
    """Scrape individual supplier page for details."""
    try:
        response = requests.get(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        })

        if response.status_code == 200:
            page_soup = BeautifulSoup(response.content, 'html.parser')
            name_tag = page_soup.find('div', class_='info-line top-bar-name')
            if name_tag:
                supplier_name = name_tag.text.strip()
            else:
                supplier_name = ""
            
            location_info_div = page_soup.find('div', class_='location-info')
            supplier_experience = "N/A"
            supplier_location = "N/A"
            if location_info_div:
                location_items = location_info_div.find_all('div', class_='location-item')

                # Extract experience and location if available
                supplier_experience = location_items[0].text.strip() if len(location_items) > 0 else "N/A"
                supplier_location = location_items[1].text.strip() if len(location_items) > 1 else "N/A"
            
            # Find the parent div with class 'block-center'
            block_center_div = page_soup.find('div', class_='block-center')
            categories_only = "N/A"
            if block_center_div:
                # Find all child divs with class 'info-line' inside 'block-center'
                info_lines = block_center_div.find_all('div', class_='info-line')

                # Extract the third div (index 2 as it's zero-based)
                if len(info_lines) >= 3:
                    third_div = info_lines[2]
                    main_categories_text = third_div.get_text(strip=True)
                    categories_only = main_categories_text.replace("Main categories: ", "")

                
            # Grab the 'score-text' inside the 'reviews' div
            reviews_div = page_soup.find('div', class_='reviews')
            score_text = "N/A"
            if reviews_div:
                score_text = reviews_div.find('span', class_='score-text').text

            # Grab all 'li' elements inside the 'supplier-ability' ul
            supplier_ability_div = page_soup.find('ul', class_='supplier-ability')
            supplier_ability_items = []
            if supplier_ability_div:
                supplier_ability_items =supplier_ability_div.find_all('li')

            # Initialize variables to store extracted data
            average_response_time = "N/A"
            on_time_delivery_rate = "N/A"
            revenue = "N/A"
            total_orders = "N/A"

            # Loop through the 'li' items and assign values based on the title
            for item in supplier_ability_items:
                strong_tag = item.find('strong')
                title_tag = item.find('div', class_='title')
                
                if title_tag and strong_tag:
                    title = title_tag.text.strip()
                    value = strong_tag.text.strip()
                    
                    if 'average response time' in title:
                        average_response_time = value
                    elif 'on-time delivery rate' in title:
                        on_time_delivery_rate = value
                    elif 'orders' in title:
                        total_orders = value.split()[0]  # Extract just the number of orders
                    elif 'US' in value:
                        revenue = value
                        
            supplier_data = {
                        "Company Name": supplier_name,
                        "Website": url,
                        "Country": supplier_location,
                        "Experience":supplier_experience,
                        "Manufacturing Capabilities": categories_only,
                        "Rating": score_text,
                        "Response Time": average_response_time,
                        "On Time delivery rate": on_time_delivery_rate,
                        "Revenue":revenue,
                        "Total Orders": total_orders
                    }
            
            return supplier_data

        else:
            print(f"Failed to fetch {url}. Status: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")

    return None

def scrap_suppliers(query):
    print("Welcome to the Alibaba Supplier Finder!")
    print(f"Searching for suppliers of '{query}' on Alibaba...")
    supplier_data = scrape_alibaba_suppliers(query)

    return (supplier_data)

