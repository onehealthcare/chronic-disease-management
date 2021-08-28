from broker.tower_sys import refresh_access_token
from models.const import CommonStatus
from models.user_sys import UserAuthProvider
from models.user_sys.dao.user_auth import UserAuthDAO


def main():
    for dao in UserAuthDAO.select().where(
            UserAuthDAO.provider == UserAuthProvider.TOWER,
            UserAuthDAO.status == CommonStatus.NORMAL):
        user_id: int = dao.user_id
        refresh_access_token(user_id=user_id)


if __name__ == "__main__":
    main()
