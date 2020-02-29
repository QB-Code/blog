from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = 'blog.users.tokens.EmailConfirmationTokenGenerator'


email_confirm_token_generator = EmailConfirmationTokenGenerator()



