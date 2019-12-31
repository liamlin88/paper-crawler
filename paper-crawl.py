from urllib import request
from bs4 import BeautifulSoup
import os

class Paper():
    def __init__(self, authors, title, abstract):
        self.authors = authors
        self.title = title
        self.abstract = abstract

    def __str__(self):
        return str((self.authors, self.title, self.abstract))

    def to_one_line(self):
        return self.title + ','.join(self.authors)

def crawl(url: str) -> str:
    response = request.urlopen(url)    
    return response.read()

def parse(body: str) -> list:
    authors = []
    soup = BeautifulSoup(body, 'html.parser') 
    for div in soup.find_all('div', class_='media-body'):
        authors.append(','.join([h5.text.strip() for h5 in div.find_all('h5')]))
    
    title = soup.find('div', class_='page-header').find('h2').text.strip()
    abstract = soup.find(text='Abstract').parent.parent.p.text.strip()
    paper = Paper(authors, title, abstract) 
    return paper

def write_papers(papers, path):
    with open(path, '+w') as f:
        for paper in papers:
            f.write(paper.to_one_line() + os.linesep)

if __name__ == "__main__":
    i = 50 
    papers = []
    while True:
        try:
            papers.append(parse(crawl("https://pldi19.sigplan.org/details/pldi-2019-papers/{0}".format(str(i)))))
        except:
            break
        i = i + 1 
    
    write_papers(papers, 'output.csv')