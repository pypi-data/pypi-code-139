def db_atomic(func):
    async def arg_wrapper(*args, **kwargs):
        from src.core.database import db, conf

        if conf.ENV == "testing":
            return await func(*args, **kwargs)

        connection = await db.acquire()
        transaction = await connection.transaction()
        try:
            results = await func(*args, **kwargs)
            await transaction.commit()
            await connection.release()
            return results
        except Exception:
            await transaction.rollback()
            await connection.release()
            raise

    return arg_wrapper
