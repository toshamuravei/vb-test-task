from aiohttp import web

from api.routes import routes
from middlewares import db_session


app = web.Application(middlewares=(db_session,))
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)
