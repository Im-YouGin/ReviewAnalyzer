import numpy as np
import pandas as pd
import plotly.graph_objects as go

from analytics.constants import SENTIMENT_BREAKDOWN_DEFAULT
from analytics.constants.enums import Color


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

        def _plot_line(start_x, end_x, color, hoverinfo="none", text=None):
            return go.Scatter(
                x=[start_x, end_x],
                y=[0, 0],
                mode="lines",
                line={"color": color, "width": 10},
                hoverinfo=hoverinfo,
                text=text,
            )

        start_x = 0
        end_x = 1

        if not np.isnan(overall_sentiment_score):
            overall_sentiment_score = (overall_sentiment_score + 1) / 2 * 100
            green_line_end_x = start_x + (overall_sentiment_score / 100) * (
                end_x - start_x
            )

            if overall_sentiment_score < 100 / 3:
                annotation_color = Color.NEGATIVE
                annotation_text = "Negative"
            elif overall_sentiment_score < 100 / 3 * 2:
                annotation_color = Color.NEUTRAL
                annotation_text = "Neutral"
            else:
                annotation_color = Color.POSITIVE
                annotation_text = "Positive"

            data = [
                _plot_line(start_x, end_x, Color.NEGATIVE),
                _plot_line(
                    start_x,
                    green_line_end_x,
                    Color.POSITIVE,
                    hoverinfo="text",
                    text=f"Users are {round(overall_sentiment_score)}% satisfied<br>with your app",
                ),
            ]
        else:
            overall_sentiment_score = None

            annotation_color = Color.NEUTRAL
            annotation_text = "Not measured"
            data = [
                _plot_line(
                    start_x,
                    end_x,
                    Color.NEUTRAL,
                    hoverinfo="text",
                    text="Sentiment analysis is in progress.<br>You will be able to see the result in a bit.",
                ),
            ]

        layout = go.Layout(
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin={"l": 40, "r": 40, "b": 40, "t": 40},
            autosize=True,
            showlegend=False,
        )

        fig = go.Figure(data=data, layout=layout)

        # Add text annotation
        fig.add_annotation(
            x=(overall_sentiment_score if overall_sentiment_score is not None else 0) / 100,
            y=0,
            text=annotation_text,
            showarrow=True,
            font={"color": annotation_color, "size": 16},
        )

        return {"value": overall_sentiment_score, "chart": fig.to_json()}

    @property
    def _average_stars(self):
        average_stars = self.df["stars"].mean()

        return round(average_stars, 1) if not np.isnan(average_stars) else 0

    @property
    def _stars_breakdown(self):
        stars_breakdown = self.df["stars"].value_counts().to_dict()

        # Create a DataFrame from the stars_breakdown dictionary
        breakdown_df = pd.DataFrame(
            list(stars_breakdown.items()), columns=["stars", "count"]
        )

        # Set the order of stars and sort the DataFrame accordingly
        ordered_stars = [1, 2, 3, 4, 5]
        breakdown_df["stars"] = pd.Categorical(
            breakdown_df["stars"], categories=ordered_stars, ordered=True
        )
        breakdown_df.sort_values("stars", inplace=True)

        # Create a horizontal bar chart
        fig = go.Figure()

        index = []
        for star in ordered_stars:
            if star in breakdown_df["stars"].values:
                index.append(star)

                fig.add_trace(
                    go.Bar(
                        name=str(star),
                        y=[star],
                        x=breakdown_df[breakdown_df["stars"] == star]["count"],
                        marker={"color": "blue"},
                        orientation="h",
                        hovertemplate="%{x}",
                        width=0.5,
                    )
                )

        # Update layout
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            margin={"l": 10, "r": 10, "b": 10, "t": 10},
            showlegend=False,
            yaxis={"tickmode": "array", "tickvals": index, "showticklabels": True},
        )

        return fig.to_json()

    @property
    def _sentiment_breakdown(self):
        sentiment_breakdown = (
            self.df[self.df["sentiment_str"] != ""]["sentiment_str"]
            .value_counts()
            .to_dict()
        )

        if not sentiment_breakdown:
            sentiment_breakdown = SENTIMENT_BREAKDOWN_DEFAULT

        # Convert sentiment_breakdown to DataFrame
        breakdown_df = pd.DataFrame(
            list(sentiment_breakdown.items()), columns=["sentiment", "count"]
        )

        # Sort by sentiment to ensure order is negative, neutral, positive
        ordered_sentiments = ["negative", "neutral", "positive"]
        breakdown_df["sentiment"] = pd.Categorical(
            breakdown_df["sentiment"], categories=ordered_sentiments, ordered=True
        )
        breakdown_df.sort_values("sentiment", inplace=True)

        # Create a horizontal bar chart
        fig = go.Figure()

        for sentiment in ordered_sentiments:
            if sentiment in breakdown_df["sentiment"].values:
                fig.add_trace(
                    go.Bar(
                        name=sentiment.capitalize(),
                        y=[sentiment],
                        x=breakdown_df[breakdown_df["sentiment"] == sentiment]["count"],
                        marker={"color": Color.__dict__[sentiment.upper()]},
                        orientation="h",  # This line creates a horizontal bar.
                        hovertemplate="%{x}",  # This line changes the hover text to show only numeric value
                        width=0.5,  # Adjusts the width of the bar
                    )
                )

        # Update layout
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            margin={"l": 60, "r": 50, "b": 50, "t": 60},
            yaxis={"showticklabels": False},  # This line removes y-axis labels
            showlegend=False,
        )

        return fig.to_json()

    @property
    def _sentiment_timeseries(self):
        df_with_sentiment = self.df[self.df["sentiment_str"] != ""]
        if df_with_sentiment.empty:
            return

        weekly_df = (
            df_with_sentiment.groupby(["sentiment_str"])
            .resample("W", on="date")
            .size()
            .unstack(level=0, fill_value=0)
            .reset_index()
        )

        weekly_df["date"] = weekly_df["date"].dt.date

        # Instead of converting to a dict and returning, we will now plot the data.
        fig = go.Figure()

        if "negative" in weekly_df.columns:
            fig.add_trace(
                go.Bar(
                    name="Negative",
                    x=weekly_df["date"],
                    y=weekly_df["negative"],
                    marker={"color": Color.NEGATIVE},
                )
            )

        if "neutral" in weekly_df.columns:
            fig.add_trace(
                go.Bar(
                    name="Neutral",
                    x=weekly_df["date"],
                    y=weekly_df["neutral"],
                    marker={"color": Color.NEUTRAL},
                )
            )

        if "positive" in weekly_df.columns:
            fig.add_trace(
                go.Bar(
                    name="Positive",
                    x=weekly_df["date"],
                    y=weekly_df["positive"],
                    marker={"color": Color.POSITIVE},
                )
            )

        # Change the bar mode
        fig.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            margin={"l": 70, "r": 50, "b": 40, "t": 40},
            xaxis={"rangeslider": {"visible": True}},
            yaxis={"fixedrange": False},
            showlegend=False,
        )

        return fig.to_json()

    @property
    def _stars_timeseries(self):
        weekly_df = (
            self.df.resample("W", on="date")["stars"].mean().round(1).reset_index()
        )
        weekly_df["date"] = weekly_df["date"].dt.date

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=weekly_df["date"],
                y=weekly_df["stars"],
                mode="lines",
                name="stars",
                line={"shape": "spline"},
            )
        )

        fig.update_layout(
            yaxis_title="Stars",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            xaxis={"rangeslider": {"visible": True}},
            hovermode="x",
            yaxis={"fixedrange": False},
            margin={"l": 70, "r": 50, "b": 40, "t": 40},
        )

        return fig.to_json()

    @property
    def _review_timeseries(self):
        weekly_df = self.df.resample("W", on="date").size().reset_index(name="count")
        weekly_df["date"] = weekly_df["date"].dt.date

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=weekly_df["date"],
                y=weekly_df["count"],
                mode="lines",
                name="Reviews",
                line={"shape": "spline"},
            )
        )

        fig.update_layout(
            yaxis_title="Count",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            xaxis={"rangeslider": {"visible": True}},
            yaxis={"fixedrange": False},
            margin={"l": 70, "r": 50, "b": 40, "t": 40},
        )

        return fig.to_json()
