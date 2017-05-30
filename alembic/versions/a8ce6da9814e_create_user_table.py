"""create user table

Revision ID: a8ce6da9814e
Revises: 
Create Date: 2017-05-29 10:49:57.414112+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8ce6da9814e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.Unicode(255), unique=False, nullable=False),
    )


def downgrade():
    op.drop_table('users')

