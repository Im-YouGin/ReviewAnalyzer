from functools import wraps

from celery import shared_task
from celery.utils.log import get_task_logger

from common.redis.lock import redis_lock


def task_with_lock(task_func):
    @shared_task(bind=True)
    @wraps(task_func)
    def wrapped_task(self, *args, **kwargs):
        logger = get_task_logger(self.name)
        logger.info(f"Spawned a new instance of %s" % self.name)

        with redis_lock(self.name, self.app.oid) as acquired:
            if acquired:
                logger.info(f"Lock for %s was acquired successfully." % self.name)

                return task_func(self, *args, **kwargs)

            logger.info(f"Another instance of %s is already running." % self.name)

    return wrapped_task
