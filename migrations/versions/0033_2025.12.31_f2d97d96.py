"""Migrate template variable syntax from brackets to double braces

Revision ID: 0033_2025.12.31_f2d97d96
Revises: 0032_2025.12.30_bb1b64a3
Create Date: 2025-12-31 17:22:14.280843+00:00
"""

import re
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic
revision: str = "0033_2025.12.31_f2d97d96"
down_revision: str | None = "0032_2025.12.30_bb1b64a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Template fields in releasepolicy that may contain variable placeholders
TEMPLATE_FIELDS = [
    "release_checklist",
    "start_vote_template",
    "announce_release_template",
    "vote_comment_template",
]

# Known variable names that should be converted
# This explicit list avoids accidentally converting Subject tags
KNOWN_VARIABLES = [
    "CHECKLIST_URL",
    "COMMITTEE",
    "DOWNLOAD_URL",
    "DURATION",
    "KEYS_FILE",
    "PROJECT",
    "RELEASE_CHECKLIST",
    "REVIEW_URL",
    "REVISION",
    "TAG",
    "VERSION",
    "VOTE_ENDS_UTC",
    "YOUR_ASF_ID",
    "YOUR_FULL_NAME",
]

# Pattern to match only known [VARIABLE] names
OLD_VARIABLE_PATTERN = re.compile(r"\[(" + "|".join(KNOWN_VARIABLES) + r")\]")

# Pattern to match only known {{VARIABLE}} names
NEW_VARIABLE_PATTERN = re.compile(r"\{\{(" + "|".join(KNOWN_VARIABLES) + r")\}\}")


def _convert_old_to_new(text: str) -> str:
    """Convert [VARIABLE] syntax to {{VARIABLE}} syntax."""
    return OLD_VARIABLE_PATTERN.sub(r"{{\1}}", text)


def _convert_new_to_old(text: str) -> str:
    """Convert {{VARIABLE}} syntax to [VARIABLE] syntax."""
    return NEW_VARIABLE_PATTERN.sub(r"[\1]", text)


def upgrade() -> None:
    conn = op.get_bind()

    # Fetch all release policies with their template fields
    result = conn.execute(sa.text(f"SELECT id, {', '.join(TEMPLATE_FIELDS)} FROM releasepolicy"))
    rows = result.fetchall()

    for row in rows:
        row_id = row[0]
        updates: dict[str, str] = {}

        for i, field in enumerate(TEMPLATE_FIELDS):
            old_value = row[i + 1]
            if old_value:
                new_value = _convert_old_to_new(old_value)
                if new_value != old_value:
                    updates[field] = new_value

        if updates:
            set_clause = ", ".join(f"{field} = :{field}" for field in updates)
            conn.execute(
                sa.text(f"UPDATE releasepolicy SET {set_clause} WHERE id = :id"),
                {"id": row_id, **updates},
            )


def downgrade() -> None:
    conn = op.get_bind()

    # Fetch all release policies with their template fields
    result = conn.execute(sa.text(f"SELECT id, {', '.join(TEMPLATE_FIELDS)} FROM releasepolicy"))
    rows = result.fetchall()

    for row in rows:
        row_id = row[0]
        updates: dict[str, str] = {}

        for i, field in enumerate(TEMPLATE_FIELDS):
            old_value = row[i + 1]
            if old_value:
                new_value = _convert_new_to_old(old_value)
                if new_value != old_value:
                    updates[field] = new_value

        if updates:
            set_clause = ", ".join(f"{field} = :{field}" for field in updates)
            conn.execute(
                sa.text(f"UPDATE releasepolicy SET {set_clause} WHERE id = :id"),
                {"id": row_id, **updates},
            )
