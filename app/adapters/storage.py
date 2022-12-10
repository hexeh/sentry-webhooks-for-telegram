from typing import Any, List, Optional

from environs import Env
from sqlalchemy import create_engine, event, exc

from app.client import SimpleStorage


class MapperStorage(SimpleStorage):
    def get_entity_by_key(self, entity: Any, key: Any) -> Any:
        with self.session.begin() as session:
            result = session.query(entity).get(key)
        return result

    def get_entities_by_chat(
        self, entity: Any, chat_id: int
    ) -> Optional[List[Any]]:
        with self.session.begin() as session:
            try:
                result = (
                    session.query(entity)
                    .filter(entity.chat_id == chat_id)
                    .all()
                )
            except exc.NoResultFound:
                result = None
        return result


env = Env()

STORAGE_NAME = env.str("STORAGE_DB_NAME", default="sentry_telegram_service")
STORAGE_ENGINE = create_engine(f"sqlite:///{STORAGE_NAME}.db")


@event.listens_for(STORAGE_ENGINE, "first_connect")
def schema_attach(dbapi_connection, connection_record):
    dbapi_connection.execute(
        f"ATTACH DATABASE '{STORAGE_NAME}.db' AS {STORAGE_NAME}"
    )


STORAGE = MapperStorage(engine=STORAGE_ENGINE)
