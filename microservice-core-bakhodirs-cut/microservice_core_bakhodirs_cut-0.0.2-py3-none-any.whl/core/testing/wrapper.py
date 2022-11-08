def atomic(func):
    async def wrapper(*args, **kwargs):
        from src.microservice.core.database import db

        results = None
        async with db.transaction() as tx:
            try:
                results = await func(*args, **kwargs)
                tx.raise_rollback()
            except Exception as e:
                raise e
        await update_sequence(db)
        return results

    return wrapper