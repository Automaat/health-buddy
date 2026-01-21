"""add source column to health_metrics

Revision ID: add_source_column
Revises: 17a9b48545b3
Create Date: 2026-01-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "add_source_column"
down_revision: str | None = "17a9b48545b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "health_metrics",
        sa.Column("source", sa.String(50), nullable=False, server_default="manual"),
    )
    op.create_index("ix_health_metrics_source", "health_metrics", ["source"])


def downgrade() -> None:
    op.drop_index("ix_health_metrics_source", table_name="health_metrics")
    op.drop_column("health_metrics", "source")
