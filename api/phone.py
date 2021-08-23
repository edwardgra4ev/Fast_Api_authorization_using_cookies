import re
import json
from fastapi import Response
from app.main_app import application as app


class Phone:
    def __init__(self, array: json):
        self.phone = self._get_numbers_from_string(array)

    def _get_numbers_from_string(array: json) -> list:
        phone = json.loads(array)["phone"]
        return re.findall(r'\d', phone)

    def _format_phone_number_by_mask(self):
        phone = ''.join(self.phone)
        return "{} ({}{}{}) {}{}{}-{}{}-{}{}".format(*phone)

    def main(self) -> str:
        first_character = self.phone[0]
        if first_character not in ("7", "8", "9"):
            return ''.join(self.phone)
        elif first_character == "7":
            self.phone.pop(0)
            self.phone.insert(0, "8")
        elif first_character == "9" and len(self.phone) == 11:
            self.phone.pop(0)
            self.phone.insert(0, "8")
        elif first_character == "9":
            self.phone.insert(0, "8")
        if len(self.phone) == 11:
            return self._format_phone_number_by_mask()

    def __str__(self):
        return self.main()


@app.post("/unify_phone_from_json")
async def phone(data: json) -> Response:
    return Response(phone(data), media_type="text/html")
