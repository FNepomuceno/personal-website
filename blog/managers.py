from django.contrib.auth.models import BaseUserManager

class BlogUserManager(BaseUserManager):
    def validate_fields(self, required_fields):
        for field_pair in required_fields:
            if not field_pair[0]:
                raise ValueError(field_pair[1])

    def create_user(self, username, email, password=None):
        self.validate_fields([
            (username, 'User must have a username'),
            (email, 'User must have an email'),
        ])
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self.db)
        return user
