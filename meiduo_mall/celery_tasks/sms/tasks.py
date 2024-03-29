import logging

from .yuntongxun.ccp_sms import CCP
from verifications import constants
from celery_tasks.main import celery_app

logger = logging.getLogger('django')

@celery_app.task(bind=True, name='send_sms_code', retry_backoff=5)
def send_sms_code(self, mobile, sms_code):
    try:
        send_ret = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        logger.error(e)
        raise self.retry(exc=e, max_retries=3)
    return send_ret

