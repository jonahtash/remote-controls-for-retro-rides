"""Login Attempts Table

Revision ID: 27c4f322ed1c
Revises: 92c7edb07939
Create Date: 2022-03-12 20:45:26.121200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27c4f322ed1c'
down_revision = '92c7edb07939'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_attempts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('password_successes', sa.Integer(), nullable=True),
    sa.Column('password_failures', sa.Integer(), nullable=True),
    sa.Column('fido_successes', sa.Integer(), nullable=True),
    sa.Column('fido_failures', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_attempts')
    # ### end Alembic commands ###
