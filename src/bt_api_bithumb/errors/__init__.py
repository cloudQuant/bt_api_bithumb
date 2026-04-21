from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class BithumbErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        message = str(raw_error.get("message", raw_error.get("msg", raw_error)))
        message_lower = message.lower()

        if "invalid signature" in message_lower or "authentication" in message_lower:
            return cls._build_error(UnifiedErrorCode.INVALID_SIGNATURE, venue, raw_error)
        if "insufficient" in message_lower or "balance" in message_lower:
            return cls._build_error(UnifiedErrorCode.INSUFFICIENT_BALANCE, venue, raw_error)
        if "not found" in message_lower or "does not exist" in message_lower:
            return cls._build_error(UnifiedErrorCode.ORDER_NOT_FOUND, venue, raw_error)
        if "rate limit" in message_lower or "too many requests" in message_lower:
            return cls._build_error(UnifiedErrorCode.RATE_LIMIT_EXCEEDED, venue, raw_error)
        if "market" in message_lower or "closed" in message_lower:
            return cls._build_error(UnifiedErrorCode.MARKET_CLOSED, venue, raw_error)
        return super().translate(raw_error, venue)

    @staticmethod
    def _build_error(code: UnifiedErrorCode, venue: str, raw_error: dict[str, Any]) -> UnifiedError:
        message = str(raw_error.get("message", raw_error.get("msg", code.name)))
        return UnifiedError(
            code=code,
            category=ErrorCategory.BUSINESS,
            venue=venue,
            message=message,
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
