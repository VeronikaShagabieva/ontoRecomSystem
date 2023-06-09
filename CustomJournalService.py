
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin

class CustomJournalService:
    def __init__(self):
        self.journal_url = 'https://lobachevskii-dml.ru/journal/ivm/676'  # URL-адрес журнала

    def initialize(self):
        page = requests.get(self.journal_url)  # Запрос страницы журнала
        self.journal_soup = BeautifulSoup(page.text, "html.parser")  # Создание объекта BeautifulSoup для парсинга страницы

    def parse_journal(self):
        self.articles = []  # Список для хранения статей
        self.articles_links = []  # Список для хранения ссылок на статьи
        self.parse_volume(self.journal_url)  # Извлечение статей из журнала

        for i, article in enumerate(self.articles):
            article['links'] = self.articles_links[i]  # Добавление ссылки на статью

        with open('articles.json', 'w', encoding='utf-8') as outfile:  # Открытие файла для записи результатов
            json.dump(self.articles, outfile, ensure_ascii=False, indent=4)  # Запись статей в формате JSON

    def parse_volume(self, volume_link):
        page = requests.get(volume_link)  # Запрос страницы выпуска журнала
        soup = BeautifulSoup(page.text, "html.parser")  # Создание объекта BeautifulSoup для парсинга страницы
        page_table = soup.find('table', class_='table')  # Поиск таблицы с данными о выпуске
        article_links = page_table.find_all('a', href=True)  # Поиск ссылок на статьи

        for article_link in article_links:
            article = self.parse_article(urljoin(self.journal_url, article_link['href']))  # Извлечение информации о статье
            if article:
                self.articles.append(article)  # Добавление статьи в список
                self.articles_links.append(article_link['href'])  # Добавление ссылки на статью в список

    def parse_article(self, article_link):
        page = requests.get(article_link)  # Запрос страницы статьи
        soup = BeautifulSoup(page.text, "html.parser")  # Создание объекта BeautifulSoup для парсинга страницы
        wrapper = soup.find('ol', class_='breadcrumb')  # Поиск элемента-обертки статьи

        if wrapper:
            headings = wrapper.parent.find_all('h4')  # Поиск заголовков статьи
            title = soup.find('h3', id="title")  # Извлечение заголовка статьи
            keywords_heading = None

            for heading in headings:
                if heading.text.strip().lower() == 'ключевые слова':  # Поиск заголовка "Ключевые слова"
                    keywords_heading = heading
                    break

            if keywords_heading:
                keywords_wrapper = keywords_heading.parent
                keyword_spans = keywords_wrapper.find_all('span')  # Поиск ключевых слов
                keywords = []  # Список для хранения ключевых слов

                for keyword_span in keyword_spans:
                    word = keyword_span.text.replace(';', '').replace('.', '').strip().lower()  # Извлечение ключевого слова
                    if word:
                        keywords.append(word)  # Добавление ключевого слова в список

               

                article = {
                    'title': title.text,  # Заголовок статьи
                    'keywords': keywords  # Ключевые слова статьи
                }

                return article  # Возврат информации о статье

        return None  # В случае отсутствия информации о статье, возвращается значение None


journal = CustomJournalService()  # Создание экземпляра класса CustomJournalService
journal.initialize()  # Инициализация класса
journal.parse_journal()  # Парсинг журнала и сохранение результатов в файле articles.json
