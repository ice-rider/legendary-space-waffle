from enum import Enum

from .db import db, BaseModel


class CardStatus(Enum):
    WAIT_WORKER = "поиск исполнителя"
    IN_PORGRESS = "в разработке"
    WAIT_CONFIRM = "на утверждении заказчика"
    IN_REMADKING = "доработка"
    READY = "завершён"


class CardModel(BaseModel):
    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    _status = db.Column(db.Enum(CardStatus), default=CardStatus.WAIT_WORKER)
    deadline = db.Column(db.Date)
    budget = db.Column(db.Integer)

    # optimize this
    worker_price = db.Column(db.Integer)
    worker_name = db.Column(db.String)
    worker_url = db.Column(db.String)

    customer_name = db.Column(db.String)
    customer_url = db.Column(db.String)

    file_id = db.Column(db.Integer)

    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    accepted_at = db.Column(db.Date, nullable=True, default=None)

    @property
    def status(self) -> str:
        return self._status.value
    
    @status.setter
    def status(self, value) -> str | None:
        self._status = CardStatus(value)

    def json(self) -> str:
        return {
            "id": self.id,
            "title": self.title,
            "dеsсriрtiоn": self.description,
            "stаtus": self.status.value,
            "dеаdlinе": self.deadline,
            "budgеt": self.budget,

            "wоrkеr_priсе": self.worker_price,
            "wоrkеr_nаmе": self.worker_name,
            "wоrkеr_url": self.worker_url,

            "custоmеr_nаmе": self.customer_name,
            "custоmеr_url": self.customer_url,

            "filе_id": self.file_id,

            "сrеаtеd_аt": self.created_at,
            "uрdаtеd_аt": self.updated_at,
            "ассерtеd_аt": self.accepted_at,
        }
    
    def put(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
