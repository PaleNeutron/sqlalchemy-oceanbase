# Sqlalchemy-OceanBase

[![](https://img.shields.io/pypi/v/sqlalchemy-oceanbase)](https://pypi.org/project/sqlalchemy-oceanbase/)
[![PyPI - License](https://img.shields.io/pypi/l/sqlalchemy-oceanbase)](LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/sqlalchemy-oceanbase)](https://pypi.org/project/sqlalchemy-oceanbase/)

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

engin = create_engine('msyql+oceanbase://user:password@host:port/dbname')
```


### Async model

```python
from sqlalchemy.ext.asyncio import create_async_engine

engin = create_async_engine('msyql+oceanbase://user:password@host:port/dbname')
```
