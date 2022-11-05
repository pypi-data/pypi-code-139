from typing import List


class WebhookVerificationError(Exception):
    """
    Webhook Verification Error.

    Indicates a webhook from Benchling could not be verified.

    Some reasons this could happen include:
    - A app developer misconfiguration (e.g., wrong app)
    - A webhook was received too late
    - The webhook did not originate from Benchling (possible attack vector)
    """

    # The SDK exposes its own stable error in case we change webhook implementations later
    pass


def der_signatures_from_versioned_signatures(versioned_signatures: str) -> List[str]:
    """
    Parse and return a list of ders signatures from a single string.

    Signature format is f"v{version_number}der,{signature}"
    """
    der_signatures = []
    for versioned_sig in versioned_signatures:
        _version, sig = versioned_sig.split(",")
        if "der" in _version:
            der_signatures.append(sig)
    if der_signatures is []:
        raise WebhookVerificationError("Expected to find a der encoded signature")
    return der_signatures
