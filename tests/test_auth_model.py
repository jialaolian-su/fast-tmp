from tortoise.contrib import test

from fast_tmp.models import Group, Permission, User


class TestAuth(test.TestCase):
    def test_something(self):
        pass

    async def test_perm(self):
        p1 = await Permission.create(name="is active", codename="is_active")
        g1 = await Group.create(name="group1")
        user = User(
            username="admin",
            email="chise123@live.com",
        )
        user.set_password("123456")
        await user.save()
        await g1.permissions.add(p1)
        await user.groups.add(g1)
        await user.permissions.add(p1)
        assert 1 == await g1.users.all().count()
        assert 1 == await user.permissions.all().count()
        assert 1 == await user.groups.all().count()
