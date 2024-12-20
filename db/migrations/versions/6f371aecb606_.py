"""empty message

Revision ID: 6f371aecb606
Revises: 64c292825362
Create Date: 2024-12-17 05:00:48.460690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f371aecb606'
down_revision = '64c292825362'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('retention_period',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('p_data',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('retention_rule_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('retention_rule_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('p_data',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('retention_period',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
