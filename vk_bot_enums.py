from enum import Enum

_ = ("IN DB NAME", "SCORE")


class UserType(Enum):
    admin = 2
    moder = 1
    simple = 0

    @classmethod
    def from_name(cls, name):
        for user_type, user_type_name in USER_TYPES.items():
            if user_type_name == name:
                return user_type
        raise ValueError('{} is not a valid user_type name'.format(name))

    def to_name(self):
        return USER_TYPES[self]


USER_TYPES = {
    UserType.admin: "ADMIN",
    UserType.moder: "MODER",
    UserType.simple: "SIMPLE"
}


class Commands(Enum):
    respect = [UserType.moder, ["respect", "одобряю", "уважаю"]]

    votekick = [UserType.simple, ["votekick"]]

    kick = [UserType.moder, ["kick"]]

    mafia = [UserType.simple, ['mafia', 'мафия']]


ALL_COMMANDS = ["respect", "одобряю", "уважаю", "votekick", "kick", "mafia", "мафия"]