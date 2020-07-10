import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule 
import time 
import smtplib, ssl

conn = sqlite3.connect('scraping.db')

global finalstr=""

def scrapequotes():
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


global finalstr2=""        
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
        finalstr2=finalstr2+title1+price1+"\n"
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
def sendingdatabasethroughmail():
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  mailid=input("Enter e-mail id\n")
  sender_email = "khushigupta515@gmail.com"  # Enter your address
  receiver_email = mailid # Enter receiver address
  password = input("Type your password and press enter: ")
  message = """\
   Subject: Hi there

   This message is sent from Python."""+finalstr+finalstr2

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


 



       
scrapequotes()
url = "http://books.toscrape.com/"          
scrapeBooks(url)
sendingdatabasethroughmail()
lambda : scrapeBooks(url)
schedule.every().day.at("00:00").do(scrapequotes)
schedule.every().day.at("00:00").do(lambda : scrapeBooks(url))

while True: 
    schedule.run_pending() 
    time.sleep(1) 
    
conn.close()   
