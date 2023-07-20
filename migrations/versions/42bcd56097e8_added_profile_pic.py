"""added profile pic

Revision ID: 42bcd56097e8
Revises: 6d142f0bd005
Create Date: 2023-07-20 01:36:02.406683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42bcd56097e8'
down_revision = '6d142f0bd005'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('profile_pic')

    # ### end Alembic commands ###