from common.celery.decorators import task_with_lock


@task_with_lock
def q_sentiment_analysis_daemon(*args):
    from analytics.sentiment.daemon import SentimentAnalysisDaemon

    SentimentAnalysisDaemon().run()
