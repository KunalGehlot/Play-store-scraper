from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd

# declare all the variables to store the data
names = []
star_texts = []
star_numbers = []
review_dates = []
helpful_counts = []
review_texts = []
review = ''

# luanch a chrome instance
driver = webdriver.Chrome()
link = "https://play.google.com/store/apps/details?id=nic.goi.aarogyasetu&showAllReviews=true"
driver.get(link)
driver.maximize_window() # maximize the window
sleep(2) # wait for the page to load

# a loop to scroll down and load all reviews
for i in range(30):
    showMore = driver.find_elements_by_xpath("//span[text()='Show More']")
    if(showMore): # if a `SHOW MORE` button is encountered, then click on it
        showMore[0].click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # scroll to the bottom of the page
    sleep(0.5) # wait for content to load

for _ in range(4): # scroll one last time till the show more is reached
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(0.5)

driver.execute_script("window.scrollTo(0, 0)") # scroll to top 

buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Full Review')]") # click on every `Full Review button`
for b in buttons:
    b.click()

# Load the HTML of the page
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

appName = soup.h1.span.text # Print the application name
print("Application Name: ", appName)

userNameBlocks = soup.find_all('div', class_='xKpxId zc7KVe') # Find all the block of each review

print("Number of reviews = ", len(userNameBlocks))

for user in userNameBlocks: # Loop through all the blocks
    poster_name = user.find('span', class_='X43Kjb').text
    names.append(poster_name) # Save the User Name

    rating = user.find('div', class_='pf5lIe').findAll('div') # Find the Ratings

    # Save the ratings text and number
    rating_text = rating[0]
    rating_text = rating_text.get_attribute_list("aria-label")[0]
    rating_number = rating_text[6] 
    star_texts.append(rating_text)
    star_numbers.append(rating_number)

    # Save the date of rating
    rating_date = user.find('span', class_="p2TkOb").text
    review_dates.append(rating_date)

    # Save the number of times the review was marked helpful (can be used to find the popular sentiment)
    helpful_count = user.find("div", class_="jUL89d y92BAb").text
    helpful_counts.append(helpful_count)

reviews = soup.select('div.UD7Dzf > span')

count = 0

# Loop through all the reviews as the page saves a long and a short review
while count < len(reviews):
    short_review = reviews[count].get_text(strip=True)
    count += 1
    if count == len(reviews):
        break
    long_review = reviews[count].get_text(strip=True)
    if len(short_review) != 0:
        review = short_review
    if len(long_review) != 0: # Saves the longer version of the review if it exists
        review = long_review
    count += 1
    review_texts.append(review) # Saves the review

# To check if all the features are of the same length (No missing data)
min_length = min(len(names), len(review_dates), len(star_texts), len(
    star_numbers), len(helpful_counts), len(review_texts))
print("The minimum length out of all features is ", min_length)

# Creates a dictionary of all the data
d = {}
d["reviewer_name"] = names[0:min_length-1]
d["review_date"] = review_dates[0:min_length-1]
d["review_star_text"] = star_texts[0:min_length-1]
d["review_star_count"] = star_numbers[0:min_length-1]
d["review_helpful_count"] = helpful_counts[0:min_length-1]
d["review"] = review_texts[0:min_length-1]

# Prints the length of each Key to make sure no data is lost
print("Length of each feature is: ")
for key, value in d.items():
    print(len(value))

# Saves the data to a dataframe
df = pd.DataFrame(data=d)
print(df.shape)

# Saves the data to the csv file
df.to_csv("data/ArogyaSetuReviews.csv", index = False)