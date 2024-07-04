class RemoveWWWAuthenticateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 401 and "WWW-Authenticate" in response:
            del response["WWW-Authenticate"]
        return response
