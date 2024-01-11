def check_password(usermap: dict, user: str, password: str) -> bool:
    return user in usermap and usermap.get(user).get("password") == password
