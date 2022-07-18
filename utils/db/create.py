from .conn import get_conn
from .read import get_subscriptions


async def create_tables():
    conn = await get_conn()
    await create_table_users(conn)
    await create_table_subscriptions(conn)
    await create_default_subscriptions(conn)
    await conn.close()


async def create_table_users(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS users(
        telegram_id bigint NOT NULL,
        subscriptions_ids integer[],
        balance integer DEFAULT 0
    )
    ''')


async def create_table_subscriptions(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions(
        id serial PRIMARY KEY,
        name text NOT NULL,
        type text NOT NULL,
        price integer,
        invite_link text
    )
    ''')


async def create_default_subscriptions(conn):
    subscriptions = await get_subscriptions()
    if len(subscriptions) == 0:
        await conn.execute('INSERT INTO subscriptions(name, type, price, invite_link) VALUES($1, $2, $3, $4)', "Проверочный канал", "channel", 350, "https://t.me/+8HNQvYtkFHEwMDQy")
        await conn.execute('INSERT INTO subscriptions(name, type, price) VALUES($1, $2, $3)', "Рассылка в боте", "bot", 700, )


async def create_user(telegram_id):
    conn = await get_conn()
    await conn.execute('INSERT INTO users(telegram_id) VALUES($1)', telegram_id)
    await conn.close()