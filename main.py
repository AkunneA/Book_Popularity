"""Aspen Akunne
Python Programming

Python Project: Creating Files to Examine Popularity of Books NYT V.S GoodReads community

 New York Times Bestseller List Source:
  https://data.world/typhon/new-york-times-bestsellers-from-2011-to-2018
  Author: Michael Tauberg @typhon
 """

import pandas as pd  # for dealing with dataframes/exporting csv file
import datetime as dt  # for converting the Best Seller data to a datetime for manipulation
import operator  # to handle a problem with sorting by week in bestseller data
import io

def printdict(name, dict, year):  # opens a file and prints a dictionary to the file
    myFile = io.open(f'{name}_{year}.txt', mode="a",encoding="utf-8") #fixes a weird bug with certain titles not being UTF-8 encoded

    for key in dict.keys():
        # print(key)
        myFile.write(f'{key}\n')
    myFile.close()


def goodreaddata():  # calls up the GoodReads list we create with the grabGoodRead program to turn into a list
    secondauthorlist = []
    secondtitlelist = []
    ranklist = []
    yearlist = []
    goodReadList = []

    goodRead = pd.read_csv("GoodReads_Most_Popular_Books_Published_In_2011_2018.csv")

    for y in goodRead['Year']:
        yearlist.append(y)

    for tt in goodRead['Name']:
        secondtitlelist.append(tt)

    for at in goodRead['Author']:
        secondauthorlist.append(at)

    for r in goodRead['Rank']:
        ranklist.append(r)

    lentwo = len(secondtitlelist)

    for gdr in range(lentwo):
        goodReadList.append([ranklist[gdr], secondtitlelist[gdr], secondauthorlist[gdr], yearlist[gdr]])

    return goodReadList


def nytdata():  # creates a list of lists from NYT BestSeller data
    titlelist = []
    authorlist = []
    weeksonlist = []
    datelist = []
    bestsellerlist = []
    goodReadList = []

    books = pd.read_csv("books_uniq_weeks.csv")

    for d in books['date']:
        datelist.append(dt.datetime.strptime(d, '%m/%d/%y').date())

    for t in books['title']:
        titlelist.append(t)

    for a in books['author']:
        authorlist.append(a)

    for w in books['weeks_on_list']:
        weeksonlist.append(w)

    length = len(titlelist)

    for bst in range(length):
        bestsellerlist.append([titlelist[bst], authorlist[bst], datelist[bst], weeksonlist[bst]])

    bestsellerlist.sort(key=operator.itemgetter(3))  # puts books inorder based on weeksonlist

    return bestsellerlist


def main(choice):  # the main program is here
    bestsellerlist = nytdata()
    bestlen = len(bestsellerlist)

    goodReadList = goodreaddata()
    goodlen = len(goodReadList)

    a_dict = {} #I do not want mutiple occurances of the same author or not on list title, so dictionaries are used
    b_dict = {}

    if int(choice) == 1:  # choice one finds the same book and prints that with Rank and Weeks on List to file
        year = input("Enter a year: 2011-2018")
        myFile = open(f'Comparison_{year}.txt', "w")

        for chk in range(bestlen):
            bookYear = bestsellerlist[chk][2].strftime(
                "%Y")  # strftime(" ")->%Y=year, %M=monthnum, %W=weekday %A=day of week %B=month
            if bookYear == f'{year}':
                for gr in range(goodlen):
                    bestTitle = bestsellerlist[chk][0]
                    bestWeeks = bestsellerlist[chk][3]
                    bestAuthor = bestsellerlist[chk][1]

                    goodTitle = goodReadList[gr][1].upper()
                    goodRank = goodReadList[gr][0]
                    goodReadYear = goodReadList[gr][3]

                    if goodReadYear == int(year) and bestTitle == goodTitle:
                        myFile.write(f'{bestTitle} By: {bestAuthor}\n')
                        myFile.write(f'[ GoodReads Rank:{goodRank} Weeks on Bestseller List: {bestWeeks}]\n')
        myFile.close()


    elif int(choice) == 2:  # choice two checks for books not on list and prints them separately to file
        year = input("Enter a year: 2011-2018")
        for chk in range(bestlen):
            bookYear = bestsellerlist[chk][2].strftime("%Y")
            if bookYear == f'{year}':
                for gr in range(goodlen):

                    goodReadYear = goodReadList[gr][3]
                    bestNotTitle = bestsellerlist[chk][0]
                    goodNotTitle = goodReadList[gr][1].upper()

                    if goodReadYear == int(year) and bestNotTitle != goodNotTitle:
                        a_dict[f"{goodNotTitle}"] = chk
                        b_dict[f"{bestNotTitle}"] = chk

        printdict("GoodReadList_NotOn", a_dict, year)
        printdict("NYT_Bestseller_NotOn", b_dict, year)


    elif int(choice) == 3:  # prints most recurring Authors to file
        year = input("Enter a year: 2011-2018")
        for chk in range(bestlen):
            bookYear = bestsellerlist[chk][2].strftime("%Y")
            if bookYear == f'{year}':
                for gr in range(goodlen):

                    goodReadYear = goodReadList[gr][3]
                    bestAuthor = bestsellerlist[chk][1]
                    goodReadAuthor = goodReadList[gr][2]

                    if goodReadYear == int(year) and bestAuthor == goodReadAuthor:
                        b_dict[f"{goodReadList[gr][2]}"] = chk

        printdict("Recurring_Authors", b_dict, year)


    elif int(choice) == 4:
       exit(0)


if __name__ == "__main__":
    going = True #will make while keep going
    while going:
        choice = input("""Select a choice: 
                         1: Same Book
                         2: Books Not On Each Other's List
                         3: Recurring Authors
                         4: Quit \n""")

        main(choice)
