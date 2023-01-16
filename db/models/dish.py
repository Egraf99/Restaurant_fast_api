from uuid import UUID

from sqlmodel import Field, Session

from db.models.request_body import RequestDishBody, RestaurantEntity


class Dish(RestaurantEntity, RequestDishBody, table=True):
    submenu_id: UUID = Field(foreign_key='submenu.id')

    @staticmethod
    def not_found() -> dict[str, str]:
        return {'detail': 'dish not found'}

    def __repr__(self):
        return "".format(self.title, f" in submenu: {self.submenu_id}", f" with price: {self.price}")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['price'] = str(self.price)
        return d

    def update_in_db(self, body: RequestDishBody, session: Session):
        self.price = body.price
        super().update_in_db(body, session)

