"""Added index and constraints

Revision ID: 5208692d740d
Revises: 6cf0abfd3a33
Create Date: 2023-04-09 03:15:21.555751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5208692d740d'
down_revision = '6cf0abfd3a33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_users_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_title'))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)

    # ### end Alembic commands ###
