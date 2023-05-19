import numpy as np

from analytics.constants import SENTIMENT_BREAKDOWN_DEFAULT, STARS_BREAKDOWN_DEFAULT


class AnalyticsManager:
    def __init__(self, df):
        self.df = df

    def get_analytics(self):
        return {
            "total_review_count": self._total_review_count,
            "overall_sentiment": self._overall_sentiment,
            "average_stars": self._average_stars,
            "stars_breakdown": self._stars_breakdown,
            "sentiment_breakdown": self._sentiment_breakdown,
            "sentiment_timeseries": self._sentiment_timeseries,
            "stars_timeseries": self._stars_timeseries,
            "review_timeseries": self._review_timeseries,
        }

    @property
    def _total_review_count(self):
        return self.df.shape[0]

    @property
    def _overall_sentiment(self):
        sentiment_mapping = {"negative": -1, "neutral": 0, "positive": 1}
        overall_sentiment_score = (
            self.df[self.df["sentiment_str"] != ""]["sentiment_str"]
            .map(sentiment_mapping)
            .mean()
        )
        overall_sentiment_score = (overall_sentiment_score + 1) / 2 * 100

        return (
            round(overall_sentiment_score)
            if not np.isnan(overall_sentiment_score)
            else 0
        )

    @property
    def _average_stars(self):
        average_stars = self.df["stars"].mean()

        return round(average_stars, 1) if not np.isnan(average_stars) else 0

    @property
    def _stars_breakdown(self):
        stars_breakdown = self.df["stars"].value_counts().to_dict()

        return stars_breakdown if stars_breakdown else STARS_BREAKDOWN_DEFAULT

    @property
    def _sentiment_breakdown(self):
        sentiment_breakdown = (
            self.df[self.df["sentiment_str"] != ""]["sentiment_str"]
            .value_counts()
            .to_dict()
        )

        return (
            sentiment_breakdown if sentiment_breakdown else SENTIMENT_BREAKDOWN_DEFAULT
        )

    @property
    def _sentiment_timeseries(self):
        weekly_df = (
            self.df[self.df["sentiment_str"] != ""]
            .groupby(["sentiment_str"])
            .resample('W', on='date')
            .size()
            .unstack(level=0, fill_value=0)
            .reset_index()
        )
        weekly_df['date'] = weekly_df['date'].dt.date

        return weekly_df.to_dict("records")

    @property
    def _stars_timeseries(self):
        weekly_df = (
            self.df
            .resample('W', on='date')["stars"]
            .mean()
            .round(1)
            .reset_index()
        )
        weekly_df['date'] = weekly_df['date'].dt.date

        return weekly_df.to_dict("records")

    @property
    def _review_timeseries(self):
        weekly_df = (
            self.df
            .resample('W', on='date')
            .size()
            .reset_index(name="count")
        )
        weekly_df['date'] = weekly_df['date'].dt.date

        return weekly_df.to_dict("records")

