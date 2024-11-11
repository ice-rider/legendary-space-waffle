from __future__ import annotations

from .db import db, BaseModel


class CommentModel(BaseModel):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    username = db.Column(db.String)
    message = db.Column(db.String)

    def json(self) -> str:
        return {
            "id": self.id,
            "username": self.username,
            "message": self.message
        }

    @classmethod
    def get_by_card_id(cls, card_id) -> list[CommentModel] | None:
        return cls.query.filter_by(card_id=card_id).all()
