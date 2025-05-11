import datetime


def create_message_json() -> dict[str, any]:
    localtime = datetime.datetime.now()
    localtime_iso_8601 = localtime.isoformat()
    json_data = {
        "dateTime": localtime_iso_8601,
        "id": None,
        "displayName": None,
        "nickname": None,
        "content": None,
        "isFirst": False,
        "isFirstOnStream": None,
        "noisy": False,
        "additionalRequests": None,
    }
    return json_data
