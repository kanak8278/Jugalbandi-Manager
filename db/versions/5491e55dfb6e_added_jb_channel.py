"""Added jb channel

Revision ID: 5491e55dfb6e
Revises: 159ddccc1ed1
Create Date: 2024-07-08 12:40:55.124729

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5491e55dfb6e"
down_revision = "159ddccc1ed1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jb_channel",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("bot_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("key", sa.String(), nullable=True),
        sa.Column("app_id", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["bot_id"],
            ["jb_bot.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_constraint("jb_bot_phone_number_key", "jb_bot", type_="unique")
    op.drop_column("jb_bot", "channels")
    op.drop_column("jb_bot", "phone_number")
    op.add_column("jb_session", sa.Column("channel_id", sa.String(), nullable=True))
    op.drop_constraint("jb_session_bot_id_fkey", "jb_session", type_="foreignkey")
    op.create_foreign_key(None, "jb_session", "jb_channel", ["channel_id"], ["id"])
    op.drop_column("jb_session", "bot_id")
    op.add_column("jb_turn", sa.Column("channel_id", sa.String(), nullable=True))
    op.drop_constraint("jb_turn_bot_id_fkey", "jb_turn", type_="foreignkey")
    op.create_foreign_key(None, "jb_turn", "jb_channel", ["channel_id"], ["id"])
    op.drop_column("jb_turn", "bot_id")
    op.add_column("jb_users", sa.Column("channel_id", sa.String(), nullable=True))
    op.add_column("jb_users", sa.Column("identifier", sa.String(), nullable=True))
    op.drop_constraint("jb_users_bot_id_fkey", "jb_users", type_="foreignkey")
    op.create_foreign_key(None, "jb_users", "jb_channel", ["channel_id"], ["id"])
    op.drop_column("jb_users", "phone_number")
    op.drop_column("jb_users", "bot_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "jb_users",
        sa.Column("bot_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "jb_users",
        sa.Column("phone_number", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "jb_users", type_="foreignkey")
    op.create_foreign_key(
        "jb_users_bot_id_fkey", "jb_users", "jb_bot", ["bot_id"], ["id"]
    )
    op.drop_column("jb_users", "identifier")
    op.drop_column("jb_users", "channel_id")
    op.add_column(
        "jb_turn", sa.Column("bot_id", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "jb_turn", type_="foreignkey")
    op.create_foreign_key(
        "jb_turn_bot_id_fkey", "jb_turn", "jb_bot", ["bot_id"], ["id"]
    )
    op.drop_column("jb_turn", "channel_id")
    op.add_column(
        "jb_session",
        sa.Column("bot_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "jb_session", type_="foreignkey")
    op.create_foreign_key(
        "jb_session_bot_id_fkey", "jb_session", "jb_bot", ["bot_id"], ["id"]
    )
    op.drop_column("jb_session", "channel_id")
    op.add_column(
        "jb_bot",
        sa.Column("phone_number", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "jb_bot",
        sa.Column(
            "channels",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_unique_constraint("jb_bot_phone_number_key", "jb_bot", ["phone_number"])
    op.drop_table("jb_channel")
    # ### end Alembic commands ###