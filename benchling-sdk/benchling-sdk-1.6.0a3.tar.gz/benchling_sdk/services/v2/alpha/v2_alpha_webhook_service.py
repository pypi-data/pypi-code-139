import base64
from functools import lru_cache
from typing import cast, List

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from jwcrypto import jwk

from benchling_sdk.apps.helpers.webhook_helpers import (
    der_signatures_from_versioned_signatures,
    WebhookVerificationError,
)
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.services.v2.base_service import BaseService
from benchling_sdk.services.v2.stable.api_service import ApiService


class V2AlphaWebhookService(BaseService):
    """
    V2-Alpha Webhooks.

    Convenience for API calls related to webhook verification.

    This does not correspond to Benchling's API reference.
    """

    _api_service: ApiService

    def __init__(self, api_service: ApiService):
        """
        Init Webhook Service.

        Accepts an API Service to make specialized calls in Benchling for JWKs not specced in the API.
        """
        super().__init__(api_service.client, api_service.retry_strategy)
        self._api_service = api_service

    @lru_cache()
    @api_method
    def jwks_by_app(self, app_id: str) -> jwk.JWKSet:
        """
        Get JWKs by App.

        Retrieves a set of JWKs assigned to an app used to verify webhooks. Caches subsequent calls.
        Use clear_cache() to force contacting the server on the next call.
        """
        response = self._api_service.get_response(f"/apps/jwks/{app_id}")
        return jwk.JWKSet.from_json(response.content)

    def clear_cache(self) -> None:
        """
        Clear Cache.

        Explicitly clears the SDK cache of JWKs from Benchling, causing the next call to reach the server.
        """
        self.jwks_by_app.cache_clear()

    # TODO: Can we get app_id from the webhook? Does app_id matter?
    def verify_raw(self, app_id, data, headers) -> None:
        """
        Verify Raw Webhooks.

        Verifies that a webhook was a valid webhook from Benchling.
        Raises WebhookVerificationError if the webhook could not be verified.
        """
        to_verify = f'{headers["webhook-id"]}.{headers["webhook-timestamp"]}.{data}'
        signatures = headers["webhook-signature"].split(" ")
        der_signatures = der_signatures_from_versioned_signatures(signatures)
        encoded_signatures = [base64.b64decode(der_signature) for der_signature in der_signatures]
        jwks = self.jwks_by_app(app_id)
        has_valid_signature = self._has_valid_signature(to_verify, jwks, encoded_signatures)
        if not has_valid_signature:
            self.clear_cache()
            jwks = self.jwks_by_app(app_id)
            has_valid_signature = self._has_valid_signature(to_verify, jwks, encoded_signatures)
        if not has_valid_signature:
            raise WebhookVerificationError("No matching signature found")

    def _has_valid_signature(self, to_verify: str, jwks: jwk.JWKSet, encoded_signatures: List[bytes]) -> bool:
        for jk in jwks:
            pubkey = cast(ec.EllipticCurvePublicKey, load_pem_public_key(jk.export_to_pem()))
            for raw_signature in encoded_signatures:
                try:
                    pubkey.verify(raw_signature, bytes(to_verify, "utf-8"), ec.ECDSA(hashes.SHA256()))
                except InvalidSignature:
                    continue
                return True
        return False
