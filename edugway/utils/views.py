from rest_framework.views import exception_handler
from rest_framework import status
from edugway import settings

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, to get 
    # the standard error response.
    response = exception_handler(exc, context)

    # Customize the standard response here.
    # If validation error payload is a list, then convert response to the 
    # standard non field error payload.
    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
        	if isinstance(response.data, (list, tuple)):
        		response.data = {
        			settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: response.data}

    return response
