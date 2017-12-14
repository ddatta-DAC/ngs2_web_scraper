import requests
from bs4 import BeautifulSoup
import json


def get_citations(doi):
    url = "http://citeseerx.ist.psu.edu/viewdoc/citations"
    payload = {'doi': doi}

    response = requests.get(url, params=payload)

    if response.status_code != 200:
        print('ERROR code {} for {}'.format(response.status_code, doi))

    soup = BeautifulSoup(response.content, "html.parser")

    citations = []

    for tr in soup.find(id="citations").table.find_all('tr'):
        td = tr.find_all('td')[1]
        attrs = td.a.attrs
        citation = {
            'title': td.a.string,
            'url': attrs['href'],
            'citation_only': 'class' in attrs and 'citation_only' in attrs['class'],
        }

        # hoping that contents[2] will always be the author/year string
        author_year = td.contents[2].string.split() if len(td.contents) > 2 else []

        # [u'-', u'Baumeister,', u'Leary', u'-', u'1995']
        if author_year and author_year[0] == '-':
            next_dash = author_year.index('-', 1) if '-' in author_year[1:] else len(author_year)

            citation['author'] = ' '.join(author_year[1:next_dash])
            if next_dash + 1 < len(author_year):
                citation['year'] = author_year[next_dash + 1]

        context = td.select('p.citationContext')
        if context:
            citation['context'] = context[0].string.strip()

        citations.append(citation)

    return citations


def get_record(doi):
    url = "http://citeseerx.ist.psu.edu/viewdoc/versions"
    payload = {'doi': doi}

    response = requests.get(url, params=payload)

    if response.status_code != 200:
        print('ERROR code {} for {}'.format(response.status_code, doi))

    soup = BeautifulSoup(response.content, "html.parser")

    record = {
        'doi': doi,
        'pdf_url': "http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf".format(doi),
        'authors': [],
    }

    for tr in soup.find_all('tr'):
        if tr.td:
            datum = tr.td.string.lower()

            if datum == "title":
                record['title'] = tr.find_all('td')[1].string
            elif datum == "abstract":
                record['abstract'] = tr.find_all('td')[1].string
            elif datum == "year":
                record['year'] = tr.find_all('td')[1].string
            elif datum == "venue":
                record['venue'] = tr.find_all('td')[1].string
            elif datum == "author name":
                record['authors'].append(tr.find_all('td')[1].string)

    record['citations'] = get_citations(doi)

    print(json.dumps(record))


if __name__ == "__main__":
    get_record('10.1.1.874.7127')
    # get_record('10.1.1.550.47')
