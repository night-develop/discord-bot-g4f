import json

from g4f import Provider
from g4f.Provider import AsyncGeneratorProvider


class Sender:

    __config: dict = None

    def __init__(self, config: dict) -> None:
        self.__config = config

    async def get_tmp_providers(self) -> list:
        f = open("tmp_provider", "r")
        result = f.read()
        return json.loads(result)

    async def send_message(self, messages: list) -> str:
        response = self.__config['alert_messages']['provider_not_found']
        providers = await self.get_tmp_providers()
        for provider in providers:
            current_provider: AsyncGeneratorProvider = getattr(Provider, provider)
            try:
                tmp_response = await current_provider.create_async(
                    model=self.__config['bot']['model'],
                    messages=messages
                )

                if not tmp_response:
                    raise Exception()
                
                response = tmp_response
                break
            except Exception as e:
                pass

        return response
