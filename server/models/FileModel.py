from .db import db, BaseModel


class FileModel(BaseModel):
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    url = db.Column(db.String)

    def json(self) -> str:
        return {
            "id": self.id,
            "filename": self.filename,
            "url": self.url
        }
