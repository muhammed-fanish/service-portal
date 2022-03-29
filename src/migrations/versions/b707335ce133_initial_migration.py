"""Initial migration.

Revision ID: b707335ce133
Revises: 
Create Date: 2022-03-24 11:36:14.903108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b707335ce133'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wso2UserId', sa.String(length=255), nullable=False),
    sa.Column('userName', sa.String(length=255), nullable=False),
    sa.Column('providerName', sa.String(length=255), nullable=False),
    sa.Column('apiKey', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phoneNumber', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###