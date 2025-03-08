import asyncio
import logging

import aiohttp

import global_value as g
from fuyuka_helper import Fuyuka
from openrec_message_helper import create_message_json
from random_helper import is_hit_by_message_json

logger = logging.getLogger(__name__)


class OpenrecBot:

    def __init__(self):
        config_or = g.config["openrec"]
        self.channel_id = config_or["channelId"]
        self.chat_polling_interval = config_or["chatPollingIntervalSec"]
        self.movie_id = None

    async def on_message(self, comments):
        for comment in comments:
            json_data = create_message_json()

            id = json_data["id"]
            if id in g.set_exclude_id:
                # 無視するID
                return

            answerLevel = g.config["fuyukaApi"]["answerLevel"]
            needs_response = is_hit_by_message_json(answerLevel, json_data)
            await Fuyuka.send_message_by_json_with_buf(json_data, needs_response)

    async def on_message_from_ws(self, json_ws):
        if "user_name" not in json_ws:
            return

        id = str(json_ws["user_id"])
        if id in g.set_exclude_id:
            # 無視するID
            return

        json_data = create_message_json()
        json_data["id"] = id
        json_data["displayName"] = json_ws["user_name"]
        if "message" in json_ws:
            json_data["content"] = json_ws["message"]
        else:
            json_data["content"] = ""

        answerLevel = g.config["fuyukaApi"]["answerLevel"]
        needs_response = is_hit_by_message_json(answerLevel, json_data)
        await Fuyuka.send_message_by_json_with_buf(json_data, needs_response)

    async def get_movie(self):
        try:
            url = "https://public.openrec.tv/external/api/v5/movies"
            params = {
                "is_live": "true",
                "onair_status": 1,
                "channel_ids": self.channel_id,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response_json = await response.json()
                    if not response_json:
                        # 配信してないかも
                        return None
                    movie = response_json[0]
                    return movie
        except Exception as e:
            logger.error(f"Error getting movies: {e}")
            return None

    async def run(self):
        while True:
            movie = await self.get_movie()
            if movie:
                self.movie_id = movie["movie_id"]
                break
            await asyncio.sleep(self.chat_polling_interval)
