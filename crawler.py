from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep
# from trash import html_mock

out: list


def get_linkedin():
    print("getting Linkedin positions (11)")

    search_urls = [
        # Portugal:
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Manager&location=Lisboa&geoId=104303357&f_E=4%2C5%2C6',
        'https://www.linkedin.com/jobs/search/?keywords=Delivery%20Manager&location=Lisboa&geoId=104303357&f_E=4%2C5%2C6',
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Director&location=Lisboa&geoId=104303357&f_E=4%2C5%2C6',

        # Sofia:
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Manager&location=Sofia%2C%20Sofia%20City%2C%20Bulgaria&geoId=103835801&f_E=4%2C5%2C6',
        'https://www.linkedin.com/jobs/search/?keywords=Delivery%20Manager&location=Sofia%2C%20Sofia%20City%2C%20Bulgaria&geoId=103835801&f_E=4%2C5%2C6',
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Director&location=Sofia%2C%20Sofia%20City%2C%20Bulgaria&geoId=103835801&f_E=4%2C5%2C6',

        # Ukr
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Director&location=Ukraine&geoId=102264497&f_E=4%2C5%2C6&f_WT=2',
        'https://www.linkedin.com/jobs/search/?keywords=Program%20Manager&location=Ukraine&geoId=102264497&f_E=4%2C5%2C6&f_WT=2',
        'https://www.linkedin.com/jobs/search/?keywords=Delivery%20Manager&location=Ukraine&geoId=102264497&f_E=4%2C5%2C6&f_WT=2',
        'https://www.linkedin.com/jobs/search/?keywords=Delivery%20Director&location=Ukraine&geoId=102264497&f_E=4%2C5%2C6&f_WT=2',
        'https://www.linkedin.com/jobs/search/?keywords=Head%20of%20delivery&location=Ukraine&geoId=102264497&f_E=4%2C5%2C6&f_WT=2',
    ]

    global out
    out = []

    # login_url = "https://www.linkedin.com/search/results/all/?keywords=program%20manager&origin=TYPEAHEAD_HISTORY&searchId=18d9c16b-a8af-4f19-8b33-2d84c2c9a9e4&sid=_5%3A&spellCorrectionEnabled=true"

    # region selenium init
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')  # disabled = show window
    driver = webdriver.Chrome(options=chrome_options)
    # endregion


    # def scroll_to_bottom_of_the_page():
    #     last_height = driver.execute_script("return document.body.scrollHeight")
    #     while True:
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         sleep(2)  # Wait for new content to load
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         if new_height == last_height:
    #             break
    #         last_height = new_height

    # def scroll_element_to_bottom(element):
    #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

    # driver.get(login_url)
    # sleep(3)



    # email = driver.find_element(By.ID, "username")
    # email.send_keys('k7.junk.email@gmail.com')
    # sleep(0.1)
    #
    # password = driver.find_element(By.ID, "password")
    # password.send_keys(f'aje#$fcwsdfq2#$#$43534rdfxWAc{Keys.RETURN}')
    #
    # sleep(2)


    first = True


    for url in search_urls:
        driver.get(url)
        sleep(10)

        if first:
            disagree = driver.find_element(By.CSS_SELECTOR, "#artdeco-global-alert-container > div > section > div > div.artdeco-global-alert-action__wrapper > button:nth-child(2)")
            disagree.click()
            first = False
            sleep(0.1)


        while True:
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)  # adjust sleep time to allow new content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == old_height:
                break


        html_content = driver.page_source
        _parse_data(html_content)

    driver.quit()

    return out


def _parse_data(input_html):
    soup = BeautifulSoup(input_html, "html.parser")
    # print(soup.prettify())

    soup = soup.find(class_='jobs-search__results-list')
    positions = soup.find_all('li')
    # locations = soup.find_all(class_="pb-2 md:pb-0 md:mr-4")

    print(len(positions))
    # print(positions[0].prettify())
    for x in range(len(positions)):
        _ = positions[x]
    #     # print(_.prettify())
    #     title = _.find('strong').text.strip()
    #     print(title)

        link = _.find('a')
        title = link.find('span').text.strip()
        # print(title)
        link = link['href'].strip()
        link = link.split('?')[0]
        # print(link)

        location = _.find(class_='job-search-card__location').text.strip()
        # print(location)

        company = _.find('h4').text.strip()
        # print(f"{title}, {link}, location: {location}, company: {company}")

        tulip = (company, {
            'position': title,
            'location': location,
            'link': link,
        })
        out.append(tulip)
