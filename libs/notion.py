from typing import Dict, List

from notion_client import Client


class NotionClient:
    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.client = Client(auth=token)

    def _gen_data(self, name: str, assign: List[str], priority: str, status: str, tower_id: int, tower_url: str):
        return {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Assign": {
                    "multi_select": [{
                        "name": o
                    } for o in assign]
                },
                "Priority": {
                    "select": {
                        "name": priority
                    }
                },
                "Status": {
                    "select": {
                        "name": status
                    }
                },
                "Tower": {
                    "url": tower_url
                },
                "Tower ID": {
                    "number": tower_id
                }
            }
        }

    def create_task(self, name: str, assign: List[str], priority: str, status: str, tower_id: int, tower_url: str):
        data = self._gen_data(
            name=name, assign=assign,
            priority=priority, status=status,
            tower_id=tower_id, tower_url=tower_url
        )

        self.client.pages.create(**data)

    def update_task(self, page_id: str, name: str, assign: List[str], priority: str, status: str, tower_id: int, tower_url: str):
        if not page_id:
            return

        data = self._gen_data(
            name=name, assign=assign,
            priority=priority, status=status,
            tower_id=tower_id, tower_url=tower_url
        )
        self.client.pages.update(page_id=page_id, **data)

    def get_by_tower_id(self, tower_id: int):
        data = {
            "filter": {
                "property": "Tower ID",
                "number": {
                    "equals": tower_id
                }
            },
            "sorts": [
                {
                    "property": "Tower ID",
                    "direction": "ascending"
                }
            ]
        }
        return self.client.databases.query(database_id=self.database_id, **data)

    def update(self, properties: Dict):
        pass
