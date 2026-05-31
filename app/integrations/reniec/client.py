import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ReniecClient:


    TOKEN = os.getenv("RENIEC_API_KEY")


    BASE_URL = os.getenv("RENIEC_API_URL")

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
