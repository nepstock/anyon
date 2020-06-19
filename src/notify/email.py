from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Email:
    __slots__ = ("_client",)

    def __init__(self, api_key: str) -> None:
        self._client = SendGridAPIClient(api_key)

    def send(self, from_email, to_email, subject, html_content):
        message = Mail(
            from_email, to_email, subject, html_content=html_content,
        )
        return self._client.send(message)
