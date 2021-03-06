"""category_table

Revision ID: 00beeaac91d9
Revises: 9160233d9b78
Create Date: 2020-07-03 22:15:57.220443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00beeaac91d9'
down_revision = '9160233d9b78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.add_column('post', sa.Column('category', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'category', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'category')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
