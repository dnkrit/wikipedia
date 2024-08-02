import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def initialize_browser():
    # Настройки веб-драйвера Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Запуск браузера в фоновом режиме
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Создаем экземпляр веб-драйвера Chrome
    service = Service('/path/to/chromedriver')  # Укажите путь к вашему файлу chromedriver
    browser = webdriver.Chrome(service=service, options=chrome_options)

    return browser


def search_wikipedia(browser, query):
    wikipedia_search_url = f"https://ru.wikipedia.org/wiki/{query}"
    browser.get(wikipedia_search_url)
    time.sleep(2)  # Ждем 2 секунды для полной загрузки страницы


def list_paragraphs(browser):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    paragraphs = soup.find_all('p')
    for i, p in enumerate(paragraphs, 1):
        print(f"Параграф {i}: {p.text}\n")


def list_links(browser):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    internal_links = [link['href'] for link in links if link['href'].startswith('/wiki/')]
    for i, link in enumerate(internal_links, 1):
        print(f"Ссылка {i}: https://ru.wikipedia.org{link}")


def main():
    browser = initialize_browser()

    try:
        query = input("Введите запрос: ")
        search_wikipedia(browser, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")

            choice = input("Ваш выбор: ")

            if choice == '1':
                list_paragraphs(browser)
            elif choice == '2':
                list_links(browser)
                link_choice = int(input("Введите номер ссылки для перехода: "))
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                links = soup.find_all('a', href=True)
                internal_links = [link['href'] for link in links if link['href'].startswith
                ('/wiki/')]
                if 1 <= link_choice <= len(internal_links):
                    selected_link = internal_links[link_choice - 1]
                    browser.get(f"https://ru.wikipedia.org{selected_link}")
                    time.sleep(2)  # Ждем 2 секунды для полной загрузки страницы
                else:
                    print("Неверный выбор ссылки.")
            elif choice == '3':
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        browser.quit()


if __name__ == "__main__":
    main()