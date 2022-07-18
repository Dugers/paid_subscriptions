from .users import RegistrationUserMiddleware


def setup_middleware(dp):
    dp.setup_middleware(RegistrationUserMiddleware())