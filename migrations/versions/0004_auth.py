from alembic import op
import sqlalchemy as sa
revision='0004'
down_revision='0003'
def upgrade():
    op.add_column('users',sa.Column('password_hash',sa.String(300)))
    op.add_column('users',sa.Column('role',sa.String(20),server_default='user',nullable=False))
def downgrade():
    with op.batch_alter_table('users') as b:
        b.drop_column('role'); b.drop_column('password_hash')
