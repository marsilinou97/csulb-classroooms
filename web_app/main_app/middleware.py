class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    # Add response headers
    def __call__(self, request):
        response = self.get_response(request)
        # response['Content-Security-Policy'] = "default-src 'self';"
        response['X-Frame-Options'] = "DENY"
        response['X-Xss-Protection'] = "1; mode=block;"
        response['X-Content-Type-Options'] = "nosniff"
        return response

