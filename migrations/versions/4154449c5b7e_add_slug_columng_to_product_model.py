"""add slug columng to product model

Revision ID: 4154449c5b7e
Revises: 3bd1ae419746
Create Date: 2024-10-30 22:18:50.624614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4154449c5b7e'
down_revision = '3bd1ae419746'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(), nullable=True))
        batch_op.create_unique_constraint('slug', ['slug'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('slug', type_='unique')
        batch_op.drop_column('slug')

    # ### end Alembic commands ###
