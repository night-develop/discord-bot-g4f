import asyncio
import json
import g4f
 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from g4f.Provider import AsyncGeneratorProvider
from g4f.Provider import __all__ as all_providers


class Scheduler:
    __config: dict = None

    def __init__(self, config: dict) -> None:
        self.__config = config

    async def check_providers(self):
        providers = []
        for provider in all_providers:
            current_provider: AsyncGeneratorProvider = getattr(g4f.Provider, provider)
            try:
                await current_provider.create_async(
                    model=self.__config['bot']['model'],
                    messages=[{"role": "user", "content": "ping"}]
                )
                providers.append(current_provider.__name__)
            except Exception as e:
                pass

        await self.set_tmp_providers(providers=providers)

    async def set_tmp_providers(self, providers: list) -> None:
        f = open("tmp_provider", "w")
        f.write(json.dumps(providers))
        f.close()

    async def run_scheduler(self):
        async_scheduler = AsyncIOScheduler()

        await self.check_providers()
        async_scheduler.add_job(self.check_providers, 'interval', minutes=5)

        async_scheduler.start()

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            async_scheduler.shutdown()


def run_scheduler_loop(config: dict):
    scheduler = Scheduler(config=config)
    asyncio.run(scheduler.run_scheduler())
