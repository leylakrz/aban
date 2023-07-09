from rest_framework import status
from rest_framework.exceptions import APIException

from utils.messages import SERVER_ERROR_MESSAGE


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = SERVER_ERROR_MESSAGE
