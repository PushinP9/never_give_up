import json
import logging
import os
import requests
from constants.constants import LOGIN_ENDPOINT, LOGIN_URL


class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, session, base_url, headers=None):
        self.session = session
        self.base_url = base_url
        self.headers = headers if headers is not None else self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def authenticate(self, email, password):
        url = f"{LOGIN_URL}{LOGIN_ENDPOINT}"
        response = requests.post(url, json={"email": email, "password": password})
        token = response.json()["accessToken"]
        self.headers.update({"Authorization": f"Bearer {token}"})
        return self

    def send_request(
        self,
        method,
        endpoint,
        data=None,
        params=None,
        expected_status=200,
        success_model=None,
        failure_model=None,
        need_logging=True,
    ):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            json=data,
            params=params,
            headers=self.headers,
        )

        if need_logging:
            self.log_request_and_response(response)

        if isinstance(expected_status, (tuple, list, set)):
            ok = response.status_code in expected_status
        else:
            ok = response.status_code == expected_status

        if not ok:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        if not success_model and not failure_model:
            return response

        if not response.content:
            return response

        body = response.json()

        if 200 <= response.status_code < 300:
            if success_model:
                return success_model.model_validate(body)
            return response

        if failure_model:
            return failure_model.model_validate(body)

        return response

    def log_request_and_response(self, response):
        try:
            request = response.request
            green = "\033[32m"
            red = "\033[31m"
            reset = "\033[0m"

            headers = " \\\n".join(
                [f"-H '{header}: {value}'" for header, value in request.headers.items()]
            )

            full_test_name = (
                f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"
            )

            body = ""
            if hasattr(request, "body") and request.body is not None:
                raw_body = request.body
                if isinstance(raw_body, bytes):
                    raw_body = raw_body.decode("utf-8")
                body = f"-d '{raw_body}' \n" if raw_body != "{}" else ""

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{green}{full_test_name}{reset}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(
                    json.loads(response.text), indent=4, ensure_ascii=False
                )
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {red}{response.status_code}{reset}\n"
                    f"\tDATA: {red}{response_data}{reset}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {green}{response.status_code}{reset}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")