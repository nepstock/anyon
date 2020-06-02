from requests.packages.urllib3.util.retry import Retry

from src.api.adapter import APIAdapter


def _get_retry_strategy():
    return Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"],
    )


def get_adapter():
    return APIAdapter(max_retries=_get_retry_strategy())
