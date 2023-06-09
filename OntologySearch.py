import json
from rdflib import Graph, URIRef

def load_keywords_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        keywords = []
        for item in data:
            keywords.extend(item['keywords'])
    return keywords

def find_similar_words(keyword, ontology_graph):
    similar_words = []
    for subj, pred, obj in ontology_graph:
        if keyword in obj.lower():
            similar_words.append(obj)
    return similar_words

def extract_subclasses(concept_uri, ontology_graph):
    subclasses = []
    for subj, pred, obj in ontology_graph.triples(
        (None, URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"), URIRef(concept_uri))):
        subclasses.append(subj)
    return subclasses

# Загрузка ключевых слов из articles.json
keywords = load_keywords_from_json("articles.json")

# Загрузка онтологии OntoMathPRO.owl в объект графа
ontology_graph = Graph()
ontology_graph.parse("C:/Users/vshagabieva/Desktop/Диплом/OntoMathPro.owl")

# Расширенный список ключевых слов с учетом упорядочивания
extended_keywords = []

# Поиск похожих слов и извлечение подклассов для каждого ключевого слова
for keyword in keywords:
    similar_words = find_similar_words(keyword, ontology_graph)
    subclasses = extract_subclasses(keyword, ontology_graph)

    # Добавление текущего ключевого слова и его похожих слов в расширенный список с учетом порядка
    extended_keywords.append(keyword)
    extended_keywords.extend(similar_words)
    extended_keywords.extend(subclasses)

# Удаление дубликатов из расширенного списка
extended_keywords = list(set(extended_keywords))

# Вывод расширенного списка ключевых слов
print("Расширенный список ключевых слов:")
for keyword in extended_keywords:
    print(keyword)

    # Сохранение расширенного списка ключевых слов в JSON-файл
output_file = "extended_keywords.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(extended_keywords, json_file, ensure_ascii=False)

print(f"Расширенный список ключевых слов сохранен в файл: {output_file}")
