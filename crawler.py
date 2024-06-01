from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def get_cars():
    search_urls = [
        "https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&year-from=20010&year-to=2025&make=Toyota&model=All&auction-type=All",
    ]

    # region selenium init
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_experimental_option("detach", True)
    # options.add_argument('--proxy-server=YOUR_PROXY_SERVER')
    driver = webdriver.Chrome(options=options)
    # endregion


    for url in search_urls:
        driver.get(url)
        sleep(5)

        items = driver.find_elements(By.CLASS_NAME, "lots-search")

        print(len(items))
        links = []
        for _ in items:
            link = _.find_element(By.CLASS_NAME, 'damage-info')
            links.append(link.get_property('href'))

        for _ in links:
            driver.get(_)
            sleep(10)
            page_title = driver.title
            if page_title != "Attention Required! | Cloudflare":
                html_content = driver.page_source
                with open(f'resources/{page_title}.html', 'w', encoding='utf-8') as file:
                    file.write(html_content)
            else:
                exit("Cloudflare...")

    driver.quit()


get_cars()
