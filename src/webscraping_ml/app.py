# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 18:22:45 2024
Modificado em: 09/09/2024

"""

# test mercado livre

# https://www.mercadolivre.com.br/ofertas


import os
import logging
from typing import List, Optional
from time import sleep
from schema import ProductData

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import requests
import json


logging.basicConfig(level=logging.INFO)
# test


class BeautifulSoupDriverManager:
    def __init__(self, driver_type: int = 1, show_browser: bool = True):
        self.driver_type = driver_type
        self.show_browser = show_browser
        self.driver: Optional[webdriver.Chrome] = None
        self.display: Optional[Display] = None

    def get_driver(self):
        var_path_principal = os.getcwd()
        var_path_driver = "chromedriver.exe"

        if self.driver_type == 1:
            var_path_chrome_driver = os.path.join(var_path_principal, var_path_driver)
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--incognito")

            self.driver = uc.Chrome(
                driver_executable_path=var_path_chrome_driver,
                options=options,
                headless=not self.show_browser,
            )
            self.driver.execute_script("return navigator.webdriver")

        elif self.driver_type == 2:
            self.display = Display(visible=0, size=(1200, 800))
            self.display.start()
            logging.info("Starting virtual display.")

            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--incognito")

            var_path_chrome_driver = os.path.join(
                var_path_principal, "src/chromedriver"
            )
            self.driver = uc.Chrome(
                driver_executable_path=var_path_chrome_driver, options=options
            )
            self.driver.execute_script("return navigator.webdriver")

        else:
            logging.error("Driver type not recognized.")
            self.driver, self.display = None, None

        return self.driver, self.display

    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
            logging.info("Driver closed.")

        if self.display:
            self.display.stop()
            logging.info("Virtual display stopped.")


class WebScraper:
    def __init__(self):
        pass

    def get_html(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching URL {url}: {e}")
            return None

    def scrape_products(self, url: str) -> List[ProductData]:
        products = []
        html = self.get_html(url)

        if not html:
            return products

        soup = BeautifulSoup(html, "html.parser")

        promotion_items = soup.select('div[class*="poly-card"]')
        for item in promotion_items:

            product_link = item.find(class_="poly-component__title")
            product_link = product_link["href"] if product_link else ""

            product_image = item.find(class_="poly-component__picture")
            product_image = product_image["data-src"] if product_image else ""
            product_title = item.find(class_="poly-component__title")

            product_title = product_title.text.strip() if product_title else ""

            previous_price = (
                item.find(class_="andes-money-amount--previous").text.strip()
                if item.find(class_="andes-money-amount--previous")
                else ""
            )
            current_price = item.find(
                class_="andes-money-amount--cents-superscript"
            )

            current_price = current_price.text.strip() if current_price else ""
            discount = (
                item.find(class_="andes-money-amount__discount").text.strip()
                if item.find(class_="andes-money-amount__discount")
                else ""
            )
            installments = (
                item.find(class_="poly-price__installments").text.strip()
                if item.find(class_="poly-price__installments")
                else ""
            )
            seller = (
                item.find(class_="poly-component__seller").text.strip()
                if item.find(class_="poly-component__seller")
                else ""
            )

            data = ProductData(
                product_link=product_link,
                product_image=product_image,
                product_title=product_title,
                previous_price=previous_price,
                current_price=current_price,
                discount=discount,
                installments=installments,
                seller=seller,
            )
            products.append(data)

        return products


if __name__ == "__main__":
    url = "https://www.mercadolivre.com.br/ofertas"
    scraper = WebScraper()

    products = scraper.scrape_products(url)

    logging.info(f"Scraped {len(products)} products.")
    if products:
        for product in products:
            logging.info(json.dumps(product.dict(), indent=2))
