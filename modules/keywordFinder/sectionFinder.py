'''
Finds the section id of keywords
'''

from bs4 import BeautifulSoup
import urllib.request


def findSection(url, word):
    '''
    :param word: word to look for in the website
    :return: section ids of where the desired word is located
    '''
    response = urllib.request.urlopen("http://localhost:8080" + url).read()
    soup = BeautifulSoup(response, "lxml")
    title = soup.title.text

    sectionList = []  # Holds list of sections that the word is in
    pTags = soup.find_all("p") #finds all p tags

    for i in range(len(pTags)):
        if (pTags[i].text.find(word) >= 0) or(pTags[i].text.find(word.title()) >= 0): #title to make first letter of word upper case
            parent = pTags[i].find_parent()

            try:
                sectionID = parent['id'] #finds the id of the parent
                #print(sectionID)
                sectionList.append(sectionID)
            except KeyError: #to handle a case where the keyword does not have a parent section id
                pass



    return sectionList

#findSection('cricketers')
#print(findSection('cricketers'))