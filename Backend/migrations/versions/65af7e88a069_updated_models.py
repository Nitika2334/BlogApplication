"""Updated Models

Revision ID: 65af7e88a069
Revises: ef4b3bec6dcb
Create Date: 2024-08-05 13:00:20.304348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65af7e88a069'
down_revision = 'ef4b3bec6dcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_uid', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_uid'], ['uid'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_uid')

    # ### end Alembic commands ###
