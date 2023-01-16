from typing import List
from uuid import UUID

from sqlmodel import Field, Relationship

from db.models.request_body import RestaurantEntity
from db.models.dish import Dish


class Submenu(RestaurantEntity, table=True):
    menu_id: UUID = Field(foreign_key='menu.id')
    dishes: List["Dish"] = Relationship(sa_relationship_kwargs={"cascade": "delete"})

    @staticmethod
    def not_found() -> dict[str, str]:
        return {'detail': 'submenu not found'}

    def __repr__(self):
        return "".format(self.title, f" in menu: {self.menu_id}")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['dishes_count'] = len(self.dishes)
        return d
