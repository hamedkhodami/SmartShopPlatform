import factory
from apps.account.enums import UserGenderEnum, UserRoleEnum
from apps.account.models import User, UserBlock, UserProfileModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.Sequence(lambda n: f"+9891234567{n}")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    national_id = factory.Sequence(lambda n: f"{n:010d}")
    role = UserRoleEnum.VIEWER
    is_active = True
    is_superuser = False
    is_staff = False
    password = factory.PostGenerationMethodCall("set_password", "testpassword123")

    class Params:
        admin = factory.Trait(role=UserRoleEnum.ADMIN, is_superuser=True, is_staff=True)
        store_admin = factory.Trait(
            role=UserRoleEnum.STORE_ADMIN, is_superuser=False, is_staff=True
        )
        customer = factory.Trait(
            role=UserRoleEnum.CUSTOMER, is_superuser=False, is_staff=True
        )
        viewer = factory.Trait(
            role=UserRoleEnum.VIEWER, is_superuser=False, is_staff=False
        )


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfileModel

    user = factory.SubFactory(UserFactory)
    gender = factory.Iterator(UserGenderEnum.values)
    bio = factory.Faker("text", max_nb_chars=200)
    image = None
    city = factory.Faker("city")


class UserBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserBlock

    user = factory.SubFactory(UserFactory)
    admin = factory.SubFactory(UserFactory, role=UserRoleEnum.ADMIN)
    note = factory.Faker("sentence", nb_words=10)
