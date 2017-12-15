# Setup :

sudo apt-get install poppler-utils
pip install --user bs4


-------------------------------


# Run Instructions :
python src/scraper_1 {num of pages}  {keyword}
python src/scraper_1.py  10 collective identity



# Metadata scraper

python src/citescraper.py 10.1.1.874.7127

### Sample (abbreviated) output

```
{
  "doi": "10.1.1.874.7127",
  "title": "An organizing framework for collective identity: Articulation and significance of multidimensionality",
  "abstract": "...",
  "pdf_url": "http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.874.7127&rep=rep1&type=pdf",
  "venue": "Psychological Bulletin",
  "authors": [
    "Richard D. Ashmore",
    "Kay Deaux",
    "Tracy Mclaughlin-volpe"
  ],
  "citations": [
    {
      "url": "/showciting?cid=11061",
      "citation_only": true,
      "author": "Goffman",
      "year": "1959",
      "title": "Presentation of Self in Everyday Life"
    },
    {
      "url": "/viewdoc/summary?cid=109950",
      "citation_only": false,
      "title": "The principles of psychology"
    },
  ],
  "year": "2004"
}
```