from models.user import User


class UserService:

    @classmethod
    def create_user(cls, user_props):
        try:
            user = User(name=user_props.get("name"),
                        age=user_props.get("age"),
                        description=user_props.get("description"),
                        userid=user_props.get("id"),
                        access=user_props.get("access", 10))
            print(user)
            return user.insert()
        except Exception as e:
            print(e)
