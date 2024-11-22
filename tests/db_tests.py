from data.requests import async_session, Users, Admins, Notes

async def create_users():
    async with async_session() as session:
        db = Users(session)
        users_data = [
            {'user_id': 123456, 'full_name': 'Ivan'},
            {'user_id': 234567, 'full_name': 'Sergey'},
            {'user_id': 345678, 'full_name': 'Anna'},
            {'user_id': 456123, 'full_name': 'Olga'},
            {'user_id': 567234, 'full_name': 'Dmitry'},
            {'user_id': 678345, 'full_name': 'Elena'},
            {'user_id': 789456, 'full_name': 'Nikolay'},
            {'user_id': 890567, 'full_name': 'Marina'},
            {'user_id': 901678, 'full_name': 'Alexey'},
            {'user_id': 102345, 'full_name': 'Tatiana'},
            {'user_id': 456789, 'full_name': 'Aleksey'}
        ]

        for user in users_data:
            await db.create(user_id=user['user_id'], full_name=user['full_name'])


async def create_admins():
    async with async_session() as session:
        admin_db = Admins(session)
        user_db = Users(session)

        users = await user_db.get(where_statement='user_id in (456789, 123456)')

        for user in users:
            await admin_db.create(user=user)


async def create_notes():
    async with async_session() as session:
        note_db = Notes(session)
        user_db = Users(session)

        users = await user_db.get(where_statement='user_id in (234567, 345678)')

        for user in users:
            await note_db.create(note='Молодец', user=user)


async def check_kwargs_tips():
    async with async_session() as session:
        user_db = Users(session)
        await user_db.update(user_id=321, full_name='Uaoeu')


async def other_tests():
    async with async_session() as session:
        user_db = Users(session)
        await user_db.set_block(123456, True)
        res = await user_db.get(sort_by='full_name', descend=True, select_blocked=True)
        print(res)


async def start_test():
    # await create_users()
    # await create_admins()
    # await create_notes()
    # await check_kwargs_tips()
    await other_tests()
