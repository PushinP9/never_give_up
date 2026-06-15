from clients.movies_api import MoviesAPI
from clients.auth_api import AuthAPI
from clients.user_api import UserAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        shared_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.auth_api = AuthAPI(session, headers=shared_headers)
        self.user_api = UserAPI(session, headers=shared_headers)
        self.movies_api = MoviesAPI(session, headers=shared_headers)


    def close_session(self):
        self.session.close()

