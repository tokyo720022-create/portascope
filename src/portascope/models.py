"""Shared, serializable data models used by the rule engine and reporters."""

from dataclasses import dataclass
from typing import Literal

Severity = Literal["error", "warning", "info"]


@dataclass(frozen=True, slots=True)
class Finding:
    """One explainable portability issue detected by a rule."""

    rule_id: str
    severity: Severity
    target: str
    paths: tuple[str, ...]
    message: str
    recommendation: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation with stable field names."""
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "target": self.target,
            "paths": list(self.paths),
            "message": self.message,
            "recommendation": self.recommendation,
        }
