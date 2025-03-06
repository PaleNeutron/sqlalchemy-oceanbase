import os
import warnings

from sqlalchemy import MetaData

from sqlalchemy_oceanbase.base import OceanBaseDialect


def test_reflection_no_warning():
    dialect = OceanBaseDialect()
    ddl = """CREATE TABLE `fund_manager_base_info` (
  `end_date` date NOT NULL,
  `fund_code` varchar(255) NOT NULL,
  `fund_name` varchar(255) DEFAULT NULL,
  `manager_id` varchar(255) NOT NULL,
  `manager_name` varchar(255) DEFAULT NULL,
  `fund_manager_comp` varchar(255) DEFAULT NULL,
  `is_inner` int(11) DEFAULT NULL,
  PRIMARY KEY (`end_date`, `fund_code`, `manager_id`),
  KEY `ix_fund_manager_base_info_end_date` (`end_date`) BLOCK_SIZE 16384 LOCAL,
  KEY `ix_fund_manager_base_info_fund_code` (`fund_code`) BLOCK_SIZE 16384 LOCAL,
  KEY `ix_fund_manager_base_info_manager_id` (`manager_id`) BLOCK_SIZE 16384 LOCAL,
  UNIQUE KEY `ix_user_email` (`email`) BLOCK_SIZE 16384 LOCAL
) DEFAULT CHARSET = utf8mb4 ROW_FORMAT = DYNAMIC COMPRESSION = 'zstd_1.3.8' REPLICA_NUM = 3 BLOCK_SIZE = 16384 USE_BLOOM_FILTER = FALSE TABLET_SIZE = 134217728 PCTFREE = 0
"""
    # dialect._tabledef_parser.parse(ddl, 'utf8')
    with warnings.catch_warnings(record=True) as record:
        state = dialect._tabledef_parser.parse(ddl, "utf8")
        assert len(state.keys) == 5
        assert len(record) == 0, "\n" + "\n".join(str(r.message) for r in record)


def test_reflection_online():
    url = os.getenv("OBDB", None)
    if url is None:
        return
    from sqlalchemy import create_engine

    engine = create_engine(url)
    meta = MetaData()
    meta.reflect(bind=engine)
    for t in meta.tables.values():
        print(f"Table: {t.name}: {t.schema}")
    assert "fund_manager_base_info" in meta.tables
