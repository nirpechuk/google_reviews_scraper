using chrome driver and selenium, searches through a list of boba shops in order to gather information from them and output in an excel spreadsheet. 

### BELOW: test snippet to try out new scrapings before running on large scale

url = "https://www.yelp.com/biz/99-tea-house-fremont-3"

driver.get(url)

page_content = driver.page_source

response = Selector(page_content)

testparameter = response.xpath('.//div[contains(@data-hypernova-hydration-status,"1")]/div[4]/div/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[1]/p[2]/text()').extract_first('')

print(testparameter)