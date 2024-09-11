from logging import addLevelName
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
)
import time
from openpyxl import Workbook

proxies = [
    
    # Add more proxies as needed
]


def get_random_proxy():
    return random.choice(proxies)


def create_driver_with_proxy():
    proxy = get_random_proxy()
    firefox_options = Options()
    firefox_options.add_argument("--proxy-server=%s" % proxy)
    cdp = "/usr/bin/geckodriver"
    service = Service(executable_path=cdp)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

driver = create_driver_with_proxy()
page = 1

salon_list = []
salon_links = []
salon_addresses = []

def switch_proxy():
    global driver
    driver.quit()
    driver = create_driver_with_proxy()




def scrape_salons():

    for page in range(1, 132):
        link = f"https://www.nearbyspasalon.com/category/salons?filter_state=0&filter_city=0&filter_sort_by=1&page={page}"
        driver.get(link)
        res = driver.find_elements(
            By.XPATH, '//h3[@class="pt-2 listing_for_map_hover"]'
        )
        res2 = driver.find_elements(By.TAG_NAME, "address")

        for j in res:
            salon_list.append(j.text)
        for k in res2:
            salon_addresses.append(k.text)


        switch_proxy()

    for salon_name in salon_list:
        salon_name = salon_name.lower()
        salon_name = (
            salon_name.replace(" ", "-")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
            .replace("&", "")
            .replace("|", "")
        )
        salon_links.append(f"https://nearbyspasalon.com/listing/{salon_name}")

    driver.quit()
    return salon_list, salon_addresses, salon_links


def save_to_excel(salon_names, salon_addresses, salon_links):
    wb = Workbook()
    ws = wb.active
    ws.title = "Salon Data"

    # Add headers
    ws.append(["Salon Name", "Address", "Link"])

    # Add data
    for name, address, link in zip(salon_names, salon_addresses, salon_links):
        ws.append([name, address, link])

    # Save the workbook
    wb.save("salon_data.xlsx")


if __name__ == "__main__":
    print("Scraping salon data...")
    salon_names, salon_addresses, salon_links = scrape_salons()

    print("Saving data to Excel...")
    save_to_excel(salon_names, salon_addresses, salon_links)

    print("Data saved to salon_data.xlsx")
