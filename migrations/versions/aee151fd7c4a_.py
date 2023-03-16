"""empty message

Revision ID: aee151fd7c4a
Revises: 30eba8cc3bb4
Create Date: 2022-05-19 09:51:09.545983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee151fd7c4a'
down_revision = '30eba8cc3bb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('logo', sa.BLOB(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'logo')
    # ### end Alembic commands ###