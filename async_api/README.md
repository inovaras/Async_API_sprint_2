# Read-Only API для доступа к фильмам, жанрам и персонам.

### Заметки
Все чтение идет из elasticsearch.
Поэтому нет полей created, modified.

Данные в elasticsearch попадают через ETL с 3го спринта (new_admin_panel_sprint_3)

models.Film нужен для валидации данных из elasticsearch.
api.v1.film.Film - DTO, трансформирует данные из models.Film в данные, которые должен увидеть пользователь через API.

Чтобы решить ошибку валидации отсутствующего поля - добавь default=None в поле модели.
```python
film_link: str | None = Field(default=None)
```
Это же применимо и к полям, которые отсутствуют в индексе.

# Вопросы
После смены маппинга надо очистить индекс?
Как персону разбить на ИМЯ и ФАМИЛИЮ - no
Что с сущностями Актер, Директор, Сценарист если они == Role(id, name) (films -> DTO) - no

Как связать lru_cache() с нашим кешем, который удаляется по времени.

#TODO
1) написать скрипт развертывания (создание сети, volumes)
2) use admin-etl-process by python-alpine
3) при изменении маппинга надо удалить данные в индексе и пересоздать индекс.

match
https://www.mo4tech.com/elasticsearch-use-boolean-queries-to-improve-search-relevance.html

OR, AND, NOT
https://stackoverflow.com/questions/28538760/elasticsearch-bool-query-combine-must-with-or


Найти id в одном из списков. ```should == OR```, ```path:название списка```,<br>
```term == точное соответствие```.<br>
```{"directors.id": person.id} == key:value```<br>
```python
{
"bool": {
    "should": [
        {"nested": {"path": "directors", "query": {"term": {"directors.id": person.id}}}},
        {"nested": {"path": "writers", "query": {"term": {"writers.id": person.id}}}},
        {"nested": {"path": "actors", "query": {"term": {"actors.id": person.id}}}},
    ]
    }
}
```
### Results
1) есть кеширование
2) есть кеширование по id и по поиску, т.е кэшируются все эндпоинты.
3) нет кеширования при сортировке - добавить.
4) не используется dry.
5) надо перенести много классов из API в utils
6) заменить составление ключа на page и per_page