#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""SQLAlchemy models for App data"""

from oslo.config import cfg

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Float, Integer, String, Text
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
    """Price model"""

    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=255))
    resource_type = Column(String(length=255))
    unit_price = Column(Float)
    region = Column(String(length=255))
    description = Column(String(length=255))


class Ex(Base):
    """Represents a ex on App."""

    __tablename__ = 'exs'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36))
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
