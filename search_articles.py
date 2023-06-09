import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search_articles(keywords):
    search_query = '+'.join(keywords)  # Формирование строки запроса для поиска
    url = f"https://scholar.google.com/scholar?q={search_query}"
    
    # Отправка HTTP-запроса и получение HTML-страницы результатов поиска
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    
    # Извлечение информации о статьях из HTML-страницы
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')
    for result in results:
        title = result.find('h3', class_='gs_rt').text
        url = result.find('a')['href']
        
        article = {
            'title': title,
            'url': url
        }
        articles.append(article)
    
    return articles

def compute_similarity(keywords, articles):
    # Создание корпуса текстов для вычисления близости
    corpus = [article['title'] for article in articles]
    corpus.append(' '.join(keywords))  # Добавление ключевых слов в корпус
    
    # Вычисление TF-IDF векторов для корпуса текстов
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Вычисление матрицы близости (косинусной схожести)
    similarity_matrix = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
    
    # Упорядочивание статей на основе близости
    sorted_indexes = similarity_matrix.argsort()[::-1]
    sorted_articles = [articles[i] for i in sorted_indexes]
    
    return sorted_articles


def read_keywords_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    keywords = data['keywords']
    return keywords


keywords_file_path = 'C:/Users/vshagabieva/Desktop/Диплом/extended_keywords.json'
keywords = read_keywords_from_json(keywords_file_path)
search_results = search_articles(keywords)

# Вывод отсортированных результатов поиска
for article in sorted_results:
    print(article['title'])
    print(article['url'])
    print('---')


