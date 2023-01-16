import os
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session

from db.db import init_db, get_session
from db.models.dish import Dish
from db.models.menu import Menu
from db.models.request_body import RequestBody, RequestDishBody
from db.models.submenu import Submenu
from db.repo import create_new_menu, get_all_menus, get_menu_by_id, create_new_submenu, get_all_submenus_in_menu, \
    get_submenu_by_id, create_new_dish, get_all_dishes_in_submenu, get_dish_by_id

HOME_URL = "/api/v1"

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


# ---------- menu block ------------
@app.post(HOME_URL + "/menus")
def create_menu(body: RequestBody, session: Session = Depends(get_session)) -> JSONResponse:
    menu = create_new_menu(body)
    menu.add_to_db(session)
    return JSONResponse(content=menu.to_dict(), status_code=201)


@app.get(HOME_URL + "/menus")
def get_menus(session: Session = Depends(get_session)) -> JSONResponse:
    list_of_menus = get_all_menus(session)
    return JSONResponse(content=[menu.to_dict() for menu in list_of_menus], status_code=200)


@app.get(HOME_URL + "/menus/{menu_id}")
def get_menu(menu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    search_menu = get_menu_by_id(UUID(menu_id), session)
    if search_menu is None:
        return JSONResponse(content=Menu.not_found(), status_code=404)
    else:
        return JSONResponse(content=search_menu.to_dict(), status_code=200)


@app.patch(HOME_URL + "/menus/{menu_id}")
def update_menu(menu_id: str, body: RequestBody, session: Session = Depends(get_session)) -> JSONResponse:
    menu = get_menu_by_id(UUID(menu_id), session)
    if menu is None:
        return JSONResponse(content=Menu.not_found(), status_code=404)
    menu.update_in_db(body, session)
    return JSONResponse(content=menu.to_dict(), status_code=200)


@app.delete(HOME_URL + "/menus/{menu_id}")
def delete_menu(menu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    menu = get_menu_by_id(UUID(menu_id), session)
    if menu is None:
        return JSONResponse(content=Menu.not_found(), status_code=404)

    menu.delete_from_db(session)
    return JSONResponse(content=[], status_code=200)


# ---------- submenu block ------------
@app.post(HOME_URL + "/menus/{menu_id}/submenus")
def create_submenu(menu_id: str, body: RequestBody, session: Session = Depends(get_session)) -> JSONResponse:
    menu = get_menu_by_id(UUID(menu_id), session)
    if menu is None:
        return JSONResponse(content=Menu.not_found(), status_code=404)

    submenu = create_new_submenu(UUID(menu_id), body)
    submenu.add_to_db(session)
    return JSONResponse(content=submenu.to_dict(), status_code=201)


@app.get(HOME_URL + "/menus/{menu_id}/submenus")
def get_submenus(menu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    list_of_submenus = get_all_submenus_in_menu(UUID(menu_id), session)
    return JSONResponse(content=[submenu.to_dict() for submenu in list_of_submenus], status_code=200)


@app.get(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: str, submenu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    submenu = get_submenu_by_id(UUID(menu_id), UUID(submenu_id), session)
    if submenu is None:
        return JSONResponse(content=Submenu.not_found(), status_code=404)
    else:
        return JSONResponse(content=submenu.to_dict(),
                            status_code=200)


@app.patch(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}")
def update_submenu(menu_id: str, submenu_id: str, body: RequestBody,
                   session: Session = Depends(get_session)) -> JSONResponse:
    submenu = get_submenu_by_id(UUID(menu_id), UUID(submenu_id), session)

    if submenu is None:
        return JSONResponse(content=Submenu.not_found(), status_code=404)

    submenu.update_in_db(body, session)
    return JSONResponse(
        content=submenu.to_dict(),
        status_code=200)


@app.delete(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    submenu = get_submenu_by_id(UUID(menu_id), UUID(submenu_id), session)

    if submenu is None:
        return JSONResponse(content=Submenu.not_found(), status_code=404)
    submenu.delete_from_db(session)
    return JSONResponse(content=[], status_code=200)


# ---------- dish block ---------------
@app.post(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes")
def create_dish(menu_id: str, submenu_id: str, body: RequestDishBody,
                session: Session = Depends(get_session)) -> JSONResponse:
    menu = get_menu_by_id(UUID(menu_id), session)
    if menu is None:
        return JSONResponse(content=Menu.not_found(), status_code=404)

    submenu = get_submenu_by_id(UUID(menu_id), UUID(submenu_id), session)
    if submenu is None:
        return JSONResponse(content=Submenu.not_found(), status_code=404)

    dash = create_new_dish(UUID(menu_id), UUID(submenu_id), body)
    dash.add_to_db(session)
    return JSONResponse(content=dash.to_dict(), status_code=201)


@app.get(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(menu_id: str, submenu_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    list_of_dishes = get_all_dishes_in_submenu(UUID(menu_id), UUID(submenu_id), session)
    return JSONResponse(content=[dash.to_dict() for dash in list_of_dishes], status_code=200)


@app.get(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(menu_id: str, submenu_id: str, dish_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    dish = get_dish_by_id(UUID(menu_id), UUID(submenu_id), UUID(dish_id), session)
    if dish is None:
        return JSONResponse(content=Dish.not_found(), status_code=404)
    else:
        return JSONResponse(content=dish.to_dict(),
                            status_code=200)


@app.patch(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def update_dash(menu_id: str, submenu_id: str, dish_id: str, body: RequestDishBody,
                session: Session = Depends(get_session)) -> JSONResponse:
    dish = get_dish_by_id(UUID(menu_id), UUID(submenu_id), UUID(dish_id), session)

    if dish is None:
        return JSONResponse(content=Dish.not_found(), status_code=404)

    dish.update_in_db(body, session)
    return JSONResponse(content=dish.to_dict(), status_code=200)


@app.delete(HOME_URL + "/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, session: Session = Depends(get_session)) -> JSONResponse:
    dish = get_dish_by_id(UUID(menu_id), UUID(submenu_id), UUID(dish_id), session)

    if dish is None:
        return JSONResponse(content=Dish.not_found(), status_code=404)

    dish.delete_from_db(session)
    return JSONResponse(content=[], status_code=200)


def write_env(path_file: str):
    """
    Записывает в окружение переменные из переданного файла (в формате key=value).
    Комментарии, начинающиеся с символа # игнорируются.
    """
    with open(path_file, 'r') as env_file:
        for line in env_file.readlines():
            if line.strip().startswith("#"): continue
            key, value = line.strip().split('=')
            os.environ[key] = value


if __name__ == "__main__":
    write_env('restaurant.env')
    uvicorn.run("main:app", port=8000, reload=True)
