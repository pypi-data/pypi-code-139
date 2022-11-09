from rest_framework import status
from django.utils.translation import gettext as _


class ResultMessageStructure:
    def __init__(self, code: int, message: str, is_success_result: bool, http_code=status.HTTP_200_OK):
        self.code, self.message, self.is_success_result, self.http_code = code, message, is_success_result, http_code


class ResultMessages:
    GET_SUCCESSFULLY = ResultMessageStructure(2000, 'Done', True, status.HTTP_200_OK)
    SUBMIT_SUCCESSFULLY = ResultMessageStructure(2001, 'Submit', True, status.HTTP_201_CREATED)
    PAGE_NOT_FOUND = ResultMessageStructure(4004, 'Page Not Found', False, status.HTTP_404_NOT_FOUND)
    UNDEFINED_ERROR = ResultMessageStructure(5000, 'Undefined Error.', False, status.HTTP_500_INTERNAL_SERVER_ERROR)
    ENTERED_DATA_NOT_VALID = ResultMessageStructure(4006, 'Entered Data Is Not Valid', False,
                                                    status.HTTP_406_NOT_ACCEPTABLE)
    BAD_REQUEST = ResultMessageStructure(4000, 'Bad Request', False, status.HTTP_400_BAD_REQUEST)
    UNDEFINED_METHOD = ResultMessageStructure(4005, 'Invalid Method', False, status.HTTP_405_METHOD_NOT_ALLOWED)
    INVALID_CONTENT_TYPE = ResultMessageStructure(4015, 'Invalid Content-Type', False,
                                                  status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    AUTHENTICATION_FAIL = ResultMessageStructure(4001, 'Unauthorized', False, status.HTTP_401_UNAUTHORIZED)
    FORBIDDEN = ResultMessageStructure(4003, 'Forbidden', False, status.HTTP_403_FORBIDDEN)
