# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 18:22:45 2024
Modificado em: 09/09/2024

"""

#test mercado livre

#https://www.mercadolivre.com.br/ofertas


'''

TODO:
    - armazenas todas as informações em listas. OK
    - capturar todas as páginas. OK
    - refatorar todo o código utilizando de funções e boas praticas.
    - tratar possiveis erros em produção. OK
    - obter os valores corretamente. OK
    - EXTRA: trocar selenium por BeautifulSoup.

    - testar script em docker

'''

import os
import warnings
warnings.filterwarnings('ignore')

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

VAR_PATH_PRINCIPAL = os.getcwd()
VAR_PATH_DRIVER = "chromedriver.exe"
VAR_TIPO_SELENIUM = 2
VAR_SLEEP_10 = 10


def pfun_chrome_get_driver(
        tipo=1,
        mostrar_driver=True
        ):

    if (tipo == 1):

        VAR_PATH_CHROME_DRIVER = f"{VAR_PATH_PRINCIPAL}/{VAR_PATH_DRIVER}"

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")

        if not mostrar_driver:
            driver = uc.Chrome(
                driver_executable_path=VAR_PATH_CHROME_DRIVER,
                options=options,
                headless=True
                )
        else:
            driver = uc.Chrome(
                driver_executable_path=VAR_PATH_CHROME_DRIVER,
                options=options
                )
        driver.execute_script('return navigator.webdriver')

        display = None

    elif (tipo == 2):

        display = Display(visible=0, size=(1200,800))
        display.start()
        print('\n>>>>> INICIANDO DISPLAY!!! <<<<<\n')

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")

        VAR_PATH_CHROME_DRIVER = f'{VAR_PATH_PRINCIPAL}/src/chromedriver'
        driver = uc.Chrome(
            driver_executable_path=VAR_PATH_CHROME_DRIVER,
            options=options
            )
        driver.execute_script('return navigator.webdriver')

    else:
        print('DRIVER NAO LOCALIZADO!!!')
        driver, display = None, None

    return driver, display


def pfun_driver_check_connection(driver, url, tempo_espera=2):
    check_conection = True
    while check_conection:
        try:

            driver.get(url)
            check_conection = False

        except:
            pass
    sleep(tempo_espera)


def pfun_driver_get_cookie(driver):

    try:

        button = WebDriverWait(driver, VAR_SLEEP_10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'button[data-testid="action:understood-button"]'
                ))
        )
        button.click()

    except:
        print('\n>>>>> ERRO AO INICIALIZAR COOKIES!!!\n')


def pfun_close_selenium_driver(driver, display):

    try:

        driver.close()
        driver.quit()

    except:
        pass

    try:

        #pausando o display
        if display != None:
            print('\n>>>>> PAUSANDO DISPLAY!!! <<<<<\n')
            display.stop()

    except:
        pass


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

url_href = 'https://www.mercadolivre.com.br/ofertas'


try:
    driver, display = pfun_chrome_get_driver(VAR_TIPO_SELENIUM)
except Exception as e:
    print(e)
    driver, display = None, None

if driver != None:

    list_products = []
    list_erros = []
    check_count = True

    pfun_driver_check_connection(driver, url_href)
    pfun_driver_get_cookie(driver)

    next_button = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next")
    a_tag = next_button.find_element(By.TAG_NAME, "a")
    svg_element = a_tag.find_element(By.TAG_NAME, "svg")
    svg_height = int(svg_element.get_attribute('height'))

    for count in range(0, svg_height):
        if  count > 0:
            try:
                next_page = driver.find_element(By.CLASS_NAME, 'andes-pagination__button--next')
                url = next_page.find_element(By.TAG_NAME, 'a')
                url_href = url.get_attribute('href')

            except:
                check_count = False

        print(url_href)

        pfun_driver_check_connection(driver, url_href)
        pfun_driver_get_cookie(driver)

        divs_promotion_itens = driver.find_elements(By.CLASS_NAME, "promotion-item")
        for item in divs_promotion_itens:
            try:
                data = {}
                data['product_link'] = item.find_element(By.CLASS_NAME, "promotion-item__link-container").get_attribute("href")
                data['product_image'] = item.find_element(By.CLASS_NAME, "promotion-item__img").get_attribute("src")
                data['product_title'] = item.find_element(By.CLASS_NAME, "promotion-item__title").text
                data['previous_price'] = item.find_element(By.CLASS_NAME, "andes-money-amount--previous").text
                data['current_price'] = item.find_element(By.CLASS_NAME, "andes-money-amount--cents-superscript").text
                data['discount'] = item.find_element(By.CLASS_NAME, "promotion-item__discount-text").text
                data['installments'] = item.find_element(By.CLASS_NAME, "promotion-item__installments").text
                data['seller'] = item.find_element(By.CLASS_NAME, "promotion-item__seller").text

                list_products.append(data)

            except:
                list_erros.append(data)

    pfun_close_selenium_driver(driver, display)
