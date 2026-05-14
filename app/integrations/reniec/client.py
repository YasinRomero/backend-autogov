import requests

class ReniecClient:

    TOKEN = "2e2d06338eddc98894bf69f9268b96554060d628ed34416ea0c64b9358a0ce8d"

    BASE_URL = "https://api.apis.net.pe/v2/reniec/dni"

    def validate_dni(self, dni: str):

        response = requests.get(
            f"{self.BASE_URL}?numero={dni}",
            headers={
                "Authorization": f"Bearer {self.TOKEN}"
            }
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        return data