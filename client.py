import aiohttp
import asyncio

HOST = 'http://0.0.0.0:8080'


async def make_request(path, method='get', **kwargs):
    async with aiohttp.ClientSession() as session:
        request_method = getattr(session, method)
        async with request_method(f'{HOST}/{path}', **kwargs) as response:
            print(response.status)
            return (await response.json())


async def main():
    response = await make_request('user', 'post', json={
                                                    'username': 'Андрей14',
                                                    'email': 'andru14g3@jhgj.ru',
                                                    'password': 'gjhfjfttvghhb'
                                                    })
    # response = await make_request('user/1')
    # response = await make_request('article', 'post', json={
    #                                                    'title': 'Привау5!',
    #                                                    'text': '2Ахаха Привау!',
    #                                                    'user_id': 3
    #                                                    })
    # response = await make_request('article/2', 'patch', json={'text': '{Ухуху Привау!'})
    # response = await make_request('user/2', 'patch', json={'password': 'Adfg34dsfs54@'})
    # response = await make_request('users')
    # response = await make_request('articles')
    # response = await make_request('article/20', 'delete')
    # response = await make_request('articles')
    print(response)
asyncio.run(main())
