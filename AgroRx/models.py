from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Issue(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="issues/images/")   
    created_at = models.DateTimeField(auto_now_add=True)

    # results
    ai_suggestion = models.TextField(blank=True, null=True)
    expert_prescription = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, default="pending") 

    def __str__(self):
        return f"{self.title} ({self.farmer})"
