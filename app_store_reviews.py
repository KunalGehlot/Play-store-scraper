from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd

names = []
star_texts = []
star_numbers = []
review_dates = []
helpful_counts = []
review_texts = []
review = ''

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome()
link = "https://play.google.com/store/apps/details?id=nic.goi.aarogyasetu&showAllReviews=true"
driver.get(link)
driver.maximize_window()
sleep(2)

for i in range(30):
    showMore = driver.find_elements_by_xpath("//span[text()='Show More']")
    if(showMore):
        showMore[0].click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(0.5)

for _ in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(0.5)

driver.execute_script("window.scrollTo(0, 0)")

buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Full Review')]")
for b in buttons:
    b.click()

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

appName = soup.h1.span.text
print("Application Name: ", appName)

userNameBlocks = soup.find_all('div', class_='xKpxId zc7KVe')

print("Number of reviews = ", len(userNameBlocks))

for user in userNameBlocks:
    poster_name = user.find('span', class_='X43Kjb').text
    names.append(poster_name)

    rating = user.find('div', class_='pf5lIe').findAll('div')

    rating_text = rating[0]
    rating_text = rating_text.get_attribute_list("aria-label")[0]
    rating_number = rating_text[6]

    star_texts.append(rating_text)
    star_numbers.append(rating_number)

    rating_date = user.find('span', class_="p2TkOb").text
    review_dates.append(rating_date)

    helpful_count = user.find("div", class_="jUL89d y92BAb").text
    helpful_counts.append(helpful_count)

reviews = soup.select('div.UD7Dzf > span')

count = 0

while count < len(reviews):
    short_review = reviews[count].get_text(strip=True)
    count += 1
    if count == len(reviews):
        break
    long_review = reviews[count].get_text(strip=True)
    if len(short_review) != 0:
        review = short_review
    if len(long_review) != 0:
        review = long_review
    count += 1
    review_texts.append(review)

min_length = min(len(names), len(review_dates), len(star_texts), len(
    star_numbers), len(helpful_counts), len(review_texts))
print("The minimum length out of all features is ", min_length)

d = {}
d["reviewer_name"] = names[0:min_length-1]
d["review_date"] = review_dates[0:min_length-1]
d["review_star_text"] = star_texts[0:min_length-1]
d["review_star_count"] = star_numbers[0:min_length-1]
d["review_helpful_count"] = helpful_counts[0:min_length-1]
d["review"] = review_texts[0:min_length-1]

print("Length of each feature is: ")
for key, value in d.items():
    print(len(value))

df = pd.DataFrame(data=d)
print(df.shape)

df.to_csv("data/ArogyaSetuReviews.csv", index = False)