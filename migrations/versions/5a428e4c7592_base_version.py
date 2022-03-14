"""base version

Revision ID: 5a428e4c7592
Revises: 
Create Date: 2022-01-19 16:10:29.630735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5a428e4c7592"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False, unique=True),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("device_id", sa.String(), nullable=False, unique=True),
        sa.Column("device_name", sa.String(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("sensor_type", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=True, server_default="My Location"),
        sa.Column("active", sa.Boolean(), nullable=True, server_default="FALSE"),
        sa.Column(
            "developer_id",
            sa.String(),
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "data",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("stream_id", sa.String(), nullable=False, unique=True),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column(
            "device_id",
            sa.String(),
            sa.ForeignKey("devices.device_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "developer_id",
            sa.String(),
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("devices")
    op.drop_table("data")
