from django.db import models


class CustomUser(models.Model):
    """
    A deliberately simple user model (separate from Django's built-in auth
    User) so that the stored password hash and the algorithm used are
    plainly visible fields in the database, which is the point of this
    assignment.
    """

    ALGORITHM_CHOICES = [
        ("md5", "MD5"),
        ("sha256", "SHA-256"),
    ]

    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=128)
    hash_algorithm = models.CharField(max_length=10, choices=ALGORITHM_CHOICES, default="sha256")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.username} ({self.hash_algorithm})"
