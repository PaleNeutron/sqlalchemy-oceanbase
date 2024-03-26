import re
from sqlalchemy.dialects.mysql.reflection import MySQLTableDefinitionParser, _re_compile

class OceanBaseTableDefinitionParser(MySQLTableDefinitionParser):
    def __init__(self, dialect, preparer):
        MySQLTableDefinitionParser.__init__(self, dialect, preparer)

    def _prep_regexes(self):
        super()._prep_regexes()

        ### this block is copied from MySQLTableDefinitionParser._prep_regexes
        _final = self.preparer.final_quote
        quotes = dict(
            zip(
                ("iq", "fq", "esc_fq"),
                [
                    re.escape(s)
                    for s in (
                        self.preparer.initial_quote,
                        _final,
                        self.preparer._escape_identifier(_final),
                    )
                ],
            )
        )
        ### end of block

        self._re_key = _re_compile(
            r"  "
            r"(?:(?P<type>\S+) )?KEY"
            r"(?: +%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s)?"
            r"(?: +USING +(?P<using_pre>\S+))?"
            r" +\((?P<columns>.+?)\)"
            r"(?: +USING +(?P<using_post>\S+))?"
            r"(?: +(KEY_)?BLOCK_SIZE *[ =]? *(?P<keyblock>\S+))?"
            r"(?: +WITH PARSER +(?P<parser>\S+))?"
            r"(?: +COMMENT +(?P<comment>(\x27\x27|\x27([^\x27])*?\x27)+))?"
            r"(?: +/\*(?P<version_sql>.+)\*/ *)?"
            r",?$" % quotes
        )

        kw = quotes.copy()
        kw["on"] = "RESTRICT|CASCADE|SET NULL|NO ACTION"
        self._re_fk_constraint = _re_compile(
            r"  "
            r"CONSTRAINT +"
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +"
            r"FOREIGN KEY +"
            r"\((?P<local>[^\)]+?)\) REFERENCES +"
            r"(?P<table>%(iq)s[^%(fq)s]+%(fq)s"
            r"(?:\.%(iq)s[^%(fq)s]+%(fq)s)?) *"
            r"\((?P<foreign>(?:%(iq)s[^%(fq)s]+%(fq)s(?: *, *)?)+)\)"
            r"(?: +(?P<match>MATCH \w+))?"
            r"(?: +ON UPDATE (?P<onupdate>%(on)s))?"
            r"(?: +ON DELETE (?P<ondelete>%(on)s))?"
        ) % kw