#!/usr/bin/env python
import requests
import pandas as pd
from os import makedirs, sched_getaffinity
from os.path import join
from typing import Dict, List
from multiprocessing import Pool


def get_springer_database(
        url: str = 'https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4'
    ) -> List[Dict]:
    database = pd.read_excel(url)
    database = list(database.T.to_dict().values())
    return database

def get_book_from_database(book: Dict):
    # Extracting book attributes
    title = book['Book Title']
    category = book['English Package Name']
    # Making dirs
    path = join('books', category)
    makedirs(path, exist_ok=True)
    # Creating urls
    exts = ['pdf', 'epub']
    urls = book['DOI URL']
    urls = [
        (
            urls.replace('doi.org', 'link.springer.com/content/' + ext),
            join(path, title) + '.' + ext
        )
        for ext in exts
    ]
    # Start book download
    print('Downloading', title)
    for url, save in urls:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save, 'wb') as file:
                file.write(response.content)
    print(title, 'completed')

def get_books_from_database(database: List[Dict]):
    pool = Pool(len(sched_getaffinity(0)))
    data = pool.map(get_book_from_database, database)
    pool.close()
    pool.join()


if __name__ == '__main__':
    database = get_springer_database()
    get_books_from_database(database)
    print('### Download completed ###')
