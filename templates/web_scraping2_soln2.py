'''
Saves information for top 50-ranked baseball
players in a csv file
'''
from bs4 import BeautifulSoup
import csv

class Player:
    def __init__(self, hdr):
        self.hdr = hdr
        self.text = ''

    def add_text(self, txt):
        if txt.find("ZiPS") >= 0:
            self.zips = txt
        elif txt.find("2017 rank:") >= 0:
            self.last_rank = txt
        else:
            self.text += txt

def readfile(fname):
    f = open(fname, 'r', encoding = "utf8")
    text = f.read()
    f.close()
    return text

def writecsv(fname, lines):
    f = open(fname, 'w', newline = '')
    writer = csv.writer(f)
    writer.writerows(lines)
    f.close()
    print("Wrote", len(lines), "lines")

def show_players(plist, rev=True):
    plist2 = plist[:]  #Make a copy so plist is not modified
    if rev:
        plist2.reverse()
    for p in plist2:
        print(p.hdr)
        print(p.last_rank)
        print(p.zips)
        print(p.text)
        print()

def build_lines(plist, heading):
    '''Returns a list of lines for output and a dictionary of player
       counts for each team'''
    lines = [heading]
    pcounts = {}
    for p in plist:
        info = p.hdr.replace(":", ',')  #Sub ',' for ':' for split(',')
        rank, name, pos, team = info.split(',')
        colonpos = p.last_rank.find(':')
        rk = p.last_rank[colonpos+1:].strip()  #last year's rank
        colonpos = p.zips.find(':')
        zips = p.zips[colonpos+1:].strip()  #zips projection
        outline = [rank.strip(), name.strip(), pos.strip(), team.strip(),
                   rk, zips]
        if team not in pcounts:
            pcounts[team] = 0
        pcounts[team] += 1
        lines.append(outline)
    return lines, pcounts

def show_pcounts(pcounts):
    pclist = []
    for team in pcounts:
        pclist.append((pcounts[team], team))
    pclist.sort()
    pclist.reverse()
    for team in pclist:
        print(team[1], team[0])

def main():
    webfile = "mlbtop50.html"
    fname_out = "mlbtop50.csv"
    text = readfile(webfile)
    soup = BeautifulSoup(text, "lxml")
    title = soup.title.text
    print(title)
    plist = []  #Holds list of Player objects
    players = soup.find_all("h2")
    for i in range(len(players)):
        if players[i].text.find("No. 50:") >= 0:
            break
    for p in players[i:]:
        newp = Player(p.text)
        sibs = p.next_siblings
        for s in sibs:
            if s.name == 'p':
                t = s.text
                t = t.replace("Did you know? ", '')
                newp.add_text(t)
            elif s.name == "h2":
                break
        plist.append(newp)
    #show_players(plist)
    toprow = ["Rank","Name","Pos","Team","LastYr","ZiPS"]
    outlines, player_counts = build_lines(plist, toprow)
    writecsv(fname_out, outlines)
    show_pcounts(player_counts)
    
main()
