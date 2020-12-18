import pandas as pd
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

df = pd.read_csv('ArogyaSetuReviews.csv', index_col=False)

negative = " ".join(
    review for review in df[df["review_star_count"] == 1].review)
positive = " ".join(
    review for review in df[df["review_star_count"] == 5].review)

stopwords = set(STOPWORDS)

mask = np.array(Image.open("img/flag.jpg"))
wordcloud_pos = WordCloud(stopwords=stopwords, background_color="white",
                          max_words=1000, mask=mask).generate(positive)

image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[25, 18])
plt.title("Positive Reviews", fontsize=24, y=1.1)
plt.imshow(wordcloud_pos.recolor(
    color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.savefig('img/pos.jpg')

# plt.show()

mask = np.array(Image.open("img/flag.jpg"))
wordcloud_neg = WordCloud(stopwords=stopwords, background_color="white",
                          max_words=1000, mask=mask).generate(negative)

image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[25, 18])
plt.title("Positive Reviews", fontsize=24, y=1.1)
plt.title("Negative Reviews", fontsize=24, y=1.1)
plt.imshow(wordcloud_neg.recolor(
    color_func=image_colors), interpolation="bilinear")
plt.axis("off")

plt.savefig('img/neg.jpg')

# plt.show()
