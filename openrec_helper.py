import re


class OpenrecHelper:

    @staticmethod
    def separate_integer_and_string(text: str) -> tuple[int | None, str]:
        """整数と文字列を分離する関数"""
        match = re.match(r"^(\d+)(.*)$", text)
        if match:
            try:
                integer_part: int = int(match.group(1))
                string_part: str = match.group(2)
                return integer_part, string_part
            except ValueError:
                return None, match.group(2)
        else:
            return None, ""
