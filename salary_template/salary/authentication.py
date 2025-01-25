# #  salary/authentication.py


# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = get_user_model().objects.get(email=username)  # Look for user by email
#             if user.check_password(password):  # Check if the password matches
#                 return user
#         except get_user_model().DoesNotExist:
#             return None
