"""One-time instructor-created assessment sessions."""

from __future__ import annotations

import hashlib
import json
import secrets
import string
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class AssessmentSession:
    week: int
    code_hash: str
    created_at: str
    used: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "week": self.week,
            "code_hash": self.code_hash,
            "created_at": self.created_at,
            "used": self.used,
        }


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def create_session(path: Path, week: int) -> str:
    alphabet = string.ascii_uppercase + string.digits
    code = "-".join(
        "".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(2)
    )
    session = AssessmentSession(
        week=week,
        code_hash=_hash_code(code),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(session.to_dict(), indent=2) + "\n", encoding="utf-8")
    return code


def consume_session(path: Path, code: str, week: int) -> AssessmentSession:
    if not path.exists():
        raise ValueError("No assessment session is active. Ask the instructor to create one.")
    data = json.loads(path.read_text(encoding="utf-8"))
    session = AssessmentSession(**data)
    if session.used or session.week != week or not secrets.compare_digest(session.code_hash, _hash_code(code.strip().upper())):
        raise ValueError("That assessment code is invalid or has already been used.")
    used_session = AssessmentSession(session.week, session.code_hash, session.created_at, True)
    path.write_text(json.dumps(used_session.to_dict(), indent=2) + "\n", encoding="utf-8")
    return session
