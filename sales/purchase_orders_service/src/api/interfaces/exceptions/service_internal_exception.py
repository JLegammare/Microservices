from src.api.interfaces.exceptions.generic_api_exception import GenericApiException


class ServiceInternalException(GenericApiException):
    def __init__(self, service_name):
        super().__init__(f'''{service_name} service internal error.''', 500)
