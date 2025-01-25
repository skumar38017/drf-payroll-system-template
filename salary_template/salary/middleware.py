# salary/middleware.py

class MultipleUserLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view is called
        self.process_request(request)

        # Get the response from the view or next middleware
        response = self.get_response(request)

        # Process the response (if needed)
        return response

    def process_request(self, request):
        """
        Check if the user is logged in as both admin and user.
        Separate admin and user session keys.
        """
        # Check if the user is logged in as admin or normal user
        if 'is_admin' in request.session:
            # Admin-specific session setup
            request.session['is_superuser'] = True
            request.session['is_admin'] = True
        elif 'is_user' in request.session:
            # Non-admin user session setup
            request.session['is_superuser'] = False
            request.session['is_admin'] = False
        else:
            request.session['is_superuser'] = False
            request.session['is_admin'] = False
