from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,        
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES($1)"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    # =============== QURANEDU ===============
    async def add_quranedu(self, sequence, sura_name, total_verses, zip_id, audiohusary):
        sql = ("INSERT INTO quranedu_quranedu (sequence, sura_name, total_verses, zip, audiohusary) "
               "VALUES($1, $2, $3, $4, $5)")
        return await self.execute(sql, sequence, sura_name, total_verses, zip_id, audiohusary, fetchrow=True)

    async def update_edu_to_muqriy(self, audiomuqriy, sequence):
        sql = "UPDATE quranedu_quranedu SET audiomuqriy=$1 WHERE sequence=$2"
        return await self.execute(sql,audiomuqriy, sequence, execute=True)

    async def update_temp_to_muqriy(self, audiomuqriy):
            sql = "UPDATE quranedu_quranedu SET audiomuqriy=$1"
            return await self.execute(sql,audiomuqriy, execute=True)

    async def select_all_muqriyaudio(self):
        sql = "SELECT sequence, sura_name, audiomuqriy FROM quranedu_quranedu ORDER BY sequence"
        return await self.execute(sql, fetch=True)

    async def select_muqriyaudio(self, sequence):
        sql = f"SELECT sequence, sura_name, audiomuqriy FROM quranedu_quranedu WHERE sequence='{sequence}'ORDER BY sequence"
        return await self.execute(sql, fetchrow=True)

    async def select_all_husary(self):
        sql = "SELECT sequence, sura_name, audiohusary, zip FROM quranedu_quranedu ORDER BY sequence"
        return await self.execute(sql, fetch=True)

    async def select_husary(self, sequence):
        sql = (f"SELECT sequence, sura_name, total_verses, audiohusary, zip FROM quranedu_quranedu "
               f"WHERE sequence='{sequence}'ORDER BY sequence")
        return await self.execute(sql, fetchrow=True)

    async def select_husary_verses(self, sequence):
        sql = f"SELECT sura_name, total_verses FROM quranedu_quranedu WHERE sequence='{sequence}'ORDER BY sequence"
        return await self.execute(sql, fetchrow=True)

    # =========================== QURANTANISHUV =========================
    async def create_table_qurantanishuv(self):
        sql = """
        CREATE TABLE IF NOT EXISTS qurantanishuv (
        id SERIAL PRIMARY KEY,        
        audio_id VARCHAR(200) NULL,
        video_id VARCHAR(200) NULL,
        caption VARCHAR(3000) NULL,
        link VARCHAR(300) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_audio_quranishuv(self, audio_id, caption, link):
        sql = "INSERT INTO qurantanishuv (audio_id, caption, link) VALUES($1, $2, $3)"
        return await self.execute(sql, audio_id, caption, link, fetchrow=True)

    async def update_videos_qurantanishuv(self, video_id):
        sql = "UPDATE qurantanishuv SET video_id=$1"
        return await self.execute(sql, video_id, execute=True)

    async def select_file_qurantanishuv(self, id_):
        sql = f"SELECT * FROM qurantanishuv WHERE id='{id_}'"
        return await self.execute(sql, fetchrow=True)