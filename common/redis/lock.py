import time
from contextlib import contextmanager

import redis
from django.conf import settings

LOCK_EXPIRE = 60 * 15  # 15 minutes

r = redis.Redis(host=settings.REDIS_HOST, port=6379, db=2)


@contextmanager
def redis_lock(lock_id, oid):
    # -3 ensures that we try to release the lock a bit earlier than its actual expiration time.
    timeout_at = time.monotonic() + LOCK_EXPIRE

    # r.setnx returns True if the key was set, False if it was not
    status = r.setnx(lock_id, oid)

    # Set the expiration time for the lock
    if status:
        r.expire(lock_id, LOCK_EXPIRE)

    try:
        yield status

    finally:
        # Redis delete is very fast, and we can use it to take
        # advantage of using setnx() for atomic locking
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            r.delete(lock_id)
