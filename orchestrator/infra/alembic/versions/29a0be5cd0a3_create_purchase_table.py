"""create purchase table

Revision ID: 29a0be5cd0a3
Revises: 6e0fef1de918
Create Date: 2023-05-15 09:25:00.207981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29a0be5cd0a3'
down_revision = '6e0fef1de918'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'purchases',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('machine_id', sa.String),
        sa.Column('product_id', sa.String),
        sa.Column('price', sa.Integer),
        sa.Column('at', sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('purchases')
