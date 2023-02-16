from aiohttp import web
from database import engine, Session
from models import Base, UserModel
import json
from sqlalchemy.exc import IntegrityError

app = web.Application()


async def get_user(user_id: int, session: Session):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps(
                {'status': 'error', 'description': 'user not found'}
            ),
            content_type='application/json'
        )
    return user


class Users(web.View):
    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        async with Session() as session:
            user = await get_user(user_id=user_id, session=session)
            return web.json_response(
                {'id': user.id,
                 'name': user.name,
                 'registration_date': user.registration_date.isoformat()}
            )

    async def post(self):
        user_data = await self.request.json()
        async with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                await session.commit()
            except IntegrityError as er:
                raise web.HTTPConflict(
                    text=json.dumps(
                        {'status': 'error', 'description': 'user already exists'}),
                    content_type='application/json'
                )
            return web.json_response({
                'id': new_user.id
            })

    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user_data = await self.request.json()
        async with Session() as session:
            user = await get_user(user_id=user_id, session=session)
            for key, value in user_data.items():
                setattr(user, key, value)
                session.add(user)
                await session.commit()
            return web.json_response({'status': 'success'})

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        async with Session() as session:
            user = await get_user(user_id=user_id, session=session)
            await session.delete(user)
            await session.commit()
            return web.json_response({'status': 'success'})


async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    print('FINISH')
    await engine.dispose()


app.cleanup_ctx.append(orm_context)

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
