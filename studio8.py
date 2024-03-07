import requests
from bs4 import BeautifulSoup as bs
import time

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags


def main():
    # making request to website
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")


    #myQuotes = (scrapeQuotes(soup))
    quotes = []
    while True:
        #use time delay to not ddos the site
        time.sleep(1)
        relative_url = getNextUrl(soup)

        if relative_url is None:
            break
        next_page = url + relative_url
        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        (scrapeQuotes(soup))
        quotes.extend(scrapeQuotes(soup))


    shortLONG = getShortestAndLongest(quotes)

    myTagsList = getTagsList(quotes)


    q1Output = []
    for tag in myTagsList:
        tagNum = myTagsList.count(tag)
        if [tag, tagNum] not in q1Output:
            q1Output.append([tag, tagNum])

    q1Output.sort(key = lambda x: x[1])
    q1Output.reverse()

    print(q1Output[:10])


    myAuthorsList = getAuthors(quotes)
    

    q4Output = []
    for author in myAuthorsList:
        authorNum = myAuthorsList.count(author)
        if authorNum >1:
            if [author, authorNum] not in q4Output:
                q4Output.append([author, authorNum])

    q4Output.sort(key = lambda x: x[1])
    q4Output.reverse()

    print(q4Output)
    
    return  




    #return gave "Response [200]" which means the request and response worked correctly

def getAuthors(quotes):
    listOfAuthors = []
    for quote in quotes:
        listOfAuthors.append(quote.author)
        
    return listOfAuthors

def getShortestAndLongest(quotes):
    longest = 0
    shortest = 100000000
    longestQuote = ""
    shortestQuote = ""

    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longestQuote = quote.text

        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortestQuote = quote.text

    print(longestQuote, longest)
    print(shortestQuote, shortest)

    return

def getTagsList(quotes):
    listOfTags = []
    for quote in quotes:
        listOfTags.extend(quote.tags)

    return listOfTags


def getNextUrl(soup:bs):
    #find next url
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    urlNext = anchor["href"]

    return urlNext

def scrapeQuotes(soup: bs):
    #pass through "type of container", "class name"
    quotesObjs = []
    quotes = soup.find_all("div", {"class": "quote"})

    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        tags = quote.find_all("a", {"class": "tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))

        quotesObjs.append(Quote(text, author, tags_text))   

    return quotesObjs



if __name__ == "__main__":
    main()



