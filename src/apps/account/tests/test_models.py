import pytest
from apps.account.models import UserBlock
from apps.account.tests.factories import (
    UserFactory,
)


@pytest.mark.django_db
class TestUserModels:

    def test_user_full_name(self):
        user = UserFactory(first_name="hamed", last_name="khodami")
        assert user.full_name() == "hamed khodami"

    def test_user_is_store_admin_user(self):
        user = UserFactory(role="store_admin")
        assert user.is_store_admin_user is True

    def test_user_has_role_check(self):
        user = UserFactory(role="admin")
        assert user.has_role("admin") is True
        assert user.has_role("viewer") is False


@pytest.mark.django_db
class TestUserBlock:

    def test_user_blocking(self):
        user = UserFactory(role="viewer")
        admin = UserFactory(role="admin")
        user_block = UserBlock.objects.create(user=user, admin=admin, note="Test block")

        assert user.is_blocked is True
        assert user_block.admin == admin

    def test_user_not_blocked_by_default(self):
        user = UserFactory()
        assert user.is_blocked is False


@pytest.mark.django_db
class TestUserProfile:

    def test_user_profile_creation(self):
        user = UserFactory()
        user.refresh_from_db()
        assert hasattr(user, "profile")

        assert user.profile.gender is None
        assert user.profile.bio is None
