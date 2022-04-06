from aiohttp.web import middleware

from db.session import SessionLocal


@middleware
async def db_session(request, handler):
    """
    Puts a database session into request attributes
    """
    async with SessionLocal() as session:
        async with session.begin():
            request["db_session"] = session
            response = await handler(request)
        await session.commit()
    return response
