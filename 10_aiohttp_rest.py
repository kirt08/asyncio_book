import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_app import Application


routes = web.RouteTableDef()
DB_KEY = "database"

async def create_database_pool(app: Application):
    print("Creating database connection pool")
    pool: Pool = await asyncpg.create_pool(host = "0.0.0.0",
                                           port = 5432,
                                           user = "asyncio_book_user",
                                           password = "12345678",
                                           database = "asyncio_book",
                                           min_size = 6,
                                           max_size = 6
                                           )
    app[DB_KEY] = pool


async def destroy_database_pool(app: Application):
    print("Destroy database connection pool")
    pool: Pool = app[DB_KEY]
    await pool.close()


@routes.get("/brands")
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = "SELECT brand_id, brand_name FROM brands"
    results: list[Record] = await connection.fetch(brand_query)
    results_as_dict: list[dict] = [dict(brand) for brand in results]
    return web.json_response(results_as_dict)


app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app)
