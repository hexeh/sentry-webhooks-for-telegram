from typing import Any

from sqlalchemy.engine import Engine, ResultProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker
from sqlalchemy.schema import MetaData


class SimpleStorage:
    # todo: add async engines support

    def __init__(self, engine: Engine, schema: str = None):
        self.engine = engine
        self.schema = schema
        self.metadata: MetaData = MetaData(
            bind=self.engine, schema=self.schema, quote_schema=self.schema
        )
        self.base = declarative_base(bind=self.engine, metadata=self.metadata)

    @property
    def session(self):
        return sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_all(self) -> None:
        self.base.metadata.create_all()

    def drop_all(self) -> None:
        self.base.metadata.drop_all()

    def execute(self, text: str) -> ResultProxy:
        return self.engine.execute(text)

    def get_all(self, entity: Any) -> Any:
        with self.session.begin() as session:
            result = session.query(entity).all()
        return result

    def query(self, *args, **kwargs) -> query.Query:
        with self.session.begin() as session:
            result = session.query(*args, **kwargs)
        return result

    def add_entity(self, entity: Any, expunge: bool = False):
        with self.session.begin() as session:
            try:
                session.add(entity)
            except:  # noqa
                session.rollback()
            else:
                session.commit()
            if expunge:
                session.expunge()
