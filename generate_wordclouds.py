import pandas as pd
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# Loads the csv file into a dataframe
df = pd.read_csv('data/ArogyaSetuReviews.csv', index_col=False)

# Creates two giant strings of all the reviews with 1 star and 5 star rating
negative = " ".join(
    review for review in df[df["review_star_count"] == 1].review)
positive = " ".join(
    review for review in df[df["review_star_count"] == 5].review)

# Create a list of all the stopwords like the, a, and to eliminate form the cloud
stopwords = set(STOPWORDS)

# Load the mask image and create a wordcloud using it
mask = np.array(Image.open("img/flag.jpg"))

# 5 star reviews
wordcloud_pos = WordCloud(stopwords=stopwords, background_color="white",
                          max_words=1000, mask=mask).generate(positive)

image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[25, 18])
plt.title("5 star Reviews", fontsize=24, y=1.1)
plt.imshow(wordcloud_pos.recolor(
    color_func=image_colors), interpolation="bilinear")
plt.axis("off") # Disables the axis lines

plt.savefig('img/pos.jpg') # Saves the images

# plt.show()

# 1 star reviews
wordcloud_neg = WordCloud(stopwords=stopwords, background_color="white",
                          max_words=1000, mask=mask).generate(negative)

image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[25, 18])
plt.title("1 star Reviews", fontsize=24, y=1.1)
plt.imshow(wordcloud_neg.recolor(
    color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.savefig('img/neg.jpg') # Saves the images

# plt.show()
