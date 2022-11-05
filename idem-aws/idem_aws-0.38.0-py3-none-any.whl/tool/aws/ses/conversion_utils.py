from typing import Any
from typing import Dict


def convert_raw_domain_identity_to_present(
    hub,
    ctx,
    raw_resource: str,
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for SES Domain Identity.

    """

    resource_translated = {
        "name": raw_resource,
        "domain": raw_resource,
        "resource_id": raw_resource,
    }

    return resource_translated
