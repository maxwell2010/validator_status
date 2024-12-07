import aiosqlite
import os.path


name_db = 'ValidatorStatus.db'

cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)


async def create_table():
    async with aiosqlite.connect(path_db) as db:
        await db.execute("""CREATE TABLE validators (
                moniker TEXT,
                status TEXT
                )""")
        await db.commit()


async def read_validator_status(moniker: str = None, status: str = None):
    async with aiosqlite.connect(path_db) as db:
        cursor = await db.execute("""SELECT status FROM validators WHERE moniker=?;""", (moniker,))
        row = await cursor.fetchone()
        status_new = row
        if row:
            await db.execute("""UPDATE validators SET status=? WHERE moniker=?;""", (status, moniker,))
            await db.commit()
            status_new = row[0]
            # if status_new != status:
            #     status_new = status
        else:
            if moniker:
                await db.execute("""INSERT INTO validators VALUES (?,?)""", (moniker, status,))
                await db.commit()
        return status_new
