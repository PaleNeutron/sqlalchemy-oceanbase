"""
File: base.py
File Created: Tuesday, 26th March 2024 8:57:43 am
Author: lv Junhong (lvjunhong@citics.com)
-----
Last Modified: Tuesday, 26th March 2024 8:58:10 am
Modified By: lv Junhong (lvjunhong@citics.com>)
-----
HISTORY:
"""

from sqlalchemy import util
from sqlalchemy.dialects.mysql import aiomysql, pymysql

from .reflection import OceanBaseTableDefinitionParser


class OceanBaseDialect(pymysql.MySQLDialect_pymysql):
    # not change dialect name, since it is a subclass of pymysql.MySQLDialect_pymysql
    # name = "oceanbase"
    supports_statement_cache = True

    @util.memoized_property
    def _tabledef_parser(self):
        """return the MySQLTableDefinitionParser, generate if needed.

        The deferred creation ensures that the dialect has
        retrieved server version information first.

        """
        preparer = self.identifier_preparer
        default_schema = self.default_schema_name
        return OceanBaseTableDefinitionParser(
            self, preparer, default_schema=default_schema
        )


class AsyncOceanBaseDialect(aiomysql.MySQLDialect_aiomysql):
    supports_statement_cache = True

    @util.memoized_property
    def _tabledef_parser(self):
        """return the MySQLTableDefinitionParser, generate if needed.

        The deferred creation ensures that the dialect has
        retrieved server version information first.

        """
        preparer = self.identifier_preparer
        default_schema = self.default_schema_name
        return OceanBaseTableDefinitionParser(
            self, preparer, default_schema=default_schema
        )
