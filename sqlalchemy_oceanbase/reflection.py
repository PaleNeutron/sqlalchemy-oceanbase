import re

from sqlalchemy.dialects.mysql.reflection import MySQLTableDefinitionParser, _re_compile


class OceanBaseTableDefinitionParser(MySQLTableDefinitionParser):
    def __init__(self, dialect, preparer, *, default_schema=None):
        MySQLTableDefinitionParser.__init__(self, dialect, preparer)
        self.default_schema = default_schema

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
                strict=False,
            )
        )
        ### end of block

        self._re_key = _re_compile(
            r"  "
            r"(?:(?P<type>\S+) )?KEY"
            r"(?: +{iq}(?P<name>(?:{esc_fq}|[^{fq}])+){fq})?"
            r"(?: +USING +(?P<using_pre>\S+))?"
            r" +\((?P<columns>.+?)\)"
            r"(?: +USING +(?P<using_post>\S+))?"
            r"(?: +(KEY_)?BLOCK_SIZE *[ =]? *(?P<keyblock>\S+) *(LOCAL)?)?"
            r"(?: +WITH PARSER +(?P<parser>\S+))?"
            r"(?: +COMMENT +(?P<comment>(\x27\x27|\x27([^\x27])*?\x27)+))?"
            r"(?: +/\*(?P<version_sql>.+)\*/ *)?"
            r",?$".format(iq=quotes["iq"], esc_fq=quotes["esc_fq"], fq=quotes["fq"])
        )

        kw = quotes.copy()
        kw["on"] = "RESTRICT|CASCADE|SET NULL|NO ACTION"
        self._re_fk_constraint = _re_compile(
            r"  "
            r"CONSTRAINT +"
            r"{iq}(?P<name>(?:{esc_fq}|[^{fq}])+){fq} +"
            r"FOREIGN KEY +"
            r"\((?P<local>[^\)]+?)\) REFERENCES +"
            r"(?P<table>{iq}[^{fq}]+{fq}"
            r"(?:\.{iq}[^{fq}]+{fq})?) *"
            r"\((?P<foreign>(?:{iq}[^{fq}]+{fq}(?: *, *)?)+)\)"
            r"(?: +(?P<match>MATCH \w+))?"
            r"(?: +ON UPDATE (?P<onupdate>{on}))?"
            r"(?: +ON DELETE (?P<ondelete>{on}))?".format(
                iq=quotes["iq"], esc_fq=quotes["esc_fq"], fq=quotes["fq"], on=kw["on"]
            )
        )

    def _parse_constraints(self, line):
        """Parse a CONSTRAINT line."""
        ret = super()._parse_constraints(line)
        # OceanBase show schema/database in foreign key constraint ddl, even if the schema/database is the default one
        if ret:
            type, spec = ret
            if type == "fk_constraint":
                if len(spec["table"]) == 2 and spec["table"][0] == self.default_schema:
                    spec["table"] = spec["table"][1:]
        return ret
