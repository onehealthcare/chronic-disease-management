"""
demo:
{
   "data":{
      "id":"f32a14e8e1892f7e098f0216b1fbf2fe",
      "type":"todos",
      "attributes":{
         "team_wide_id":93555,
         "content":"webhook 测试任务",
         "desc":"<p>tes</p>",
         "is_active":true,
         "is_completed":false,
         "priority":"normal",
         "start_at":"None",
         "due_at":"None",
         "closed_at":"None",
         "created_at":"2021-08-23T23:53:18.000+08:00",
         "updated_at":"2021-08-25T14:02:49.240+08:00",
         "labels":[
            "需求"
         ]
      },
      "relationships":{
         "project":{
            "data":{
               "id":"7a59cf752983fa71167478091a42276c",
               "type":"projects"
            }
         },
         "todolist":{
            "data":{
               "id":"ae9c619e293e3dc06e3c25bbc770231e",
               "type":"todolists"
            }
         },
         "creator":{
            "data":{
               "id":"6954901637064852b24a2506f0c02e97",
               "type":"members"
            }
         },
         "assignee":{
            "data":{
               "id":"6954901637064852b24a2506f0c02e97",
               "type":"members"
            }
         },
         "closer":{
            "data":"None"
         },
         "parent":{
            "data":"None"
         },
         "custom_field_value":{
            "data":{
               "id":"10470990",
               "type":"todos_custom_field_values"
            }
         },
         "sub_todos":{
            "data":[

            ]
         },
         "comments":{
            "data":[
               {
                  "id":"4d8527ece108fd02c00d34d567eaf02c",
                  "type":"comments"
               },
               {
                  "id":"63393101b7e180164c0c072a65f384e8",
                  "type":"comments"
               }
            ]
         },
         "todolists":{
            "data":[
               {
                  "id":"ae9c619e293e3dc06e3c25bbc770231e",
                  "type":"todolists"
               }
            ]
         },
         "attachments":{
            "data":[

            ]
         }
      }
   },
   "included":[
      {
         "id":"7a59cf752983fa71167478091a42276c",
         "type":"projects",
         "attributes":{
            "name":"需求池",
            "is_archived":false
         }
      },
      {
         "id":"ae9c619e293e3dc06e3c25bbc770231e",
         "type":"todolists",
         "attributes":{
            "name":"增值",
            "is_active":true,
            "is_archived":false,
            "is_default":false
         },
         "relationships":{
            "project":{
               "data":{
                  "id":"7a59cf752983fa71167478091a42276c",
                  "type":"projects"
               }
            }
         }
      },
      {
         "id":"6954901637064852b24a2506f0c02e97",
         "type":"members",
         "attributes":{
            "nickname":"仝华帅",
            "is_active":true,
            "gavatar":"https://avatar-alioss.tower.im/8f85409d34be4ea282a38e7b8990d251?t=1629870800",
            "role":"admin"
         }
      },
      {
         "id":"10470990",
         "type":"todos_custom_field_values",
         "attributes":{
            "custom_fields":{
               "select_512rDWZJ":{
                  "name":"进展状态",
                  "value":"未启动",
                  "field_type":"select"
               },
               "member_h6VnmPJa":{
                  "name":"相关人",
                  "value":[
                     "6954901637064852b24a2506f0c02e97"
                  ],
                  "field_type":"member"
               },
               "boolean_VbZW57UQ":{
                  "name":"是否延期",
                  "value":"None",
                  "field_type":"boolean"
               },
               "multi_select_nD8JTb3e":{
                  "name":"功能",
                  "value":[
                     "广告"
                  ],
                  "field_type":"multi_select"
               }
            }
         }
      },
      {
         "id":"4d8527ece108fd02c00d34d567eaf02c",
         "type":"comments",
         "attributes":{
            "content":"<p>hh</p>",
            "created_at":"2021-08-25T01:14:33.000+08:00",
            "updated_at":"2021-08-25T01:14:33.833+08:00"
         },
         "relationships":{
            "creator":{
               "data":{
                  "id":"6954901637064852b24a2506f0c02e97",
                  "type":"members"
               }
            },
            "attachments":{
               "data":[

               ]
            }
         }
      },
      {
         "id":"63393101b7e180164c0c072a65f384e8",
         "type":"comments",
         "attributes":{
            "content":"<p><a class=\"tr-mention\" href=\"/members/6954901637064852b24a2506f0c02e97\" rel=\"nofollow\">@仝华帅</a> huashuai\\xa0</p>",
            "created_at":"2021-08-25T01:14:46.000+08:00",
            "updated_at":"2021-08-25T01:14:46.806+08:00"
         },
         "relationships":{
            "creator":{
               "data":{
                  "id":"6954901637064852b24a2506f0c02e97",
                  "type":"members"
               }
            },
            "attachments":{
               "data":[

               ]
            }
         }
      }
   ],
   "jsonapi":{
      "version":"1.0"
   }
}
"""
from typing import Dict, List, Optional, Union

from config import TOWER_TEAM_ID
from models.tower_sys.const import (
    TaskPriority,
    TaskStatus,
    TaskTowerPriorityMap,
    TaskTowerStatusMap,
    TowerStatus,
    TowerUserMap,
    me,
)
from pydantic import BaseModel


class IncludedAttribute(BaseModel):
    name: str
    is_active: bool
    is_archived: bool
    is_default: bool

    nickname: str
    gavatar: str
    role: str

    content: str
    created_at: str
    updated_at: str


class IncludedProject(BaseModel):
    id: str
    type: str
    attributes: IncludedAttribute


class IncludedTodolist(BaseModel):
    id: str
    type: str
    attributes: IncludedAttribute


class IncludedMember(BaseModel):
    id: str
    type: str
    attributes: IncludedAttribute


class IncludedTodosCustomField(BaseModel):
    id: str
    type: str
    attributes: Dict

    def _get_by_name(self, name: str) -> Dict:
        """
        根据 name 获取自定义字段
        :param name:
        :return:
        """
        for k, v in self.attributes['custom_fields'].items():
            if v.get('name') == name:
                return v

        return {}

    def get_related_member_id(self) -> List:
        """
        获取相关人
        :return:
        """
        return self._get_by_name("相关人").get('value', []) or []

    def get_status(self) -> str:
        """
        获取状态
        :return:
        """
        return self._get_by_name("进展状态").get('value', TowerStatus.NO_STATUS)


class IncludedComments(BaseModel):
    id: str
    type: str
    attributes: IncludedAttribute


class TodoAttributesModel(BaseModel):
    team_wide_id: int
    content: str
    desc: Optional[str]
    is_active: bool
    is_completed: bool
    priority: str
    start_at: Optional[str]
    due_at: Optional[str]
    closed_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    labels: List[str]


class TodoRelationshipObjDataModel(BaseModel):
    id: str
    type: str


class TodoRelationshipObjModel(BaseModel):
    data: Optional[TodoRelationshipObjDataModel]


class TodoRelationshipObjArrayModel(BaseModel):
    data: List[TodoRelationshipObjDataModel]


class TodoRelationshipsModel(BaseModel):
    project: TodoRelationshipObjModel
    todolist: TodoRelationshipObjModel
    creator: TodoRelationshipObjModel
    assignee: TodoRelationshipObjModel
    closer: TodoRelationshipObjModel
    parent: TodoRelationshipObjModel
    custom_field_value: TodoRelationshipObjModel
    sub_todos: TodoRelationshipObjArrayModel
    comments: TodoRelationshipObjArrayModel
    todolists: TodoRelationshipObjArrayModel
    attachments: TodoRelationshipObjArrayModel


class TodoDataModel(BaseModel):
    id: str
    type: str
    attributes: TodoAttributesModel
    relationships: TodoRelationshipsModel


class JsonApiModel(BaseModel):
    version: str


class TodoModel(BaseModel):
    data: TodoDataModel
    included: List[Union[IncludedProject, IncludedTodolist, IncludedMember, IncludedTodosCustomField, IncludedComments]]
    jsonapi: JsonApiModel

    def get_included_by_type(self, type_name: str):
        for o in self.included:
            if o.type == type_name:
                return o

    @property
    def attr(self) -> TodoAttributesModel:
        return self.data.attributes

    @property
    def name(self) -> str:
        return self.attr.content

    @property
    def id(self):
        return self.attr.team_wide_id

    @property
    def url(self) -> str:
        return f"https://tower.im/teams/{TOWER_TEAM_ID}/todos/{self.id}/"

    @property
    def related_member(self) -> List[str]:
        custom_field = self.get_included_by_type("todos_custom_field_values")
        # 拿到用户的 ID
        user_ids: List[str] = custom_field.get_related_member_id()
        # 分配给谁
        assignee = self.data.relationships.assignee.data
        if assignee:
            user_ids.append(assignee.id)

        return list(set([TowerUserMap.get(user_id, "") for user_id in user_ids if user_id in TowerUserMap]))

    @property
    def status(self) -> str:
        if self.attr.is_completed:
            return TaskStatus.COMPLETED

        custom_field = self.get_included_by_type("todos_custom_field_values")
        tower_status = custom_field.get_status()
        if tower_status in TaskTowerStatusMap:
            return TaskTowerStatusMap.get(tower_status, TaskStatus.NO_STATUS)

        if len(self.related_member) > 0:
            return TaskStatus.ASSIGNED

        return TaskStatus.NO_STATUS

    @property
    def priority(self) -> str:
        return TaskTowerPriorityMap.get(self.attr.priority, TaskPriority.NORMAL)

    @property
    def is_related_to_me(self) -> bool:
        """
        是否跟我相关
        1. 增值的任务
        2. 分配给我的任务
        3. 相关人是我的任务
        4. 描述中提到我的

        :return:
        """
        todolist = self.get_included_by_type("todolists")
        if todolist.attributes.get('name') == "增值":
            return True

        if me in self.related_member:
            return True

        if self.attr.desc and me in self.attr.desc:
            return True

        return False
