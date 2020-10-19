from django.contrib.auth.models import User


def user_existis(username: str) -> bool:
    l = User.objects.filter(username=username)
    return len(list(l)) > 0


def remove_user(name: str) -> bool:
    """
    Delete a User Model record, given a username

    param:
        -
    """
    try:
        user = list(User.objects.filter(username=name))[0]
        user.delete()
        return True
    except Exception as e:
        return False
