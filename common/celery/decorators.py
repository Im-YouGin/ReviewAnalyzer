from functools import wraps

from celery import shared_task
from celery.utils.log import get_task_logger

from common.redis.lock import redis_lock


def task_with_lock(task_func):
    @shared_task(bind=True)
    @wraps(task_func)
    def wrapped_task(self, *args, **kwargs):
        logger = get_task_logger(self.name)
        logger.info(f"Spawned a new instance of {self.name}")

        with redis_lock(self.name, self.app.oid) as acquired:
            if acquired:
                logger.info(f"Lock for {self.name} was acquired successfully.")

                return task_func(self, *args, **kwargs)

            else:
                logger.info(f"Another instance of {self.name} is already running.")

    return wrapped_task
