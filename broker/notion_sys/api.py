from broker.tower_sys import get_todo
from models.init_db import notion_client
from models.tower_sys.dataclass.api_data import TodoModel


def update_notion_task_by_tower_todo_id(todo_id: str, user_id: int):
    todo_info = get_todo(todo_id=todo_id, user_id=user_id)
    m = TodoModel.parse_obj(todo_info)
    notion_client.create_task(
        name=m.name, assign=m.related_member,
        priority=m.priority, status=m.status,
        tower_id=m.id, tower_url=m.url
    )
