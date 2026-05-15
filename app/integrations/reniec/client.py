import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ReniecClient:

    TOKEN = "1867cf2b64806fd5779b44601e543fe3ee8ddbce2eef99c53b8b5fadcf7f0cb8"

    BASE_URL = "https://apiperu.dev/api/dni"

    def validate_dni(self, dni: str):

        try:

            response = requests.get(
                f"{self.BASE_URL}/{dni}",
                headers={
                    "Authorization": f"Bearer {self.TOKEN}"
                },
                timeout=5
            )

            if response.status_code != 200:
                return None

            data = response.json()

            return data.get("data")

        except requests.RequestException:
            return None