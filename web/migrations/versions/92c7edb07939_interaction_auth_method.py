"""Interaction Auth Method

Revision ID: 92c7edb07939
Revises: 40021fb6fbec
Create Date: 2022-03-12 20:14:39.244931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c7edb07939'
down_revision = '40021fb6fbec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('login_method', sa.Enum('did not attempt', 'fido', 'password'), nullable=False))
        batch_op.alter_column('page',
               existing_type=sa.VARCHAR(length=9),
               type_=sa.Enum('/register', '/login', '/add-password'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interaction', schema=None) as batch_op:
        batch_op.alter_column('page',
               existing_type=sa.Enum('/register', '/login', '/add-password'),
               type_=sa.VARCHAR(length=9),
               existing_nullable=False)
        batch_op.drop_column('login_method')

    # ### end Alembic commands ###
