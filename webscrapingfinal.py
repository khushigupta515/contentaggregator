import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule 
import time 

conn = sqlite3.connect('scraping.db')

def takingemailidfromtheuser():
  name=input("Enter name\n")
  mailid=input("Enter e-mail id\n")

def wesite1scraped():
    conn.execute('''CREATE TABLE if not exists tablenew
                (counter int,date text)''')
    count=0
    finalstr=""
    for j in range(3):    
        url = "http://quotes.toscrape.com/tag/love/page/{}/".format(j)
        stuff = requests.get(url)
        soup = BeautifulSoup(stuff.content)
        firstQuote = soup.findAll("span",attrs={"class","text"})
        for i in range(len(firstQuote)):
            count+=1
            k=firstQuote[i].text
            ar=[count,k]
            conn.execute("INSERT INTO tablenew VALUES (?,?)",ar)
        print("LOVE QUOTES FROM quotes.toscrape.com")    
        for row in conn.execute('SELECT * FROM tablenew'):   
            print(row)
            finalstr=finalstr+"\n"+row[1]
        conn.commit()
def scrapeBooks(url,count=1,urlNum=1):
    conn.execute('''CREATE TABLE if not exists table2
                (data1 text,data2 text)''')
    bookInfo = requests.get(url)
    soup2 = BeautifulSoup(bookInfo.content)
    anotherSoup = soup2.findAll("li",attrs={"class", "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    for i in range(len(anotherSoup)):
        print(count,')', 'Title: ',  anotherSoup[i].h3.a['title'])
        print('    Price:',anotherSoup[i].find('p',attrs='price_color').text)
        print()
        title1=anotherSoup[i].h3.a['title']
        price1=anotherSoup[i].find('p',attrs='price_color').text
        ar=[title1,price1]
        conn.execute("INSERT INTO table2 VALUES (?,?)",ar)
        conn.commit() 
        count+=1
    if(len(soup2.findAll('li',attrs={'class','next'}))==1):
        if urlNum>1:
            url="http://books.toscrape.com/catalogue/"+soup2.findAll('li',attrs={'class','next'})[0].a['href']
            print('---- URL Being Scraped ---- ')
            print(url)
            print('--------------------------')
            print()
            scrapeBooks(url,count,urlNum)
        else:
            url="http://books.toscrape.com/"+soup2.findAll('li',attrs={'class','next'})[0].a['href']
            print('---- URL Being Scraped ---- ')
            print(url)
            print('---------------------------')
            print()
            urlNum+=1
            scrapeBooks(url,count,urlNum)         


 



takingemailidfromtheuser()        
wesite1scraped()
url = "http://books.toscrape.com/"          
scrapeBooks(url)
lambda : scrapeBooks(url)
schedule.every().day.at("00:00").do(wesite1scraped)
schedule.every().day.at("00:00").do(lambda : scrapeBooks(url))

while True: 
    schedule.run_pending() 
    time.sleep(1) 
    
conn.close()   
