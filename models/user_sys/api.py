from models.user_sys.dao.user import UserDAO
from models.user_sys.dto.user import UserDTO
from models.user_sys.exceptions import UserNotFoundException


def get_user_by_id(user_id: int) -> UserDTO:
    user = UserDAO.get_by_id(user_id)
    if not user:
        raise UserNotFoundException

    return UserDTO.from_dao(user)
