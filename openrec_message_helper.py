import datetime

from one_comme_users import OneCommeUsers


def create_message_json(
    id: str, display_name: str, is_first: bool, content: str
) -> dict[str, any]:
    localtime = datetime.datetime.now()
    localtime_iso_8601 = localtime.isoformat()
    json_data = {
        "dateTime": localtime_iso_8601,
        "id": id,
        "displayName": display_name,
        "nickname": None,
        "content": content,
        "isFirst": is_first,
        "isFirstOnStream": None,
        "noisy": False,
        "additionalRequests": None,
    }
    OneCommeUsers.update_message_json(json_data)
    return json_data


def create_message_json_from_ws(json_ws: dict[str, any]) -> dict[str, any]:
    id = json_ws["user_key"]
    display_name = json_ws["user_name"]
    is_first = False
    content = ""
    if "message" in json_ws:
        content = json_ws["message"]
    return create_message_json(id, display_name, is_first, content)
