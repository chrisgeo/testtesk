import logging
from celery import (
    Celery,
    group,
    chain,
    task
)



log = logging.getLogger(__name__)

worker = Celery(__name__)
worker.config_from_object('testtesk.celeryconfig')

@worker.task(
    bind=True,
    default_retry_delay=10,
    rate_limit='300/m',
    max_retries=1)
def test_task(self, num):
    try:
        if num == 3:
            #doing this causes app to stay in pending
            #state
            if self.request.callbacks:
                self.request.callbacks[:] = []

            log.debug('success test task')
            #self.update_state(state='SUCCESS')
            return num

        log.debug('test success something none')
        if num == 5:
            raise Exception("Brought to you by the number 5")

    except Exception as exc:
        self.retry(exc=exc)

    return None

