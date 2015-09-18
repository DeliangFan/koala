from sqlalchemy import Table, Column, MetaData
from sqlalchemy import DateTime, Integer, Float, String, Text


meta = MetaData()

prices = Table('prices', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', String(length=255)),
        Column('resource_type', String(length=255)),
        Column('unit_price', Float),
        Column('region', String(length=255)),
        Column('description', String(length=255)),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

resources = Table('resources', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('uuid', String(length=36)),
        Column('name', String(length=255)),
        Column('status', String(length=255)),
        Column('consumption', Float),
        Column('tenant_id', String(length=36)),
        Column('region', String(length=255)),
        Column('resource_type', String(length=255)),
        Column('created_at', DateTime),
        Column('deleted', Integer),
        Column('description', String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

records = Table('records', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('resource_id', String(length=36)),
        Column('resource_status', String(length=255)),
        Column('start_at', DateTime),
        Column('end_at', DateTime),
        Column('unit_price', Float),
        Column('consumption', Float),
        Column('description', String(length=255)),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

tables = [prices, resources, records]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    for table in tables:
        try:
            table.create()
        except Exception:
            raise


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    for table in tables:
        try:
            table.drop()
        except Exception:
            raise
