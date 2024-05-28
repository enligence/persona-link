import asyncio
import pytest
from tortoise import Tortoise
from server.settings import TORTOISE_ORM

@pytest.fixture(scope="session", autouse=True)
def db(request) -> None:
    config = TORTOISE_ORM
    config["connections"]["default"] = "sqlite://:memory:"

    async def _init_db() -> None:
        await Tortoise.init(config)
        try:
            await Tortoise._drop_databases()
        except:  # pragma: nocoverage
            pass

        await Tortoise.init(config, _create_db=True)
        await Tortoise.generate_schemas(safe=False)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(_init_db())
    
    def _drop_db():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(Tortoise._drop_databases())
        loop.close()
    
    request.addfinalizer(_drop_db)