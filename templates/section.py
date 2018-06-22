'''
Prints top 50 ranked baseball players with
associated text
'''

from bs4 import BeautifulSoup
import urllib.request


def findSection():
    '''
    :param word: word to look for in the website
    :return: section ids of where the desired word is located
    '''
    response = urllib.request.urlopen("http://localhost:8080/sports").read()
    soup = BeautifulSoup(response, "lxml")
    title = soup.title.text

    sectionList = []  # Holds list of sections that the word is in
    pTags = soup.find_all("p") #finds all p tags

    for i in range(len(pTags)):
        if pTags[i].text.find("Bangladesh") >= 0:
            parent = pTags[i].find_parent()
            sectionID = parent['id']
            #print(sectionID)
            sectionList.append(sectionID)

    return sectionList

findSection()
print(findSection())