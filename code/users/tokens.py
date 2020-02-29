from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    key_salt = 'blog.users.tokens.EmailConfirmationTokenGenerator'


# email_confirm_token_generator = EmailConfirmationTokenGenerator()
email_confirm_token_generator = default_token_generator



