from aiohttp import web

app = web.Application()


class Users(web.View):
    async def get(self):
        pass

    async def post(self):
        pass

    async def patch(self):
        pass

    async def delete(self):
        pass


app.add_routes(
    [
        web.get('/users/{user_id:\d+}', Users),
        web.post('/users/', Users),
        web.patch('/users/{user_id:\d+}', Users),
        web.delete('/users/{user_id:\d+}', Users)
    ]
)

if __name__ == '__main__':
    web.run_app(app, port=8000)
