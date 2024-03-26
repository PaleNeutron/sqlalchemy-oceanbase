import pytest
from sqlalchemy.dialects import registry

registry.register("mysql.oceanbase", "sqlalchemy_oceanbase.base", "OceanBaseDialect")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")
