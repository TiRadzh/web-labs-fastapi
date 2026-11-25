from alembic import op
import sqlalchemy as sa
revision = '0002'
down_revision = '0001'

def upgrade():
    with op.batch_alter_table('tasks', recreate='always') as b:
        b.add_column(sa.Column('status', sa.String(20), server_default='todo', nullable=False))
        b.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
        b.add_column(sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))

def downgrade():
    with op.batch_alter_table('tasks', recreate='always') as b:
        for name in ('updated_at','created_at','status'):
            b.drop_column(name)
