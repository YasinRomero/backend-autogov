import requests

class ReniecClient:

    TOKEN = "4fdf6e36e5b679f6100876e4e1dde6a920248dbec6196f99e1cfa94c255b2b47"

    BASE_URL = "https://apiperu.dev/api/dni"

    def validate_dni(self, dni: str):

        url = f"{self.BASE_URL}?numero={dni}"

        print("URL:", url)

        response = requests.get(
            f"{self.BASE_URL}/{dni}",
            headers={
                "Authorization": f"Bearer {self.TOKEN}"
            }
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        if response.status_code != 200:
            return None

        return response.json()