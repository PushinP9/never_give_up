from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    ROUTE = "/movies"

    def create_movie(self, payload, token):
        """
        Создание фильма. Требует токен админа.
        Ожидаем 201 Created.
        """
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        return self.send_request(
            "POST",
            self.ROUTE,
            data=payload,
            headers=headers,
            expected_status=201
        )

    def get_all_movies(self, params=None):
        """
        Получение списка фильмов.
        Параметры (params) нужны для фильтрации (поиск по названию).
        Ожидаем 200 OK.
        """
        return self.send_request(
            "GET",
            self.ROUTE,
            params=params,
            expected_status=200
        )

    def get_movie_by_id(self, movie_id):
        """
        Получение одного фильма по ID.
        Ожидаем 200 OK.
        """
        return self.send_request(
            "GET",
            f"{self.ROUTE}/{movie_id}",
            expected_status=200
        )

    def update_movie(self, movie_id, payload, token):
        """
        Обновление фильма (PATCH). Требует токен.
        Ожидаем 200 OK.
        """
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        return self.send_request(
            "PATCH",
            f"{self.ROUTE}/{movie_id}",
            data=payload,
            headers=headers,
            expected_status=200
        )

    def delete_movie(self, movie_id, token):
        """
        Удаление фильма. Требует токен.
        Ожидаем 204 No Content (или 200, зависит от API, ставим пока 200 как дефолт в реквестере,
        но если сваггер говорит 204 - поменяем).
        """
        headers = self.base_headers.copy()
        headers["Authorization"] = f"Bearer {token}"

        # Обычно DELETE возвращает 204 или 200. Давай пока ожидать 200 или укажем явно.
        # Если сваггер говорит 204, то нужно передать expected_status=204
        return self.send_request(
            "DELETE",
            f"{self.ROUTE}/{movie_id}",
            headers=headers,
            expected_status=200  # <-- Тут нужно свериться со сваггером, часто бывает 204
        )