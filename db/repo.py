from typing import Optional, List
from uuid import UUID, uuid1

from sqlmodel import Session, select

from db.models.dish import Dish
from db.models.menu import Menu
from db.models.request_body import RequestBody, RequestDishBody
from db.models.submenu import Submenu


# -------------- menu block -------------------
def get_menu_by_id(id_: UUID, session: Session) -> Optional[Menu]:
    return session.execute(select(Menu).where(Menu.id == id_)).scalar()


def get_all_menus(session: Session) -> List[Menu]:
    return session.execute(select(Menu)).scalars().all()


def create_new_menu(body: RequestBody) -> Menu:
    return Menu(id=uuid1(), title=body.title, description=body.description)


# -------------- submenu block ----------------
def get_submenu_by_id(menu_id: UUID, id_: UUID, session: Session) -> Optional[Submenu]:
    return session.execute(
        select(Submenu).join(Menu).where(Menu.id == menu_id).where(Submenu.id == id_)).scalar()


def get_all_submenus_in_menu(menu_id: UUID, session: Session) -> List[Submenu]:
    return session.execute(select(Submenu).join(Menu).where(Menu.id == menu_id)).scalars().all()


def create_new_submenu(menu_id: UUID, body: RequestBody) -> Submenu:
    return Submenu(id=uuid1(), title=body.title, description=body.description, menu_id=menu_id)


# -------------- dash block ----------------
def get_dish_by_id(menu_id: UUID, submenu_id: UUID, id_: UUID, session: Session) -> Optional[Dish]:
    return session.execute(
        select(Dish).join(Submenu).join(Menu)
        .where(Menu.id == menu_id).where(Submenu.id == submenu_id).where(Dish.id == id_)
    ).scalar()


def get_all_dishes_in_submenu(menu_id: UUID, submenu_id: UUID, session: Session) -> List[Dish]:
    return session.execute(
        select(Dish).join(Submenu).join(Menu)
        .where(Menu.id == menu_id).where(Submenu.id == submenu_id)
    ).scalars().all()


def create_new_dish(menu_id: UUID, submenu_id: UUID, body: RequestDishBody) -> Dish:
    return Dish(id=uuid1(), title=body.title, description=body.description, price=body.price,
                menu_id=menu_id, submenu_id=submenu_id)
