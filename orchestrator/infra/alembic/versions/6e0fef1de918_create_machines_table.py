"""create machines table

Revision ID: 6e0fef1de918
Revises: 
Create Date: 2023-05-14 20:44:37.247366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e0fef1de918'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'machines',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('hardware_id', sa.String),
    )


def downgrade() -> None:
    op.drop_table('machines')
