from sentry_sdk.integrations import celery
from urllib3.exceptions import RequestError
from utils import _datetime


class A:
    def __init__(self, a):
        self.a = 1

    def __add__(self, other):
        return self.a + other.a


def add(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def countdown(n: int):
    while n > 0:
        countdown(n)


class PrimeRenewalRefundRecord:
    def __init__(self):
        self.channel = None
        self.refund_no = None
        self.renewal_record = None

    @classmethod
    def get_by_refund_no(cls, application_id, refund_no):
        pass


@celery.task(bind=True, max_retries=50)
def async_wechat_refund_query(self, application_id: int, refund_no: str):
    pass


def get_prime_refunder_cls_by_channel(channel):
    pass


@celery.task(bind=True, max_retries=50)
def async_wechat_prime_refund_query(self, application_id: int, refund_no: str, wechat_prime_logger=None):
    logger_action: str = "async_wechat_prime_refund_query"

    refund: PrimeRenewalRefundRecord = PrimeRenewalRefundRecord.get_by_refund_no(
        application_id=application_id, refund_no=refund_no
    )

    if not refund:
        self.retry(countdown=5 * async_wechat_refund_query.request.retries)

    wechat_prime_logger.info(f'{logger_action},req')
    try:
        client = refund.renewal_record.subscription.client
        query_result = client.query_refund(refund.refund_no)
    except RequestError:
        wechat_prime_logger.warning(
            f'{logger_action},request_err,contract_code'
        )
        self.retry(countdown=5 * async_wechat_refund_query.request.retries)

    if not query_result:
        self.retry(countdown=30 * async_wechat_refund_query.request.retries)
        wechat_prime_logger.warning(
            f'{logger_action},no_query_result,contract_code'
        )
        return

    # 找到对应的退款编号
    for k, v in query_result.items():
        if k.startswith('out_refund_no_') and v == refund.refund_no:
            refund_index = k.split('_')[-1]

    if not refund_index:
        wechat_prime_logger.warning(
            f'{logger_action},cannot_index_result,contract_code'
        )
        self.retry(countdown=30 * async_wechat_refund_query.request.retries)

    refund_id_key: str = f'refund_id_{refund_index}'
    refund_success_time_key: str = f'refund_success_time_{refund_index}'
    if refund_id_key not in query_result or refund_success_time_key not in query_result:
        wechat_prime_logger.warning(
            f'{logger_action},cannot_index_result,contract_code'
        )
        self.retry(countdown=30 * async_wechat_refund_query.request.retries)

    refund_id: str = query_result[refund_id_key]
    refund_success_time: str = query_result[refund_success_time_key]  # 格式 2016-07-25 15:26:26

    # 更新退款记录并通知主站
    get_prime_refunder_cls_by_channel(refund.channel).refund_success(
        refund_record=refund,
        refund_time=_datetime(refund_success_time),
        third_party_refund_no=refund_id,
    )
    wechat_prime_logger.info(
        f'{logger_action},success,contract_code'
    )

    return


def main():
    add(1, 2)
    add(1, "a")
    divide(1, 2)
    divide(1, 0)

    a = A(1)
    add(a.a, a.b)


if __name__ == '__main__':
    main()
