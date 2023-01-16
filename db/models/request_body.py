from typing import Optional
from uuid import UUID, uuid1

from sqlmodel import SQLModel, Field, Session


class RequestBody(SQLModel):
    title: str
    description: str


class RestaurantEntity(RequestBody):
    id: Optional[UUID] = Field(default=uuid1(), primary_key=True)

    def add_to_db(self, session: Session) -> None:
        session.add(self)
        session.commit()

    def delete_from_db(self, session: Session) -> None:
        session.delete(self)
        session.commit()

    def update_in_db(self, body: RequestBody, session: Session):
        self.title = body.title
        self.description = body.description
        session.add(self)
        session.commit()
        session.refresh(self)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'title': self.title, 'description': self.description}


class RequestDishBody(RequestBody):
    price: float
