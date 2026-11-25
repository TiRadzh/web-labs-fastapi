from alembic import op
import sqlalchemy as sa
revision = '0001'
down_revision = None

def upgrade():
    op.create_table('tasks', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('title', sa.String(200), nullable=False), sa.Column('description', sa.Text()))

def downgrade():
    op.drop_table('tasks')
