from bs4 import BeautifulSoup  # requires PIP install: pip install bs4
import urllib.request

"""
    website:    FULL website URL for scraping (http:// included automatically)
    ex:
    www.ky3.com/content/news/Police-investigating-a-suspicious-death-in-north-Springfield-478493043.html
    
    Uses a best guess to find the main article in a news site and then parses it into a list
    Based on the idea that the division tag with the most paragraph tags has the highest probability to be the main article
    
    Returns getKeyWords(), which returns a list of keywords
    
    Example use:
        keyWordsForMe = getKeys(websiteURL)
        keyWordsForMe = [key1, ..., keyN]
"""


def getKeys(website):
    IGNORELIST = "modules/keywordFinder/IgnoredWords.txt"

    # request = urllib.request.Request(website, None, headers)

    response = urllib.request.urlopen(website).read()
    soup = BeautifulSoup(response, "html.parser")
    # deletes the reference, urllib cleans up after itself when there is no reference
    del response

    divs = soup.body.find_all("div")  # list of all div tags in html

    # find the <div> with the most <p> tags. Main algorithm in method
    tagMax = 0
    iter = 0
    bestDiv = 0
    # count the p tags in each div
    for div in divs:
        pTags = div.find_all('p')
        tagCount = 0

        for tag in pTags:
            tagCount += 1
        # keep running tally of most p tags
        if (tagCount > tagMax):
            tagMax = tagCount
            bestDiv = iter
        iter += 1

    # start with the title and then append bestDiv to articleText
    articleText = soup.title.string
    """
        para.attrs returns all the attributes for the tag in para
        it looks for p tags with no class, to hopefully stop inline ads
    """
    for para in (divs[bestDiv].find_all('p')):
        if 'class' not in para.attrs:
            articleText += para.get_text()

    ignoreList = readFile(IGNORELIST)

    # print(articleText)
    return getKeyWords(articleText.split(), ignoreList)


"""
    words:      list of words in an article
    ignoreMe:   list of words in a stop word list
    
    Finds the most frequently used words while ignoring commonly used words
        Variable number of keywords dependent on article size
    
    Returns a list of keywords with variable size
"""


def getKeyWords(words, ignoreList):
    MINKEYS = 4  # Minimum number of keys to return
    MAXKEYS = 10  # Maximum number of keys to return

    keyWords = []
    punctuation = ['.', ',', '!', '(', ')', '?', '"', '-', '\n', '\r']
    # 1 keyword per 250 words in article
    keyNum = int(len(words) / 250)
    # minimum of 5 keywords per article
    if keyNum < MINKEYS:
        keyNum = MINKEYS

    for i in range(len(words)):
        word = words[i]
        # Strip punctuation from the words first
        word = ''.join(c for c in word if c not in punctuation).lower()
        words[i] = word
        # puts one version of each word into keyWords
        if word not in ignoreList and word not in keyWords:
            keyWords.append(word)

    counts = []
    # counts occurrences
    for key in keyWords:
        count = 0
        for word in words:
            if word == key:
                count += 1
        counts.append((count, key))

    counts.sort()
    counts.reverse()

    keywordsFinal = []
    # prints them
    for i in range(min(min(keyNum, len(counts)), MAXKEYS)):
        count, word = counts[i]
        keywordsFinal.append(word)

    return keywordsFinal


"""
    Takes filename string
    Returns list of things in file
    Simple file reader
"""


def readFile(input_filename):
    with open(input_filename, 'r', encoding="utf-8") as array_file:
        array_data = [str(val) for val in array_file.read().split()]
    return array_data
