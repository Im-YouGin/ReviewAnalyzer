import re

import contractions
import emoji
import stanza
from bs4 import BeautifulSoup

stanza.download("en")
# Load the English language model
nlp = stanza.Pipeline("en")


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
    try:
        review = " ".join(
            [word.lemma for sent in nlp(review).sentences for word in sent.words]
        )
    except Exception:
        print(f"Failed to lemmatize {review}")

    return review
