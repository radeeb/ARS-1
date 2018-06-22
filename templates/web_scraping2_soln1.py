'''
Prints top 50 ranked baseball players with
associated text
'''

from bs4 import BeautifulSoup
import csv

def readfile(fname):
    f = open(fname, 'r', encoding = "utf8")
    text = f.read()
    f.close()
    return text

def main():
    webfile = "mlbtop50.html"
    text = readfile(webfile)
    soup = BeautifulSoup(text, "lxml")
    title = soup.title.text
    print(title)
    players = soup.find_all("h2")
    for i in range(len(players)):
        if players[i].text.find("No. 50:") >= 0:
            break
    for p in players[i:]:
        print(p.text)
        sibs = p.next_siblings
        for s in sibs:
            if s.name == 'p':
                t = s.text
                t = t.replace("Did you know? ", '')
                print(t)
            elif s.name == "h2":
                print()
                break

main()
