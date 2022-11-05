from typing import Any, Dict, Union

from svix import Webhook, WebhookVerificationError


class WebhookFailedVerificationError(Exception):
    """
    Webhook Verification Error.

    Indicates a webhook from Benchling could not be verified.

    Some reasons this could happen include:
    - A user misconfiguration (e.g., wrong webhook secret)
    - A webhook was received too late
    - The webhook did not originate from Benchling (possible attack vector)
    """

    # The SDK exposes its own stable error in case we change webhook implementations later
    pass


def verify_webhook_raw(secret: str, headers: Dict[str, Any], data: Union[str, bytes]) -> Any:
    """
    Verify webhook raw.

    Verifies that a webhook was a valid webhook from Benchling.

    Raises WebhookFailedVerificationError if the webhook could not be verified.
    Otherwise returns the verified payload.
    """
    try:
        return Webhook(secret).verify(data, headers)
    # Re-raise our stable error instead of exposing Svix error directly
    except WebhookVerificationError as e:
        raise WebhookFailedVerificationError(e)
