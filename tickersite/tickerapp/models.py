from django.db import models


class UserRequest(models.Model):
    class Meta:
        ordering = ["created_at"]

    user_ip = models.GenericIPAddressField(null=True, blank=True)
    input_text = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
