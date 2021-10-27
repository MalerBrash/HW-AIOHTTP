import pydantic
from views import *

PG_DSN = f'postgres://aiohttp:1234@127.0.0.1:5432/aiohttp'


@web.middleware
async def validation_error_handler(request, handler):
    try:
        response = await handler(request)
    except pydantic.error_wrappers.ValidationError as er:
        response = web.json_response({'error': 'Validation error', 'message': er.errors()}, status=422)
    except ValidateError as er:
        response = web.json_response({'error': er.reason, 'message': er.message}, status=422)
    except asyncpg.exceptions.ForeignKeyViolationError as er:
        response = web.json_response({'error': 'KeyError', 'message': 'no such user'}, status=422)
    except NotFound as er:
        response = web.json_response({'error': er.reason, 'message': er.message}, status=404)
    except web.HTTPBadRequest as er:
        response = web.json_response({'error': str(er), 'message': 'username or email already exist'}, status=400)

    return response

app = web.Application(middlewares=[validation_error_handler])


async def init_orm(app):
    print('приложение стартовало')

    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


app.add_routes([web.post('/user', UserView)])
app.add_routes([web.get('/user/{user_id:\d+}', UserView)])
app.add_routes([web.patch('/user/{user_id:\d+}', UserView)])
app.add_routes([web.delete('/user/{user_id:\d+}', UserView)])
app.add_routes([web.get('/users', UsersView)])
app.add_routes([web.post('/article', ArticleView)])
app.add_routes([web.get('/article/{article_id:\d+}', ArticleView)])
app.add_routes([web.patch('/article/{article_id:\d+}', ArticleView)])
app.add_routes([web.delete('/article/{article_id:\d+}', ArticleView)])
app.add_routes([web.get('/articles', ArticlesView)])
app.cleanup_ctx.append(init_orm)

if __name__ == '__main__':
    web.run_app(app, port=8080)
