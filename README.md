# Restaurant API
## Для запуска
1. Склонировать репозиторий
```commandline
git clone https://github.com/Egraf99/Restaurant_fast_api
```
 
2. Установить зависимости
```commandline
pip install -r requirements.txt
```
3. Установить адаптер для конкретной базы данных. Например:
```commandline
pip install psycopg2
```

4. Указать URL для базы данных в файле *_restaurant.env_*. Например:
```text
DATABASE_URL=postgresql://postgres:@localhost:5432/postgres
```

5. Запустить main.py
```commandline
python main.py
```
