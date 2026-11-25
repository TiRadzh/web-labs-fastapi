from alembic import op
import sqlalchemy as sa
revision='0005'
down_revision='0004'
def upgrade():
    op.create_table('attachments',sa.Column('id',sa.Integer,primary_key=True),sa.Column('filename',sa.String(255),nullable=False),sa.Column('file_path',sa.String(255),nullable=False),sa.Column('content_type',sa.String(100),nullable=False),sa.Column('size',sa.Integer,nullable=False),sa.Column('task_id',sa.Integer,sa.ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False),sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id'),nullable=False),sa.Column('created_at',sa.DateTime,server_default=sa.func.now(),nullable=False))
def downgrade(): op.drop_table('attachments')
