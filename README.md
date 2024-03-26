# Sqlalchemy-OceanBase

OceanBase mysql tenant use pymysql to connect to OceanBase database.

See [OceanBase Document](https://en.oceanbase.com/docs/common-oceanbase-database-10000000000829751)

But the DDL of OceanBase is slightly different from MySQL, and user will get some warnings when reflecting metadata from OceanBase.

Alembic thus cannot work with OceanBase directly.

This package is a workaround to make Alembic work with OceanBase.

## Installation

```bash
pip install sqlalchemy-oceanbase
```

## Usage

```python
from sqlalchemy import create_engine

create_engine('msyql+oceanbase://user:password@host:port/dbname')
```
