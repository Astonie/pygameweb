"""removed unused page tables and fields

Revision ID: 6cb6a6a151b7
Revises: f15de2cc22c7
Create Date: 2017-02-23 17:25:48.059713

"""

# revision identifiers, used by Alembic.
revision = '6cb6a6a151b7'
down_revision = 'f15de2cc22c7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skin')
    op.drop_table('modules')
    op.drop_column('node', 'mods')
    op.drop_column('node', 'parentid')
    op.drop_column('node', 'folderid')
    op.drop_column('node', 'image')
    op.drop_column('node', 'folder')
    op.drop_column('node', 'custom')
    op.drop_column('node', 'target')
    op.drop_column('node', 'type')
    op.drop_column('node', 'skin_id')
    op.drop_column('node', 'modules_id')
    op.rename_table('node', 'page')
    op.execute('ALTER SEQUENCE node_id_seq RENAME TO page_id_seq')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('node', sa.Column('modules_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('skin_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('type', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('target', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('custom', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('folder', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('image', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('folderid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('parentid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('node', sa.Column('mods', sa.INTEGER(), autoincrement=False, nullable=True))
    op.rename_table('page', 'node')
    op.execute('ALTER SEQUENCE page_id_seq RENAME TO node_id_seq')

    op.create_table('modules',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('orders', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='modules_pkey')
    )
    op.create_table('skin',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('fname', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('orders', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='skin_pkey')
    )
    # ### end Alembic commands ###
