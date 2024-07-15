"""Added session_id to JBFSM state

Revision ID: ba643170ce28
Revises: 5491e55dfb6e
Create Date: 2024-07-09 01:55:58.622880

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ba643170ce28"
down_revision = "5491e55dfb6e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("jb_fsm_state", sa.Column("session_id", sa.String(), nullable=True))
    op.drop_column("jb_fsm_state", "pid")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "jb_fsm_state",
        sa.Column("pid", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("jb_fsm_state", "session_id")
    # ### end Alembic commands ###
