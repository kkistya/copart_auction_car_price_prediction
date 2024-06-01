from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import certifi
import ssl



def get_cars():
    # ssl._create_default_https_context = ssl._create_unverified_context

    search_urls = [
        "https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=20010&year-to=2025&make=Toyota&model=All&auction-type=All",
    ]

    # region selenium init
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)

    options = uc.ChromeOptions()
    options.add_argument("--headless")  # Optional: Run Chrome in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_argument('--proxy-server=YOUR_PROXY_SERVER')  # Use a proxy server if needed
    driver = uc.Chrome(options=options)
    # endregion

    ssl_context = certifi.where()

    driver.get("https://www.google.com/")
    sleep(2)

    page_title = driver.title
    if page_title != "Attention Required! | Cloudflare":
        html_content = driver.page_source
        with open(f'resources/{page_title}.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
    else:
        exit("Cloudflare...")

    # for url in search_urls:
    #     driver.get(url)
    #     sleep(5)
    #
    #     items = driver.find_elements(By.CLASS_NAME, "lots-search")
    #
    #     print(len(items))
    #     links = []
    #     for _ in items:
    #         link = _.find_element(By.CLASS_NAME, 'damage-info')
    #         links.append(link.get_property('href'))
    #
    #     for _ in links[:2]:
    #         driver.get(_)
    #         sleep(10)
    #         page_title = driver.title
    #         if page_title != "Attention Required! | Cloudflare":
    #             html_content = driver.page_source
    #             with open(f'resources/{page_title}.html', 'w', encoding='utf-8') as file:
    #                 file.write(html_content)
    #         else:
    #             exit("Cloudflare...")

    driver.quit()


get_cars()
