from functools import wraps

from django.contrib.auth import get_user_model

User = get_user_model()


def bad_user_creation_count_assertion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        initial_user_count = User.objects.count()
        func(*args, **kwargs)
        assert User.objects.count() == initial_user_count, (
            "User is created with invalid data"
        )

    return wrapper
