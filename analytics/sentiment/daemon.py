import logging

from transformers import pipeline

from analytics.sentiment.cleaning import clean_review
from applications.models import Review
from common.constants import BATCH_SIZE

logger = logging.getLogger("review_analyzer")

VERBOSE_LABELS = {"LABEL_2": "positive", "LABEL_1": "neutral", "LABEL_0": "negative"}


class SentimentAnalysisDaemon:
    SESSION_REVIEW_COUNT_LIMIT = 10
    WORKERS_COUNT = 1

    MODEL_NAME = "Seethal/sentiment_analysis_generic_dataset"

    def __init__(self):
        self._nlp_model = pipeline("sentiment-analysis", model=self.MODEL_NAME)

    def run(self):
        logger.info("Starting sentiment analysis daemon.")

        reviews = self._get_reviews_to_analyze()

        logger.info(
            f"Sentiment analysis daemon found %s reviews to analyze." % len(reviews)
        )

        # TODO: figure out how to parallelize
        updated_reviews = {self._analyze_sentiment(r) for r in reviews}

        Review.objects.bulk_update(
            updated_reviews, ("sentiment_str",), batch_size=BATCH_SIZE
        )

        logger.info("Sentiment analysis daemon finished.")

    def _analyze_sentiment(self, review):
        cleaned = clean_review(review.content)

        try:
            sentiment = self._nlp_model(cleaned)[0]
            review.sentiment_str = VERBOSE_LABELS[sentiment["label"]]

        except Exception as exc:
            logger.exception(
                f"Exception occurred trying to analyze the following review:\n%s\n%s" % (review.content, exc)
            )

        review.is_sentiment_analyzed = True

        return review

    @staticmethod
    def _slice_review_content(content):
        return " ".join(content.split()[:100])

    def _get_reviews_to_analyze(self):
        return Review.objects.filter(
            sentiment_str="", is_sentiment_analyzed=False
        ).order_by("?")[: self.SESSION_REVIEW_COUNT_LIMIT]
