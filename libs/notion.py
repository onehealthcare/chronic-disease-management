from typing import Dict, List

from notion_client import Client


class NotionClient:
    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.client = Client(auth=token)

    def create_task(self, name: str, assign: List[str], priority: str, status: str, tower_id: int, tower_url: str):
        data = {
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
        self.client.pages.create(**data)

    def get_by_tower_id(self, tower_id: int):
        pass

    def sync_flag(self) -> bool:
        return False

    def update(self, properties: Dict):
        pass
