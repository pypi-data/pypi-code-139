import asyncio
import os
from src.microservice.core.config import conf


class BaseTest:
    fixtures = []
    fixture_path = os.path.join(conf.BASE_DIR, "src", "apps")
    transaction = None

    @property
    def db(self):
        from src.microservice.core.database import db

        return db

    @property
    def loop(self):
        return asyncio.get_event_loop()

    @pytest.fixture(autouse=True)
    async def clear_messages(self):
        producer.clear_messages()

    @pytest.fixture(scope="class", autouse=True)
    async def initialize(self):
        await truncate_tables(self.db)
        await self.populate_db()
        await update_sequence(self.db)

    async def populate_db(self):
        for fixture in self.fixtures:
            await self.load_data(fixture)

    async def load_data(self, relative_path):
        file = open(os.path.join(self.fixture_path, relative_path), "r")
        data = json.load(file)
        for datum in data:
            columns = ",".join(map(lambda field: f'"{field}"', datum["fields"].keys()))
            values = ",".join(map(_str_caster, datum["fields"].values()))
            query = f"""
                                    insert into "{datum['table']}"({columns}) values ({values})
                                """
            await self.db.status(query)
