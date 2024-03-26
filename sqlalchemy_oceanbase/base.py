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
from sqlalchemy.dialects.mysql import pymysql

from .reflection import OceanBaseTableDefinitionParser


class OceanBaseDialect(pymysql.MySQLDialect_pymysql):
    name = "oceanbase"

    @util.memoized_property
    def _tabledef_parser(self):
        """return the MySQLTableDefinitionParser, generate if needed.

        The deferred creation ensures that the dialect has
        retrieved server version information first.

        """
        preparer = self.identifier_preparer
        return OceanBaseTableDefinitionParser(self, preparer)
