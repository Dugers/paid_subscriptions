from .conn import get_conn


async def get_user(telegram_id=False, conn=False, subscription_id=False):
    need_close = False
    if not conn:
        need_close = True
        conn = await get_conn()
    if telegram_id:
        res = await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', telegram_id)
    if subscription_id:
        res = await conn.fetch(f'SELECT telegram_id FROM users WHERE {subscription_id} = ANY(subscriptions_ids);')
    if need_close:
        await conn.close()
    return res


async def get_subscriptions(subscriptions_ids=False, subscription_id=False):
    conn = await get_conn()
    if subscription_id:
        res = await conn.fetchrow('SELECT * FROM subscriptions WHERE id = $1', subscription_id)
    elif subscriptions_ids:
        subscriptions_ids = ",".join(list(map(str, subscriptions_ids)))
        res = await conn.fetch(f'SELECT * FROM subscriptions WHERE id NOT IN ({subscriptions_ids})')
    else:
        res = await conn.fetch('SELECT * FROM subscriptions')
    
    await conn.close()
    return res