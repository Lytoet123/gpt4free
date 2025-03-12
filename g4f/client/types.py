import os
import aiohttp  # Thêm aiohttp để hỗ trợ bất đồng bộ

from typing import Union

Proxies = Union[dict, str]

class Client:
    def __init__(
        self,
        api_key: str = None,
        proxies: Proxies = None,
        **kwargs
    ) -> None:
        self.api_key: str = api_key
        self.proxies = proxies 
        self.proxy: str = self.get_proxy()

    def get_proxy(self) -> Union[str, None]:
        if isinstance(self.proxies, str):
            return self.proxies
        elif self.proxies is None:
            return os.environ.get("G4F_PROXY")
        elif "all" in self.proxies:
            return self.proxies["all"]
        elif "https" in self.proxies:
            return self.proxies["https"]

    async def chat_completions_create(self, model: str, messages: list, temperature: float = 0.7, web_search: bool = False):
        """ Gửi yêu cầu và nhận phản hồi từ G4f API sử dụng aiohttp """
        url = "https://api.gpt4free.com/chat/completions"  # Giả sử URL của G4f API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "web_search": web_search,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Error: {response.status}")
                return await response.json()
