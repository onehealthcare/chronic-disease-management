from typing import Dict, List, Optional

from broker.tower_sys import get_todo
from models.init_db import notion_client
from models.tower_sys.dataclass.api_data import TodoModel
from utils import logger as _logger


logger = _logger("broker.tower_sys.api")


def update_notion_task_by_tower_todo_id(todo_id: str, user_id: int):
    todo_info = get_todo(todo_id=todo_id, user_id=user_id)

    if not todo_info:
        logger.error(f"update_notion_task_by_tower_todo_id,get_todo_error,tower token expired - {todo_id}")
        return

    m = TodoModel.parse_obj(todo_info)

    # 其他不相关的不同步到 notion
    if not m.is_related_to_me:
        logger.warn(f"update_notion_task_by_tower_todo_id,sync fail,none of my business - {m.name} - {m.url}")
        return

    # notion 是否创建过任务
    notion_task = _get_notion_task_by_tower_id(tower_id=m.id)

    # 如果没有找到则创建
    if not notion_task:
        notion_client.create_task(
            name=m.name, assign=m.related_member,
            priority=m.priority, status=m.status,
            tower_id=m.id, tower_url=m.url
        )

    # 设置了暂停同步
    if notion_task.get("properties", {}).get("暂停同步", {}).get("checkbox"):
        logger.warn(f"update_notion_task_by_tower_todo_id,sync fail,pause status - {m.name} - {m.url}")
        return
    else:
        notion_client.update_task(
            page_id=notion_task.get("id", ""),
            name=m.name, assign=m.related_member,
            priority=m.priority, status=m.status,
            tower_id=m.id, tower_url=m.url
        )


def _get_notion_task_by_tower_id(tower_id: int) -> Dict:
    """
    {'object': 'list',
     'results': [{'object': 'page',
       'id': '0a0cf4bc-b6d9-4db8-b13d-b7371e8b618f',
       'created_time': '2021-08-25T14:18:00.000Z',
       'last_edited_time': '2021-08-25T14:18:00.000Z',
       'cover': None,
       'icon': None,
       'parent': {'type': 'database_id',
        'database_id': '5396afaf-db52-4ad0-b188-fb901c0e5ca7'},
       'archived': False,
       'properties': {'Status': {'id': '3E6J',
         'type': 'select',
         'select': {'id': '407b7fe1-ae05-4368-a6f2-0eb126ccc147',
          'name': 'Testing',
          'color': 'blue'}},
        'Last edited time': {'id': '<b^~',
         'type': 'last_edited_time',
         'last_edited_time': '2021-08-25T14:18:00.000Z'},
        'Date Created': {'id': 'DrOp',
         'type': 'created_time',
         'created_time': '2021-08-25T14:18:00.000Z'},
        'Assign': {'id': 'F$#]',
         'type': 'multi_select',
         'multi_select': [{'id': '6645c395-53c5-43f9-9cbd-eb3ee2681ed0',
           'name': 'tonghs',
           'color': 'brown'}]},
        '关联任务': {'id': 'GVft', 'type': 'rich_text', 'rich_text': []},
        'Desc': {'id': 'Zt\\J', 'type': 'rich_text', 'rich_text': []},
        'Tag': {'id': 'gFEV', 'type': 'multi_select', 'multi_select': []},
        'Tower': {'id': 'gK}<',
         'type': 'url',
         'url': 'https://tower.im/teams/158367/todos/93555/'},
        '周报模板': {'id': 'ln[r',
         'type': 'formula',
         'formula': {'type': 'string',
          'string': '- webhook 测试任务, [Tower](https://tower.im/teams/158367/todos/93555/),  @tonghs'}},
        '暂停同步': {'id': 'qt|n', 'type': 'checkbox', 'checkbox': False},
        'Priority': {'id': "rqJ'",
         'type': 'select',
         'select': {'id': 'f169b144-5fcc-4974-8080-0a310e4cf1f7',
          'name': 'normal',
          'color': 'default'}},
        'Tower ID': {'id': '}SAi', 'type': 'number', 'number': 93555},
        'Name': {'id': 'title',
         'type': 'title',
         'title': [{'type': 'text',
           'text': {'content': 'webhook 测试任务', 'link': None},
           'annotations': {'bold': False,
            'italic': False,
            'strikethrough': False,
            'underline': False,
            'code': False,
            'color': 'default'},
           'plain_text': 'webhook 测试任务',
           'href': None}]}},
       'url': 'https://www.notion.so/webhook-0a0cf4bcb6d94db8b13db7371e8b618f'}],
     'next_cursor': None,
     'has_more': False}
    :param tower_id:
    :return:
    """
    resp: Dict = notion_client.get_by_tower_id(tower_id=tower_id)
    results: List = resp.get("results", [])
    if not results:
        return {}

    task: Dict = results[0]
    _tower_id: Optional[int] = task.get("properties", {}).get("Tower ID", {}).get("number")
    if results and _tower_id is not None and tower_id == _tower_id:
        return task

    return {}
