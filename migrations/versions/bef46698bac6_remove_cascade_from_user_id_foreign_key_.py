"""Remove CASCADE from user_id foreign key in comments table

Revision ID: bef46698bac6
Revises: 2af17251775b
Create Date: 2024-05-26 22:44:58.448396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bef46698bac6'
down_revision: Union[str, None] = '2af17251775b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
