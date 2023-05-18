import re

import contractions
import emoji
import nltk
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer

from analytics.constants import ENGLISH_STOP_WORDS

nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()


def clean_review(review):
    # Translate emojis into text
    review = emoji.demojize(review)

    # Replace underscores in emojis
    review = re.sub(r"_", " ", review)

    # Decode HTML
    review = BeautifulSoup(review, "lxml").get_text()

    # Remove URLs
    review = re.sub(r"http\S+|www\S+|https\S+", "", review, flags=re.MULTILINE)

    # Remove mentions but keep the text after '#'
    review = re.sub(r"@\w+", "", review)

    # Shortens repeated characters
    review = re.sub(r"(.)\1+", r"\1\1", review)

    # Expand contractions
    review = contractions.fix(review)

    # Remove digits
    review = re.sub(r"\d+", "", review)

    # Remove punctuations
    review = re.sub(r"\W", " ", review)

    # To lowercase
    review = review.lower()

    # Remove extra spaces
    review = re.sub(r"\s+", " ", review).strip()

    # Lemmatization and stop-word removal
    review = " ".join(
        [
            lemmatizer.lemmatize(word)
            for word in review.split()
            if word not in ENGLISH_STOP_WORDS
        ]
    )

    return review
