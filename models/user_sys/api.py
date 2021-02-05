from models.const import CommonStatus
from models.user_sys.dao.user import UserDAO
from models.user_sys.dto.user import UserDTO
from models.user_sys.exceptions import UserNotFoundException


def get_user_by_id(user_id: int) -> UserDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    return UserDTO.from_dao(user)


def create_user(name: str, ident: str = "") -> UserDTO:
    user = UserDAO.create(name=name, ident=ident)
    return UserDTO.from_dao(user)


def update_status_by_user_id(user_id: int, status: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    user.update_status(status)


def delete_user(user_id: int):
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    user.update_status(status=CommonStatus.DELETED)
