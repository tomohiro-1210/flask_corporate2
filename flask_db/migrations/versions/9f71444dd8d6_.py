"""empty message

Revision ID: 9f71444dd8d6
Revises: 926e071275cf
Create Date: 2024-08-17 11:14:05.416426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f71444dd8d6'
down_revision = '926e071275cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('summary', sa.String(length=140), nullable=True),
    sa.Column('featured_image', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    # ### end Alembic commands ###
