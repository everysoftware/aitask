class RepositoryError(Exception):
    pass


class NoResultFoundError(RepositoryError):
    pass
