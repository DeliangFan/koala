#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""SQLAlchemy models for App data"""

from oslo.config import cfg

from sqlalchemy import Column
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from koala.openstack.common.db.sqlalchemy import models

sql_opts = [cfg.StrOpt('mysql_engine', default='InnoDB', help='MySQL engine')]
cfg.CONF.register_opts(sql_opts)


class KoalaBase(models.TimestampMixin,
                  models.ModelBase):

    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

Base = declarative_base(cls=KoalaBase)


class Price(Base):
    """Price model."""

    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, nullable=False)
    resource_type = Column(String(length=255))
    unit_price = Column(Float)
    region = Column(String(length=255))
    description = Column(String(length=255))
    # NOTE(fandeliang) In fact, timestamp is not needed.
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Resource(Base):
    """Resource model."""
    __tablename__ = 'resources'

    # TBD(fandeliang) uuid or id
    id = Column(Integer, primary_key=True, nullable=False)
    resource_id = Column(String(length=255))
    resource_name = Column(String(length=255))
    status = Column(String(length=255))
    region = Column(String(length=255))
    content = Column(String(length=255))
    consumption = Column(Float)
    deleted = Column(Integer)
    tenant_id = Column(String(length=255))
    resource_type = Column(String(length=255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    description = Column(String(length=255))


class Record(Base):
    """Record model."""
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, nullable=False)
    resource_id = Column(String(length=255))
    consumption = Column(Float)
    unit_price = Column(Float)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    description = Column(String(length=255))
    # TBD(fandeliang) created_at and updated_at is not needed.
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
