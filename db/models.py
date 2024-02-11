from sqlalchemy import Identity, ForeignKey, text
from sqlalchemy.dialects.postgresql import TEXT, BIGINT, BOOLEAN, NUMERIC, DATE
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import expression, true
from sqlalchemy.types import DateTime
from typing import Annotated
from datetime import datetime


from db.base import Base

created_at = Annotated[datetime, mapped_column(
    DATE, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))]
intpk = Annotated[int, mapped_column(
    BIGINT, Identity(always=True), primary_key=True)]
bigint = Annotated[int, mapped_column(BIGINT)]
ttext = Annotated[str, mapped_column(TEXT)]


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Agencies(Base):
    __tablename__ = "agencies"

    agency_id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(nullable=False)
    tg_bot_id: Mapped[bigint]
    test_tg_bot: Mapped[bigint]


class Models(Base):
    __tablename__ = "models"

    model_id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(nullable=False)
    description: Mapped[ttext]


class Earnings(Base):
    __tablename__ = "earnings"

    earning_id: Mapped[intpk]
    shift_user_id: Mapped[bigint]
    confirm: Mapped[bool] = mapped_column(BOOLEAN, server_default=true())
    dirty: Mapped[float] = mapped_column(NUMERIC)


class AgencyModel(Base):
    __tablename__ = "agency_model"

    agency_id: Mapped[bigint] = mapped_column(
        ForeignKey('agencies.agency_id', ondelete='CASCADE'),
        primary_key=True)
    model_id: Mapped[bigint] = mapped_column(
        ForeignKey('models.model_id', ondelete='CASCADE'),
        primary_key=True)


class Fines(Base):
    __tablename__ = "fines"

    fine_id: Mapped[intpk]
    date_fine: Mapped[created_at]
    description: Mapped[ttext]
    amount: Mapped[float] = mapped_column(NUMERIC)
    user_id: Mapped[bigint] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'))


class Pages(Base):
    __tablename__ = "pages"

    page_id: Mapped[intpk]
    model_id: Mapped[bigint] = mapped_column(
        ForeignKey('models.model_id', ondelete='CASCADE'))
    vip: Mapped[bool] = mapped_column(BOOLEAN)
    sales_commision: Mapped[float] = mapped_column(NUMERIC)
    senior_id: Mapped[bigint] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'))
    number_operator_shift: Mapped[bigint] = mapped_column(
        server_default=ttext("0"))
    page_link: Mapped[ttext]

    # model = relationship("Models")


class Permissions(Base):
    __tablename__ = "permissions"

    permission_id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(unique=True)


class Roles(Base):
    __tablename__ = "roles"

    role_id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(unique=True)


class RolesPermissions(Base):
    __tablename__ = "roles_permissions"

    role_id: Mapped[bigint] = mapped_column(ForeignKey(
        'roles.role_id', ondelete='CASCADE'),
        primary_key=True)
    permission_id: Mapped[bigint] = mapped_column(ForeignKey(
        'permissions.permission_id', ondelete='CASCADE'),
        primary_key=True)


class Shifts(Base):
    __tablename__ = "shifts"

    shift_id: Mapped[intpk]
    date_shift: Mapped[created_at]
    page_time_period_id: Mapped[bigint] = mapped_column(ForeignKey(
        'pages_time_periods.page_time_period_id', ondelete='CASCADE'))


class ShiftsUsers(Base):
    __tablename__ = "shifts_users"

    shift_user_id: Mapped[intpk]
    operator_id: Mapped[bigint] = mapped_column(ForeignKey(
        'users.user_id', ondelete='CASCADE'))
    shift_id: Mapped[bigint] = mapped_column(ForeignKey(
        'shifts.shift_id', ondelete='CASCADE'))


class TimePeriods(Base):
    __tablename__ = "time_periods"

    time_period_id: Mapped[intpk]
    title: Mapped[ttext]


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[intpk]
    name: Mapped[ttext] = mapped_column(nullable=False)
    emoji: Mapped[ttext]
    status: Mapped[ttext] = mapped_column(default='AppliedWating')
    work_now: Mapped[bool] = mapped_column(
        BOOLEAN, default=False, nullable=False)
    wallet: Mapped[ttext]
    time_period_id: Mapped[bigint] = mapped_column(ForeignKey(
        'time_periods.time_period_id', ondelete='CASCADE'))
    role_id: Mapped[bigint] = mapped_column(
        ForeignKey('roles.role_id', ondelete='CASCADE'))
    manager_id: Mapped[bigint] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'))

    # manager = relationship("Users", remote_side=[user_id])
    # time_period = relationship("TimePeriods")
    # role = relationship("Roles")


class UsersAgencies(Base):
    __tablename__ = "users_agencies"

    user_id: Mapped[bigint] = mapped_column(ForeignKey(
        'users.user_id', ondelete='CASCADE'), primary_key=True)
    agency_id: Mapped[bigint] = mapped_column(ForeignKey(
        'agencies.agency_id', ondelete='CASCADE'), primary_key=True)


class UsersModels(Base):
    __tablename__ = "users_models"

    user_id: Mapped[bigint] = mapped_column(ForeignKey(
        'users.user_id', ondelete='CASCADE'), primary_key=True)
    model_id: Mapped[bigint] = mapped_column(ForeignKey(
        'models.model_id', ondelete='CASCADE'), primary_key=True)


class UserTg(Base):
    __tablename__ = "user_tg"

    user_tg_id: Mapped[intpk]
    user_id: Mapped[bigint] = mapped_column(ForeignKey(
        'users.user_id', ondelete='CASCADE'))
    tg_id: Mapped[bigint] = mapped_column(unique=True)


class PagesTimePeriod (Base):
    __tablename__ = "pages_time_periods"

    page_time_period_id: Mapped[intpk]
    time_period_id: Mapped[bigint] = mapped_column(
        ForeignKey('time_periods.time_period_id', ondelete="CASCADE"))
    page_id: Mapped[bigint] = mapped_column(
        ForeignKey('pages.page_id', ondelete="CASCADE"))
