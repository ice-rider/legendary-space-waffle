from __future__ import annotations

from flask.typing import AppOrBlueprintKey
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseModel(db.Model):  # type: ignore
    __abstract__ = True

    def __str__(self) -> str:
        return str(self.json())

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: int) -> BaseModel | None:
        return cls.query.filter_by(id=id).first()
