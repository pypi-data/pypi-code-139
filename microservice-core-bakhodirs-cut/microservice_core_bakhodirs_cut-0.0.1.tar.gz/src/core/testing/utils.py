import json

async def update_sequence(db):
    for table_name, table in db.tables.items():
        if not table.c.id.autoincrement:
            continue
        query = f"""
                    SELECT SETVAL('{table_name}_id_seq',
                        (SELECT COALESCE(MAX(id), 1) FROM "{table_name}"))
                """
        await db.status(query)

async def truncate_tables(db):
    for table_name, table in db.tables.items():
        query = f"""TRUNCATE "{table_name}" CASCADE"""
        await db.status(query)


def _str_caster(val):
    if val is None:
        return "null"
    if isinstance(val, str):
        return f"'{val}'"
    elif isinstance(val, (list, dict)):
        return f"'{json.dumps(val)}'"
    elif isinstance(val, bool):
        val = {True: "true", False: "false"}[val]
        return val
    return str(val)


