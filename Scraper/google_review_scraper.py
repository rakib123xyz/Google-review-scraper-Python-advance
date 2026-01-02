import json
import time
import csv
import os
import logging
from camoufox.sync_api import Camoufox

# Read the cookies from the JSON file
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

# Validate and adjust the sameSite attribute if necessary
for cookie in cookies:
    if cookie.get('sameSite') not in ['Strict', 'Lax', 'None']:
        cookie['sameSite'] = 'None'  # Default to 'None' if not correctly set


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)


def is_page_at_bottom(page, element):
    """
    Checks if the scrollable element has reached the bottom.

    Args:
        page: The Playwright page object.
        element: The element to check scroll position for.

    Returns:
        bool: True if at bottom, False otherwise.
    """
    # Get the current scroll position of the element
    scroll_position = element.evaluate('el => el.scrollTop', element)

    # Get the maximum scroll position of the element
    max_scroll_position = element.evaluate('el => el.scrollHeight - el.clientHeight', element)

    # Check if the current scroll position is equal to or near the maximum scroll position
    return max_scroll_position - scroll_position <= 5




def scroll_to_bottom(page,element,wait):
    """
    Scrolls the element to the bottom to load more content.

    Args:
        page: The Playwright page object.
        element: The element to scroll.
        wait (int): Time in seconds to wait after scrolling.
    """

    while not is_page_at_bottom(page,element):
        # Scroll down one screen
        page.evaluate('element => element.scrollBy(0, 4000)', element)
        reviews = page.query_selector_all('''xpath=//div[@jsname="ShBeI"]''')
        logging.info(f"{len(reviews)} reviews loaded")
        # max review load limit
        if len(reviews) >= 1000 :
            logging.info('Max reviews loaded...')
            break


        # Wait for the page to scroll
        time.sleep(wait) # Adjust this value as needed







def add_data_to_csv(data_dict, csv_filename):
    """
    Appends a dictionary of data to a CSV file.

    Args:
        data_dict (dict): The data to write.
        csv_filename (str): The path to the CSV file.
    """
    # Check if the CSV file exists
    file_exists = os.path.exists(csv_filename)

    with open(csv_filename, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = list(data_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

        # If the file doesn't exist, write the hea/
        if not file_exists:
            writer.writeheader()

        # Write the data from the dictionary to the CSV file
        writer.writerow(data_dict)

def block_resources(route, request):
    """
    Blocks unnecessary resources to speed up loading and reduce bandwidth.

    Args:
        route: The Playwright route object.
        request: The Playwright request object.
    """
    # Block images, media, and unnecessary third-party scripts
    if request.resource_type in ['image', 'media', 'font', 'stylesheet']:
        route.abort()
    elif 'google-analytics' in request.url or 'ads' in request.url:
        route.abort()
    else:
        route.continue_()


# Read input URLs from input.txt
with open('input.txt', 'r') as f:
    input_urls = [line.strip() for line in f if line.strip()]


with Camoufox(
    headless=False,
    geoip=True,  # Automatically set locale/timezone based on IP for stealth
    locale='en-US', # Enforce US English
) as browser:

    for i, input_url in enumerate(input_urls):
        logging.info(f"Processing URL {i+1}/{len(input_urls)}: {input_url}")
        # Open a new page (Camoufox manages the context and fingerprint)
        page = browser.new_page()

        # Load cookies from a file
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)

        # Add cookies to the context
        page.context.add_cookies(cookies)
        
        # Navigate to the website where the cookies should be used
        page.goto(input_url,timeout=100000)

        # 🔎 CAPTCHA detection (generic)
        captcha_selector = 'xpath=//div[@id="recaptcha"]'

        if page.locator(captcha_selector).count() > 0:
            logging.warning("⚠️ CAPTCHA detected. Please solve it manually.")
            input("Press ENTER after solving CAPTCHA...")

        # ✅ Always wait until page is usable
        page.wait_for_load_state("networkidle")
        time.sleep(30)
        
        page.query_selector('xpath=//span[@class="z3HNkc"]/following-sibling::span//a').click()
        page.wait_for_selector('xpath=//div[@jsname="ShBeI"]',timeout=120000)
        page.query_selector('xpath=//div[@data-sort="2"]').click()
        page.wait_for_selector('xpath=//div[@jsname="ShBeI"]',timeout=120000)
        time.sleep(3)

        review_list = page.query_selector('xpath=//div[@class="RVCQse"]')
        logging.info("Starting scroll to load reviews...")

        scroll_to_bottom(page,review_list,2)
        time.sleep(20)
        scroll_to_bottom(page, review_list, 3)
        for i in range(50):
            scroll_to_bottom(page, review_list, 2)
            # user_input = input("If load is complete please type done: ")
            # time.sleep(1)
            # if user_input == "done":
            #     break
        # //div[@class="TSUbDb"]   reviewer_Name   //div[contains(@class,'gws-localreviews__google-review')]


        reviews = page.query_selector_all('''xpath=//div[@jsname="ShBeI"]''')
        dealer = page.query_selector('xpath=//div[@class="ZhoJLd"]').inner_text()
        dealer_location = page.query_selector('xpath=//div[@class="EcGBwf"]').inner_text()
        logging.info(f"Extracting data for {len(reviews)} reviews...")
        for review in reviews:
            data = {}
            data['Dealer Name'] = dealer
            data['Dealer Location'] = dealer_location
            try:
                reviewer = review.query_selector('xpath=.//div[@class="Vpc5Fe"]').text_content()
                data["Reviewer"] = reviewer
            except:
                pass
            try:
                rating = review.query_selector('xpath=.//div[@class="dHX2k "]').get_attribute('aria-label')
                data['Rating'] = rating
            except:
                pass
            try:
                Date = review.query_selector('xpath=.//span[@class="y3Ibjb"]').text_content()
                data['Date'] =Date
                # year = Date.split(sep=' ')[0].split(sep='/')[2]
                # data['Year'] = year

            except:
                pass




            try:
                try:
                    review_text = review.query_selector('xpath=.//div[@class="OA1nbd"]').text_content()
                    data['Review Text'] = review_text
                except:
                    review_text = review.query_selector('xpath=.//div[@class="OA1nbd"]').text_content()
                    data['Review Text'] = review_text
                    pass


            except:
                pass

            # print(data)
            add_data_to_csv(data, f'review_list_{i+1}.csv')
        logging.info(f"Finished processing URL: {input_url}")
        
        page.close()
