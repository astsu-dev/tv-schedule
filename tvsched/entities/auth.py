import enum


class ActorPermission(enum.Enum):
    """Permissions for auth endpoint."""

    CREATE = enum.auto()
    READ = enum.auto()
    UPDATE = enum.auto()
    DELETE = enum.auto()


class ShowPermission(enum.Enum):
    """Permissions for show endpoint."""

    CREATE = enum.auto()
    READ = enum.auto()
    UPDATE = enum.auto()
    DELETE = enum.auto()


class EpisodePermission(enum.Enum):
    """Permissions for episode endpoint."""

    CREATE = enum.auto()
    READ = enum.auto()
    UPDATE = enum.auto()
    DELETE = enum.auto()


class Role(str, enum.Enum):
    """User role."""

    USER = "USER"
    ADMIN = "ADMIN"


roles = {
    Role.USER: {
        ActorPermission.READ, ShowPermission.READ, EpisodePermission.READ
    },
    Role.ADMIN: {
        ActorPermission.CREATE, ActorPermission.READ, ActorPermission.UPDATE, ActorPermission.DELETE,
        ShowPermission.CREATE, ShowPermission.READ, ShowPermission.UPDATE, ShowPermission.DELETE,
        EpisodePermission.CREATE, EpisodePermission.READ, EpisodePermission.UPDATE, EpisodePermission.DELETE
    }
}
