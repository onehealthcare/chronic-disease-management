class TaskStatus:
    NO_STATUS = "No Status"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"
    TESTING = "Testing"
    READY = "准备开发"
    NEED_REVIEW = "Need Review"


TowerUserMap = {
    "f0fa08bc03134e3eb84b667644853eca": "zming",
    "6954901637064852b24a2506f0c02e97": "tonghs",
    "9f3c65cad57290583954dfccc65e90b5": "chuck",
}


class TowerStatus:
    NO_STATUS = "No Status"
    ASSIGNED = "排期中"
    IN_PROGRESS = "开发中"
    COMPLETED = "已上线"
    TESTING = "测试中"
    READY = "未启动"

    @classmethod
    def get_all_status(cls):
        return {cls.READY, cls.TESTING, cls.COMPLETED, cls.ASSIGNED, cls.IN_PROGRESS}


TaskTowerStatusMap = {
    TowerStatus.NO_STATUS: TaskStatus.NO_STATUS,
    TowerStatus.ASSIGNED: TaskStatus.ASSIGNED,
    TowerStatus.IN_PROGRESS: TaskStatus.IN_PROGRESS,
    TowerStatus.COMPLETED: TaskStatus.COMPLETED,
    TowerStatus.TESTING: TaskStatus.TESTING,
    TowerStatus.READY: TaskStatus.READY
}
