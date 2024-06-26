"""change nullable

Revision ID: 2af17251775b
Revises: 356d9ec77b9f
Create Date: 2024-05-25 14:37:48.004486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2af17251775b'
down_revision: Union[str, None] = '356d9ec77b9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'edited_image',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('images', 'description',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('images', 'qr_code',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'qr_code',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('images', 'description',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('images', 'edited_image',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
