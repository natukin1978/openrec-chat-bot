import asyncio
import json
import logging
import os
import sys

import global_value as g

g.app_name = "openrec_chat_bot"
g.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

from config_helper import read_config
from one_comme_users import OneCommeUsers
from openrec_bot import OpenrecBot
from openrec_helper import OpenrecHelper
from text_helper import read_text, read_text_set
from websocket_helper import websocket_listen_forever

print("前回の続きですか？(y/n) ", end="")
is_continue = input() == "y"

g.ADDITIONAL_REQUESTS_PROMPT = read_text("prompts/additional_requests_prompt.txt")

g.config = read_config()

# ロガーの設定
logging.basicConfig(filename=f"{g.app_name}.log", encoding="utf-8", level=logging.INFO)

logger = logging.getLogger(__name__)

g.map_is_first_on_stream = {}
g.set_exclude_id = read_text_set("exclude_id.txt")
# g.set_needs_response = set()
g.websocket_openrec_live = None
g.websocket_fuyuka = None


async def main():
    def get_fuyukaApi_baseUrl() -> str:
        conf_fa = g.config["fuyukaApi"]
        if not conf_fa:
            return ""
        return conf_fa["baseUrl"]

    def set_ws_openrec_live(ws) -> None:
        g.websocket_openrec_live = ws

    async def recv_openrec_live_response(message: str) -> None:
        try:
            mode, json_str = OpenrecHelper.separate_integer_and_string(message)
            if mode is None:
                return
            if mode != 42:
                # コメント以外
                return
            _, json_str = json.loads(json_str)
            json_ws = json.loads(json_str)
            if json_ws["type"] != 0:
                # コメント以外
                return
            await bot.on_message_from_ws(json_ws["data"])
        except json.JSONDecodeError as e:
            logger.error(f"Error JSONDecode: {e}")
        except Exception as e:
            logger.error(f"Error : {e}")

    def set_ws_fuyuka(ws) -> None:
        g.websocket_fuyuka = ws

    async def recv_fuyuka_response(message: str) -> None:
        return

    bot = OpenrecBot()

    if is_continue and OneCommeUsers.load_is_first_on_stream():
        print("挨拶キャッシュを復元しました。")

    await bot.run()

    # movie_id が得られるまで待機する
    while True:
        if bot.movie_id:
            break
        await asyncio.sleep(self.chat_polling_interval)

    websocket_uri = f"wss://chat.openrec.tv/socket.io/?EIO=3&transport=websocket&movieId={bot.movie_id}"
    asyncio.create_task(
        websocket_listen_forever(
            websocket_uri, recv_openrec_live_response, set_ws_openrec_live
        )
    )

    fuyukaApi_baseUrl = get_fuyukaApi_baseUrl()
    if fuyukaApi_baseUrl:
        websocket_uri = f"{fuyukaApi_baseUrl}/chat/{g.app_name}"
        asyncio.create_task(
            websocket_listen_forever(websocket_uri, recv_fuyuka_response, set_ws_fuyuka)
        )

    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
