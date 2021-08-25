from typing import List, Optional

from pydantic import BaseModel


class MemberModel(BaseModel):
    guid: str
    nickname: str


class TodoModel(BaseModel):
    guid: str
    title: str
    updated_at: str
    handler: MemberModel
    due_at: Optional[str]
    assignee: MemberModel
    labels: List[str]
    priority: str


class ProjectModel(BaseModel):
    guid: str
    name: str


class TodoListModel(BaseModel):
    guid: str
    title: str
    desc: str


class TodoPayloadDataModel(BaseModel):
    todo: TodoModel
    project: ProjectModel
    todolist: TodoListModel


class TodoPayloadModel(BaseModel):
    """
    {
        "action":"updated",
        "data":{
            "project":{
                "guid":"7a59cf752983fa71167478091a42276c",
                "name":"需求池"
            },
            "todo":{
                "guid":"f32a14e8e1892f7e098f0216b1fbf2fe",
                "title":"webhook 测试任务",
                "updated_at":"2021-08-25T05:27:48.327Z",
                "handler":{
                    "guid":"6954901637064852b24a2506f0c02e97",
                    "nickname":"仝华帅"
                },
                "due_at":"None",
                "assignee":{
                    "guid":"6954901637064852b24a2506f0c02e97",
                    "nickname":"仝华帅"
                },
                "labels":[

                ],
                "priority":"normal",
                "parent":{

                }
            },
            "todolist":{
                "guid":"ae9c619e293e3dc06e3c25bbc770231e",
                "title":"增值",
                "desc":""
            }
        }
    }
    """
    action: str
    data: TodoPayloadDataModel
