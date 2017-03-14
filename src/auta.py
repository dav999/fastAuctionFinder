from lxml import html
from time import gmtime, strftime
import requests
import smtplib
import time


OTOMOTO_URL = 'https://www.otomoto.pl/osobowe/kia/ceed/-/-/kombi/?search%5Bfilter_float_price%3Afrom%5D=25000&search%5Bfilter_float_price%3Ato%5D=35000&search%5Bfilter_float_year%3Afrom%5D=2010&search%5Bfilter_float_mileage%3Ato%5D=150000&search%5Bfilter_float_engine_capacity%3Afrom%5D=1500&search%5Bfilter_float_engine_capacity%3Ato%5D=2000&search%5Bfilter_float_engine_power%3Afrom%5D=100&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_no_accident%5D=1&search%5Bcountry%5D='
MOBILEDE_URL = 'http://www.mobile.de/pl/samochod/kia/lokalizacja/hanower-niemcy/vhc:car,cnt:de,loc:hanower%2C%2C+niemcy,rng:100,srt:date,sro:desc,ms1:13200__,frn:2010,prx:8000,mlx:150000,pwn:74,dmg:false,vcg:estatecar'
otomoto = 999
mobile = 999

def otomotoCars():
    page = requests.get(OTOMOTO_URL)
    tree = html.fromstring(page.content) 
    cars = tree.xpath('//span[@class="counter"]/text()')
    print "OTOMOTO: " + cars[0][1:2]
    return cars[0][1:2]

def mobileDeCars():
    page = requests.get(MOBILEDE_URL)
    tree = html.fromstring(page.content) 
    cars = tree.xpath('//h1[@class="h2 u-text-orange"]/text()')
    print "MOBILEDE: " + cars[0][0:1]
    return cars[0][0:1]

def otomotoNewCar():
    page = requests.get(OTOMOTO_URL)
    tree = html.fromstring(page.content) 
    cars = tree.xpath('//a[@class="offer-title__link"]')
    return cars[0].items()[2][1]

def mobileNewCar():
    page = requests.get(MOBILEDE_URL)
    tree = html.fromstring(page.content) 
    cars = tree.xpath('//a[@class="vehicle-data track-event u-block js-track-event js-track-dealer-ratings"]')
    return "www.mobile.de" + cars[0].items()[6][1]
    
def sendMail(text):
    gmail_user = 'EMAIL_USER'
    gmail_pwd = 'EMAIL_PASSWORD'
    FROM = 'EMAIL_FROM'
    TO = ['EMAIL_TO']
    SUBJECT = 'TITLE'
    TEXT = text

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'Successfully sent the mail'
    except:
        print "Failed to send mail"

while 1:    
    print "Check at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    newOtomoto = int(otomotoCars())
    newMobilede = int(mobileDeCars())
     
    if otomoto < newOtomoto:
        print "NEW CAR IN OTOMOTO!!!"
        sendMail("New car in Otomoto\n" + otomotoNewCar())
     
    if mobile < newMobilede:
        print "NEW CAR IN MOBILEDE!!!"
        sendMail("New car in Mobile.de\n" + mobileNewCar())
     
    otomoto = newOtomoto
    mobile = newMobilede
    print "-----------------"
    time.sleep(30)
    



