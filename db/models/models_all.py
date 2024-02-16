from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import BOOLEAN, NUMERIC
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import expression, false
from sqlalchemy.types import DateTime


from db.models.types import intbigint, intpk, strtext, created_at
from db.models.base import Base


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Earnings(Base):
    __tablename__ = "earnings"

    earning_id: Mapped[intpk]
    shift_user_id: Mapped[intbigint]  # FK
    confirm: Mapped[bool] = mapped_column(BOOLEAN, default=false())
    dirty: Mapped[float] = mapped_column(NUMERIC)


class Fines(Base):
    __tablename__ = "fines"

    fine_id: Mapped[intpk]
    date_fine: Mapped[created_at]
    description: Mapped[strtext] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(NUMERIC)
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )


class Pages(Base):
    __tablename__ = "pages"

    page_id: Mapped[intpk]
    model_id: Mapped[intbigint] = mapped_column(
        ForeignKey("models.model_id", ondelete="CASCADE")
    )
    vip: Mapped[bool] = mapped_column(BOOLEAN)
    sales_commision: Mapped[float] = mapped_column(NUMERIC)
    senior_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True
    )
    number_operator_shift: Mapped[intbigint] = mapped_column(server_default=text("0"))
    page_link: Mapped[strtext]

    # model = relationship("Models")


class Shifts(Base):
    __tablename__ = "shifts"

    shift_id: Mapped[intpk]
    date_shift: Mapped[created_at]
    page_time_period_id: Mapped[intbigint] = mapped_column(
        ForeignKey("pages_time_periods.page_time_period_id", ondelete="CASCADE")
    )


class ShiftsUsers(Base):
    __tablename__ = "shifts_users"

    shift_user_id: Mapped[intpk]
    operator_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    shift_id: Mapped[intbigint] = mapped_column(
        ForeignKey("shifts.shift_id", ondelete="CASCADE")
    )


# class TimePeriods(Base):
#     __tablename__ = "time_periods"

#     time_period_id: Mapped[intpk]
#     title: Mapped[ttext]


# class Users(Base):
#     __tablename__ = "users"

#     user_id: Mapped[intpk]
#     name: Mapped[strtext]
#     emoji: Mapped[strtext] = mapped_column(nullable=True)
#     status: Mapped[strtext] = mapped_column(default="AppliedWating")
#     work_now: Mapped[bool] = mapped_column(BOOLEAN, default=False)
#     wallet: Mapped[strtext] = mapped_column(nullable=True)
#     time_period_id: Mapped[intbigint] = mapped_column(
#         ForeignKey("time_periods.time_period_id", ondelete="CASCADE"), nullable=True
#     )
#     role_id: Mapped[intbigint] = mapped_column(
#         ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=True
#     )
#     manager_id: Mapped[intbigint] = mapped_column(
#         ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True
#     )

#     # manager = relationship("Users", remote_side=[user_id])
#     # time_period = relationship("TimePeriods")
#     # role = relationship("Roles")


class UsersAgencies(Base):
    __tablename__ = "users_agencies"

    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    agency_id: Mapped[intbigint] = mapped_column(
        ForeignKey("agencies.agency_id", ondelete="CASCADE"), primary_key=True
    )


class UsersModels(Base):
    __tablename__ = "users_models"

    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True
    )
    model_id: Mapped[intbigint] = mapped_column(
        ForeignKey("models.model_id", ondelete="CASCADE"), primary_key=True
    )


class UserTg(Base):
    __tablename__ = "user_tg"

    user_tg_id: Mapped[intpk]
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    tg_id: Mapped[intbigint] = mapped_column(unique=True)


class PagesTimePeriod(Base):
    __tablename__ = "pages_time_periods"

    page_time_period_id: Mapped[intpk]
    time_period_id: Mapped[intbigint] = mapped_column(
        ForeignKey("time_periods.time_period_id", ondelete="CASCADE")
    )
    page_id: Mapped[intbigint] = mapped_column(
        ForeignKey("pages.page_id", ondelete="CASCADE")
    )
