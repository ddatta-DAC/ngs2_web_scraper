import argparse
import requests
from bs4 import BeautifulSoup
import json
from urlparse import urlparse, parse_qs


class Citation():
    def __init__(self, tr):
        """Take a BeautifulSoup Tag for a tr in the citation list table."""
        td = tr.find_all('td')[1]
        attrs = td.a.attrs

        self.title = td.a.string
        self.url = attrs['href']
        self.citation_only = 'class' in attrs and 'citation_only' in attrs['class']

        # hoping that contents[2] will always be the author/year string
        author_year = td.contents[2].string.split() if len(td.contents) > 2 else []

        # [u'-', u'Baumeister,', u'Leary', u'-', u'1995']
        if author_year and author_year[0] == '-':
            next_dash = author_year.index('-', 1) if '-' in author_year[1:] else len(author_year)

            self.author = ' '.join(author_year[1:next_dash])
            self.year = author_year[next_dash + 1] if next_dash + 1 < len(author_year) else None

        context = td.select('p.citationContext')
        if context:
            self.context = context[0].string.strip()

    def follow(self):
        if not self.citation_only:
            cid = cid_from_url(self.url)
            return Record(cid, identifier_key="cid")


def doi_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['doi'][0] if 'doi' in qs and qs['doi'] else None


def cid_from_url(url):
    qs = parse_qs(urlparse(url).query)
    return qs['cid'][0] if 'cid' in qs and qs['cid'] else None


class Record():
    def __init__(self, identifier, identifier_key="doi"):
        """Fetch a record.

        identifier_key can be "doi" or "cid"
        identifier is the actual doi or cid identification number
        """
        url = "http://citeseerx.ist.psu.edu/viewdoc/versions"
        payload = {identifier_key: identifier}

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            print('ERROR code {} for {}'.format(response.status_code, doi))

        soup = BeautifulSoup(response.content, "html.parser")

        self.doi = doi_from_url(response.url)
        self.pdf_url = "http://citeseerx.ist.psu.edu/viewdoc/download?doi={}&rep=rep1&type=pdf".format(self.doi)
        self.authors = []

        for tr in soup.find_all('tr'):
            if tr.td:
                datum = tr.td.string.lower()

                if datum == "title":
                    self.title = tr.find_all('td')[1].string
                elif datum == "abstract":
                    self.abstract = tr.find_all('td')[1].string
                elif datum == "year":
                    self.year = tr.find_all('td')[1].string
                elif datum == "venue":
                    self.venue = tr.find_all('td')[1].string
                elif datum == "author name":
                    self.authors.append(tr.find_all('td')[1].string)

        self.citations = self.get_citations(self.doi)

    def get_citations(self, doi):
        url = "http://citeseerx.ist.psu.edu/viewdoc/citations"
        payload = {'doi': doi}

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            print('ERROR code {} for {}'.format(response.status_code, doi))

        soup = BeautifulSoup(response.content, "html.parser")

        citations = []

        for tr in soup.find(id="citations").table.find_all('tr'):
            c = Citation(tr)
            citations.append(c)

        return citations

    def toJSON(self):
        obj = self.__dict__
        obj['citations'] = [c.__dict__ for c in obj['citations']]
        return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("doi", help="A DOI for a paper on CiteSeerX (e.g. 10.1.1.874.7127)")
    args = parser.parse_args ()

    record = Record(args.doi)

    # record = Record('10.1.1.874.7127')
    # record = get_record('10.1.1.550.47')
    # record = get_record('10.1.1.10.3979')
    print(json.dumps(record.toJSON()))
