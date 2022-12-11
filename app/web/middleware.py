import hashlib
import hmac
import logging

from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

log = logging.getLogger("app")


class SentryProcessMiddleware:
    def __init__(self, app: ASGIApp, sentry_secret: str) -> None:
        self.app = app
        self.sentry_secret = sentry_secret

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] == "http":

            async def inner_receive():
                request = Request(scope)
                message = await receive()
                body = message.get("body", b"").decode("utf-8")
                scope["sentry-resource"] = request.headers.get(
                    "Sentry-Hook-Resource"
                )
                scope["sentry-timestamp"] = request.headers.get(
                    "Sentry-Hook-Timestamp"
                )
                signature = request.headers.get("Sentry-Hook-Signature")
                if scope["sentry-resource"] and signature:
                    log.info(f"new hook signature - {signature}")
                    digest = hmac.new(
                        key=self.sentry_secret.encode("utf-8"),
                        msg=body,
                        digestmod=hashlib.sha256,
                    ).hexdigest()
                    digest_check = hmac.compare_digest(digest, signature)
                    scope["sentry-digest-valid"] = digest and digest_check
                    log.info(f"digest check - {digest}")
                else:
                    scope["sentry-digest-valid"] = True
                return message

        else:
            inner_receive = receive

        await self.app(scope, inner_receive, send)
