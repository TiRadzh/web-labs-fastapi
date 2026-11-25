from alembic import op
import sqlalchemy as sa
revision = '0003'
down_revision = '0002'
def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer,primary_key=True),sa.Column('username',sa.String(100),nullable=False,unique=True))
    op.create_table('projects',sa.Column('id',sa.Integer,primary_key=True),sa.Column('title',sa.String(200),nullable=False),sa.Column('owner_id',sa.Integer,sa.ForeignKey('users.id'),nullable=False))
    op.create_table('tags',sa.Column('id',sa.Integer,primary_key=True),sa.Column('name',sa.String(100),nullable=False,unique=True))
    with op.batch_alter_table('tasks') as b:
        b.add_column(sa.Column('project_id',sa.Integer))
        b.create_foreign_key('fk_task_project','projects',['project_id'],['id'],ondelete='CASCADE')
    op.create_table('task_tags',sa.Column('task_id',sa.Integer,sa.ForeignKey('tasks.id',ondelete='CASCADE'),primary_key=True),sa.Column('tag_id',sa.Integer,sa.ForeignKey('tags.id',ondelete='CASCADE'),primary_key=True))
    op.create_table('comments',sa.Column('id',sa.Integer,primary_key=True),sa.Column('text',sa.String(2000),nullable=False),sa.Column('task_id',sa.Integer,sa.ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False),sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id'),nullable=False))
def downgrade():
    op.drop_table('comments')
    op.drop_table('task_tags')
    with op.batch_alter_table('tasks') as b:
        b.drop_constraint('fk_task_project',type_='foreignkey')
        b.drop_column('project_id')
    for t in ('tags','projects','users'): op.drop_table(t)
