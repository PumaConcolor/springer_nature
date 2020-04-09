#!/usr/bin/env python
import argparse
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

def get_book_from_database(book: Dict, args: Dict):
    # Extracting book attributes
    title = book['Book Title'].replace('/', '-')
    category = book['English Package Name']
    # Making dirs
    path = join('books', category)
    makedirs(path, exist_ok=True)
    # Creating urls
    path = join(path, title)
    urls = []
    if not args['epub_only']:
        urls.append(
            [
                book['DOI URL'].replace('doi.org', 'link.springer.com/content/pdf') + '.pdf',
                path + '.pdf'
            ]
        )
    if not args['no_epub']:
        urls.append(
            [
                book['DOI URL'].replace('doi.org', 'link.springer.com/download/epub') + '.epub',
                path + '.epub'
            ]
        )
    # Start book download
    print('Downloading', title)
    for url, save in urls:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            with open(save, 'wb') as file:
                file.write(response.content)
    print(title, 'completed')

def get_books_from_database(database: List[Dict], args: Dict):
    database = [
        (book, args)
        for book in database
    ]
    pool = Pool(len(sched_getaffinity(0)))
    data = pool.starmap(get_book_from_database, database)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-epub', action='store_true')
    parser.add_argument('--epub-only', action='store_true')
    args = vars(parser.parse_args())
    database = get_springer_database()
    get_books_from_database(database, args)
    print('### Download completed ###')
