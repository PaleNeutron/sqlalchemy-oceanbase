from sqlalchemy import create_engine


def test_create_engine():
    create_engine("mysql+oceanbase://root:root@localhost:3306/strategy")
