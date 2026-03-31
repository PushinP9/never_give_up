BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

body = {
  "name": "Няньки",
  "imageUrl": "https://image.url",
  "price": 100,
  "description": "2 нянки",
  "location": "SPB",
  "published": True,
  "genreId": 1
}

body_negative = {
  "name": "",
  "imageUrl": "https://image.url",
  "price": 100,
  "description": "2 нянки",
  "location": "SPB",
  "published": True,
  "genreId": 1
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"


create_body = {
  "id": 2,
  "name": "Название фильма",
  "price": 200,
  "description": "Описание фильма",
  "imageUrl": "https://image.url",
  "location": "MSK",
  "published": True,
  "genreId": 1,
  "genre": {
    "name": "Драма"
  },
  "createdAt": "2024-02-28T04:28:15.965Z",
  "rating": 5
}

create_body_negative = {
  "id": 0,
  "name": "Название фильма",
  "price": 200,
  "description": "Описание фильма",
  "imageUrl": "https://image.url",
  "location": "MSK",
  "published": True,
  "genreId": 1,
  "genre": {
    "name": "Драма"
  },
  "createdAt": "2024-02-28T04:28:15.965Z",
  "rating": 5
}