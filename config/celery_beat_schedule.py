from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    "app-store-reviews-scraping-daemon": {
        "task": "scraping.tasks.q_scrape_app_store_all_apps_reviews",
        "schedule": timedelta(minutes=30),
        "args": [],
    },
    "google-play-reviews-scraping-daemon": {
        "task": "scraping.tasks.q_scrape_google_play_all_apps_reviews",
        "schedule": timedelta(minutes=15),
        "args": [],
    },
    "sentiment-analysis-daemon": {
        "task": "analytics.tasks.q_sentiment_analysis_daemon",
        "schedule": timedelta(seconds=15),
        "args": [],
    },
}
