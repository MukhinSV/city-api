"""update city table

Revision ID: 217dcd1a0398
Revises: 62d5c28273f3
Create Date: 2026-05-06 09:58:37.865675

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "217dcd1a0398"
down_revision: Union[str, Sequence[str], None] = "62d5c28273f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "city", ["name"])


def downgrade() -> None:
    op.drop_constraint(None, "city", type_="unique")
