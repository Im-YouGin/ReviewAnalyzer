from celery import shared_task

from common.celery.decorators import task_with_lock


@shared_task
def q_scrape_app_store_app_reviews(application_id):
    from scraping.app_store.app_reviews.runner import (
        AppStoreReviewScrapingProcessRunner,
    )

    AppStoreReviewScrapingProcessRunner(application_id).scrape()


@shared_task
def q_scrape_google_play_app_reviews(application_id):
    from scraping.google_play.app_reviews.runner import (
        GooglePlayReviewScrapingProcessRunner,
    )

    GooglePlayReviewScrapingProcessRunner(application_id).scrape()


@task_with_lock
def q_scrape_app_store_all_apps_reviews(*args):
    from scraping.app_store.app_reviews.daemon import AppStoreAllReviewScrapingDaemon

    AppStoreAllReviewScrapingDaemon().run()


@task_with_lock
def q_scrape_google_play_all_apps_reviews(*args):
    from scraping.google_play.app_reviews.daemon import (
        GooglePlayAllReviewScrapingDaemon,
    )

    GooglePlayAllReviewScrapingDaemon().run()
