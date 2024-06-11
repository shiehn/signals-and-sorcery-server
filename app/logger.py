"""
Middleware to log all requests and responses.
Uses a logger configured by the name of django.request
to log all requests and responses according to configuration
specified for django.request.
"""
import logging
import socket
import time
import json
from typing import Callable, Dict, Any

from django.template.response import TemplateResponse
from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin

REQUEST_LOGGER = logging.getLogger("django.request")

# Define the type for log information
CustomLogInfoType = Dict[str, Any]


class RequestLogMiddleware(MiddlewareMixin):
    """Request Logging Middleware"""

    def __init__(self, get_response: Callable = None):
        """Constructor"""
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request: WSGIRequest) -> TemplateResponse:
        """Overrides __call__"""
        RequestLogMiddleware.process_request(request)
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, e)
            raise
        RequestLogMiddleware.process_response(request, response)
        return response

    def process_exception(self, request: WSGIRequest, exception: Exception):
        """Process exception to log it"""
        log_data = self.extract_log_info(request)
        log_data["exception"] = str(exception)
        REQUEST_LOGGER.error(msg=json.dumps(log_data), exc_info=True)

    @staticmethod
    def process_request(request: WSGIRequest) -> None:
        """Set Request Start Time to measure time taken to service request"""
        request.start_time = time.time()

    @staticmethod
    def extract_log_info(
        request: WSGIRequest, response: TemplateResponse = None
    ) -> CustomLogInfoType:
        """Extract appropriate log info from requests/responses/exceptions"""
        log_data = {
            "remote_address": request.META.get("REMOTE_ADDR", "-"),
            "user_agent": request.META.get("HTTP_USER_AGENT", "-"),
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "execution_time": f"{(time.time() - request.start_time):.2f} sec",
        }
        if response:
            log_data["response_code"] = response.status_code

        return log_data

    @staticmethod
    def process_response(request: WSGIRequest, response: TemplateResponse) -> None:
        """Log data using logger"""
        log_data = RequestLogMiddleware.extract_log_info(
            request=request, response=response
        )

        if response.status_code in range(400, 499):
            REQUEST_LOGGER.warning(msg=json.dumps(log_data))
        elif response.status_code in range(500, 599):
            REQUEST_LOGGER.error(msg=json.dumps(log_data))
        else:
            REQUEST_LOGGER.info(msg=json.dumps(log_data))
