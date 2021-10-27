from serializers import *
from errors import ValidateError
from models import *


class UserView(web.View):

    async def post(self):
        user_data = await self.request.json()
        if user_data.get('username', False) and type(user_data['username']) == int:
            raise ValidateError('username must be string')
        user_data_validated = UserValidator(**user_data).dict()
        new_user = await User.create_instance(**user_data_validated)
        return web.json_response(new_user.to_dict())

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await User.by_id(user_id)
        user_data = user.to_dict()
        return web.json_response(user_data)

    async def patch(self):
        user_data = await self.request.json()
        user_id = int(self.request.match_info['user_id'])
        if len(user_data) > 1:
            raise ValidateError('One value may be changed only!')
        elif len(user_data) == 1 and user_data.get('email', False):
            user_data_validated = UserValidatorEmail(**user_data).dict()
        elif len(user_data) == 1 and user_data.get('username', False):
            user_data_validated = UserValidatorUser(**user_data).dict()
        elif len(user_data) == 1 and user_data.get('password', False):
            user_data_validated = UserValidatorPass(**user_data).dict()

        new_user = await User.update_model(user_id, **user_data_validated)
        return web.json_response(new_user.to_dict())


class ArticleView(web.View):
    async def post(self):
        article_data = await self.request.json()
        article_data_validated = ArticleValidator(**article_data).dict()
        new_article = await Article.create_instance(**article_data_validated)
        return web.json_response(new_article.to_dict())

    async def get(self):
        article_id = self.request.match_info['article_id']
        article = await Article.by_id(int(article_id))
        article_data = article.to_dict()
        return web.json_response(article_data)

    async def patch(self):
        article_data = await self.request.json()
        article_id = int(self.request.match_info['article_id'])
        if len(article_data) > 1:
            raise ValidateError('One value may be changed only!')
        elif len(article_data) == 1 and article_data.get('title', False):
            article_data_validated = ArticleValidatorTitle(**article_data).dict()
        elif len(article_data) == 1 and article_data.get('text', False):
            article_data_validated = ArticleValidatorText(**article_data).dict()
        elif len(article_data) == 1 and article_data.get('user_id', False):
            article_data_validated = ArticleValidatorUser(**article_data).dict()

        new_article = await Article.update_model(article_id, **article_data_validated)
        return web.json_response(new_article.to_dict())

    async def delete(self):
        art_id = int(self.request.match_info['article_id'])
        res = await Article.delete_model(art_id)
        if res:
            resp = {
                'status': '200',
                'message': f'article_id: {res} successfully deleting'
            }
        else:
            resp = {
                'status': '204',
                'message': 'article_id probably not deleting'
            }
        return web.json_response(resp)


class ArticlesView(web.View):
    async def get(self):
        articles = await db.all(Article.query)
        article_list = []
        for element in articles:
            article_list.append(element.to_dict())
        return web.json_response(article_list)


class UsersView(web.View):
    async def get(self):
        users = await db.all(User.query)
        user_list = []
        for element in users:
            user_list.append(element.to_dict())
        return web.json_response(user_list)