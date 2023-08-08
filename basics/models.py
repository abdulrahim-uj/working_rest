import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    creator = models.ForeignKey("accounts.User", blank=True,
                                related_name="creator_%(class)s_objects",
                                on_delete=models.CASCADE)
    updater = models.ForeignKey("accounts.User", blank=True,
                                related_name="updater_%(class)s_objects",
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
