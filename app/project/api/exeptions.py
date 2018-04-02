from rest_framework.exceptions import APIException

class RequestAlreadyExists(APIException):
    status_code = 400
    default_detail = 'Friend request was already sent'
    default_code = 'bad_request'


class OwnPostError(APIException):
    status_code = 400
    default_detail = 'Can\' perform operation on own posts'
    default_code = 'bad_request'
