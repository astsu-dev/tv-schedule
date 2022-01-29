import enum


class ActorPermission(enum.Enum):
    """Permissions for auth endpoint."""

    READ = enum.auto()
    WRITE = enum.auto()
    EDIT = enum.auto()


class ShowPermission(enum.Enum):
    """Permissions for show endpoint."""

    READ = enum.auto()
    WRITE = enum.auto()
    EDIT = enum.auto()


class EpisodePermission(enum.Enum):
    """Permissions for episode endpoint."""

    READ = enum.auto()
    WRITE = enum.auto()
    EDIT = enum.auto()


class Role(str, enum.Enum):
    """User role."""

    USER = "USER"
    ADMIN = "ADMIN"


roles = {
    Role.USER: {
        ActorPermission.READ, ShowPermission.READ, EpisodePermission.READ
    },
    Role.ADMIN: {
        ActorPermission.READ, ActorPermission.WRITE, ActorPermission.EDIT,
        ShowPermission.READ, ShowPermission.WRITE, ShowPermission.EDIT,
        EpisodePermission.READ, EpisodePermission.WRITE, EpisodePermission.EDIT
    }
}
