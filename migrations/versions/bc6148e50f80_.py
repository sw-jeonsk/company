"""empty message

Revision ID: bc6148e50f80
Revises: 
Create Date: 2024-12-15 19:22:38.498589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc6148e50f80'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Company',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('code', sa.VARCHAR(length=128), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('CompanyName',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('company_id', sa.BIGINT(), nullable=True),
    sa.Column('country', sa.VARCHAR(length=128), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CompanyName_country'), 'CompanyName', ['country'], unique=False)
    op.create_table('CompanyTag',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('company_id', sa.BIGINT(), nullable=True),
    sa.Column('country', sa.VARCHAR(length=128), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_CompanyTag_country'), 'CompanyTag', ['country'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_CompanyTag_country'), table_name='CompanyTag')
    op.drop_table('CompanyTag')
    op.drop_index(op.f('ix_CompanyName_country'), table_name='CompanyName')
    op.drop_table('CompanyName')
    op.drop_table('Company')
    # ### end Alembic commands ###
