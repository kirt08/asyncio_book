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

@routes.get("/product/{id}")
async def get_product(request: Request) -> Response:
    try:
        product_id = int(request.match_info["id"])
        query = "SELECT product_id, product_name, brand_id FROM product WHERE product_id = $1"
        connection: Pool = request.app[DB_KEY]
        result: Record = await connection.fetchrow(query, product_id)

        if result is not None:
            return web.json_response(dict(result))
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()
    
@routes.post("/product")
async def create_product(request: Request) -> Response:
    PRODUCT_NAME = "product_name"
    BRAND_ID = "brand_id"

    if not request.can_read_body:
        raise web.HTTPBadRequest()
    
    body = await request.json()

    if PRODUCT_NAME in body and BRAND_ID in body:
        db: Pool = request.app[DB_KEY]
        await db.execute("INSERT INTO product(product_id, product_name, brand_id) VALUES (DEFAULT, $1, $2)", body[PRODUCT_NAME], int(body[BRAND_ID]))
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()
        

app = web.Application()
app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app)
