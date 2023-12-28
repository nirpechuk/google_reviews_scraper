from random import random
from time import sleep
from parsel import Selector
from selenium import webdriver
import csv

# set up chrome driver
chromedrive_path = './chromedriver.exe'
driver = webdriver.Chrome(chromedrive_path)

# 24 hour time
def timeConversion(s):
   if s[-2:] == "AM":
      if s[:2] == '12':
          a = str('00' + s[2:8])
      else:
          a = s[:-2]
   else:
      if s[:2] == '12':
          a = s[:-2]
      else:
          a = str(int(s[0:1]) + 12) + ":" + s[2:4]
   return a

# BELOW: test snippet to try out new scrapings before running on large scale
#
# url = "https://www.yelp.com/biz/99-tea-house-fremont-3"
# driver.get(url)
# page_content = driver.page_source
# response = Selector(page_content)
# testparameter = response.xpath('.//div[contains(@data-hypernova-hydration-status,"1")]/div[4]/div/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[1]/p[2]/text()').extract_first('')
# print(testparameter)

# main code


with open('MOREBOBA.csv', 'w', newline='') as outcsvfile:
    with open("bobalist.csv", newline='') as incsvfile:
        # set up csv reading and writing
        bobafile = csv.DictReader(incsvfile)
        fieldnames = ['num', 'id', 'name', 'rating', 'address', 'city', 'lat', 'long','yelpcost','websiteprovided','yelpphone','url']
        writer = csv.DictWriter(outcsvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in bobafile:
            # search the term and get the page content

            # google
            # searchTerm = row['name'].replace(' ', '+').replace('&', '%26') + '+' + (
            #     row['city'].replace(' ', '+')) + '+ca+' + row['address'].replace(' ','+')
            # url = "https://www.google.com/search?q=" + searchTerm

            # yelp
            url = "https://www.yelp.com/biz/" + row['id']
            driver.get(url)
            page_content = driver.page_source
            response = Selector(page_content)

            # scrape values by finding an anchor and the xpath from there

            # google
            # starRating = response.xpath(
            #     './/div[contains(@data-attrid,"kc:/collection/knowledge_panels/local_reviewable:star_score")]/div/div/span[1]/text()').extract_first(
            #     '')
            # if starRating == '':
            #     starRating = response.xpath(
            #         '/html/body/div[7]/div/div[10]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div/span[1]/text()').extract_first(
            #         '')
            #
            # numReviews = response.xpath('.//a[contains(@data-async-trigger,"reviewDialog")]/span/text()').extract_first('').replace(" Google reviews","")
            # if numReviews == '':
            #     numReviews = '0'
            #
            # serviceOptions = response.xpath('.//div[contains(@data-attrid,"kc:/local:business_availability_modes")]/c-wiz/div/text()').extract_first('').replace(' · ',',')
            # if serviceOptions == '':
            #     serviceOptions = "No data"
            #
            # dollarSigns = response.xpath('.//div[contains(@data-attrid,"kc:/local:one line summary")]/div/span[1]/span/text()').extract_first('')
            # if dollarSigns == '':
            #     dollarSigns = 'No data'

            # yelp

            # numReviews = response.xpath(
            #     './/div[contains(@data-testid,"photoHeader")]/div[1]/div[1]/div/div/div[2]/div[2]/span/text()').extract_first(
            #     '').replace(" reviews", "")
            #
            # hoursOpen = response.xpath('.//section[contains(@aria-label,"Location & Hours")]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[1]/ul/li/p/text()').extract_first('').replace(" ","").split("-")
            # print(hoursOpen[0])
            #
            #
            # if hoursOpen[0] == '':
            #     opening,closing = '',''
            # elif hoursOpen[0] == 'Closed':
            #     opening,closing = 'Closed','Closed'
            # else:
            #     opening = timeConversion(hoursOpen[0])
            #     closing = timeConversion(hoursOpen[1])

            cost = response.xpath('.//div[contains(@data-testid,"photoHeader")]/div[1]/div[1]/div/div/span[2]/span/text()').extract_first('')

            website = response.xpath('.//span[contains(@class,"icon--24-external-link-v2 icon__09f24__zr17A css-147xtl9")]/../../../div[1]/p[2]/a/text()').extract_first('')
            if website == '':
                website = 'False'
            else:
                website = 'True'

            phone = response.xpath('.//span[contains(@class,"icon--24-phone-v2 icon__09f24__zr17A css-147xtl9")]/../../div[1]/p[2]/text()').extract_first('')
            if phone == '':
                phone = 'None Provided'


            # write in the new values to a csv
            print(cost, website, phone, url)

            writer.writerow({'num': row['num'],
                             'id': row['id'],
                             'name': row['name'],
                             'rating': row['rating'],
                             'address': row['address'],
                             'city': row['city'],
                             'lat': row['lat'],
                             'long': row['long'],
                             'yelpcost': cost,
                             'websiteprovided': website,
                             'yelpphone': phone,
                             'url': url})

            # evade google bot prevention
            sleep(random() * 10)