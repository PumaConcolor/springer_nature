# Springer Nature Free Books

## Description
This Python script download simultaneously all books listed in https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4 , both in PDF or Epub (if available).

## Usage
Install the required dependencies:  

    pip install -r requirements.txt

Start the parallel download of pdf and epub:

    python main.py

To select no epub format:

    python main.py --no-epub

To select only epub format:

    python main.py --epub-only

## Reference
https://www.springernature.com/gp/librarians/news-events/all-news-articles/industry-news-initiatives/free-access-to-textbooks-for-institutions-affected-by-coronaviru/17855960