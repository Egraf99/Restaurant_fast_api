from typing import List

from sqlmodel import Relationship

from db.models.request_body import RestaurantEntity
from db.models.submenu import Submenu


class Menu(RestaurantEntity, table=True):
    submenus: List["Submenu"] = Relationship(sa_relationship_kwargs={"cascade": "delete"})

    def get_dishes(self):
        # из каждого Submenu в List[Submenu] берем List[Dish] -> получается List[List[Dish]]
        # преобразуем List[List[Dish]] в List[Dish]
        return [dish for sub in self.submenus for dish in sub.dishes]

    def __repr__(self):
        return self.title

    @staticmethod
    def not_found() -> dict:
        return {'detail': 'menu not found'}

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['submenus_count'] = len(self.submenus)
        d['dishes_count'] = len(self.get_dishes())
        return d
