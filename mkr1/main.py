import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

def get_publication_info(publication_url):
    try:
        response = requests.get(publication_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table')
        if table:
            rows = table.find_all('tr')[1:]  # пропускаю перший рядок з заголовками
            publications = []
            for row in rows:
                cells = row.find_all('td')
                publication_year = cells[0].find('em').text.strip()
                title = cells[1].text.strip()
                authors = [author.text.strip() for author in cells[2].find_all('a')]
                publications.append({'publication_year': publication_year, 'title': title, 'authors': authors})
            return publications
    except Exception as e:
        print("Помилка при отриманні інформації про публікації:", e)
    return None


def get_authors_and_works(url):
    authors_and_works = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        author_list = soup.find_all('li', class_='list-group-item')

        for author in author_list:
            author_name = author.a.text
            author_url = 'https://dspace.uzhnu.edu.ua' + author.a['href']
            works_count = author.span.text
            publications = get_publication_info(author_url)
            if publications:
                authors_and_works.append({'author_name': author_name, 'author_url': author_url, 'works_count': works_count, 'publications': publications})
                print(f"АВТОР: {author_name},  Кількість робіт: {works_count}")
                for publication in publications:
                    print(f"    Рік публікації: {publication['publication_year']}, Назва публікації: {publication['title']}, Співавтори: {', '.join(publication['authors'])}")
            else:
                print(f"Автор: {author_name},  Кількість робіт: {works_count}, No publications found")
            time.sleep(1)  # Затримка на 1 секунду, щоб не навантажувати сервер
    except Exception as e:
        print("Помилка при отриманні списку авторів та їх робіт:", e)
    return authors_and_works


def save_to_xml(data):
    try:
        root = ET.Element('library')

        for entry in data:
            author_elem = ET.SubElement(root, 'author')
            name_elem = ET.SubElement(author_elem, 'name')
            name_elem.text = entry['author_name']
            url_elem = ET.SubElement(author_elem, 'url')
            url_elem.text = entry['author_url']
            works_elem = ET.SubElement(author_elem, 'works_count')
            works_elem.text = entry['works_count']
            publications_elem = ET.SubElement(author_elem, 'publications')
            for publication in entry['publications']:
                publication_elem = ET.SubElement(publications_elem, 'publication')
                year_elem = ET.SubElement(publication_elem, 'publication_year')
                year_elem.text = publication['publication_year']
                title_elem = ET.SubElement(publication_elem, 'title')
                title_elem.text = publication['title']
                authors_elem = ET.SubElement(publication_elem, 'authors')
                authors_text = ', '.join(publication['authors'])
                authors_elem.text = authors_text

        tree = ET.ElementTree(root)
        tree.write('authors_and_works.xml', encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print("Помилка при збереженні даних у файл XML:", e)

# Основна функція
def main():
    base_url = 'https://dspace.uzhnu.edu.ua/jspui/handle/123456789/43/browse?type=author&order=ASC&rpp=20&offset='
    total_pages = 10  # є ніби  10 сторінок з авторами та їх роботами

    all_authors_and_works = []

    for page_num in range(total_pages):
        offset = page_num * 20  # По 20 елементів на сторінку
        url = base_url + str(offset)
        authors_and_works = get_authors_and_works(url)
        all_authors_and_works.extend(authors_and_works)

    save_to_xml(all_authors_and_works)

if __name__ == "__main__":
    main()
