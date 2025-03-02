import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('django')

    def __call__(self, request):
        response = self.get_response(request)
        self.logger.debug(
            f"{request.method} {request.get_full_path()} - Status: {response.status_code}"
        )
        return response
