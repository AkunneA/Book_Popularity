"""Aspen Akunne
Python Programming

Python Project: Creating a Webscraper that takes data from GoodRead's popular_by_date_page"""

from bs4 import BeautifulSoup #for grabbing html files
import pandas as pd #for dealing with dataframes/exporting csv file
import requests #grabbing from a url for Webscraping

year=input("Enter Year(2011-2018)") #gets input for year

if int(year)<2011 or int(year)>2018:  #ends if year is wrong
    raise Exception(f'Wrong Year {year}')

html_text=requests.get(f'https://www.goodreads.com/book/popular_by_date/{year}').text #gets year's bestseller page
soup=BeautifulSoup(html_text,"html.parser") #grabs all of the html text
soup.prettify(); #organizes the html
books=soup.find_all('a',class_="bookTitle") #gets book title class
author=soup.find_all('a',class_="authorName") #grabs author name class
good_Read={"Name":[], "Author":[],"Year":[]} #a list of a list that holds the name, author, and year

for i in range(len(books)): #adds title, author, etc to list
    title = books[i].find('span').get_text()
    created = author[i].find('span').get_text()
    good_Read["Name"].append(title)
    good_Read["Author"].append(created)
    good_Read["Year"].append(year)

#print(good_Read) #for printing/testing purposes
df=pd.DataFrame(good_Read) #creates pandas DataFrame
df.to_csv('GoodReads_Most_Popular_Books_Published_In_2011_2018.csv', mode='a', header=False) #new CSV or appends


