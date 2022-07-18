from .conn import get_conn
from .read import get_user

async def update_user(telegram_id, balance=False, subscription_id=False):
    conn = await get_conn()
    if balance:
        await conn.execute('UPDATE users SET balance = balance + $1 WHERE telegram_id = $2', balance, telegram_id)
    if subscription_id:
        user = await get_user(telegram_id)
        if user['subscriptions_ids'] is None:
            subscriptions_ids = [subscription_id]
        else:
            subscriptions_ids = user['subscriptions_ids']
            subscriptions_ids.append(subscription_id)
        await conn.execute('UPDATE users SET subscriptions_ids = $1 WHERE telegram_id = $2', subscriptions_ids, telegram_id)
    await conn.close()