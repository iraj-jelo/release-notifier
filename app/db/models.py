from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    email = fields.CharField(max_length=255, null=True)
    telegram_chat_id = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"


class UserPreference(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="preferences")
    frequency = fields.CharField(max_length=20, default="daily")
    email_enabled = fields.BooleanField(default=True)
    telegram_enabled = fields.BooleanField(default=True)
    timezone = fields.CharField(max_length=50, default="UTC")
    quiet_hours_start = fields.CharField(max_length=10, null=True)
    quiet_hours_end = fields.CharField(max_length=10, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_preferences"


class WatchedProject(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="projects")
    source = fields.CharField(max_length=50, default="github")
    owner = fields.CharField(max_length=255)
    repo = fields.CharField(max_length=255)
    display_name = fields.CharField(max_length=255, null=True)
    project_url = fields.CharField(max_length=512, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "watched_projects"


class ReleaseRecord(Model):
    id = fields.IntField(pk=True)
    project = fields.ForeignKeyField("models.WatchedProject", related_name="releases")
    version_tag = fields.CharField(max_length=100)
    published_at = fields.DatetimeField(null=True)
    release_url = fields.CharField(max_length=512, null=True)
    body_summary = fields.TextField(null=True)
    is_prerelease = fields.BooleanField(default=False)
    is_draft = fields.BooleanField(default=False)
    source = fields.CharField(max_length=50, default="github")
    fetched_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "release_records"


class NotificationLog(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="notifications")
    project = fields.ForeignKeyField("models.WatchedProject", related_name="notification_logs")
    release = fields.ForeignKeyField("models.ReleaseRecord", related_name="notifications")
    channel = fields.CharField(max_length=20)
    status = fields.CharField(max_length=20, default="sent")
    sent_at = fields.DatetimeField(auto_now_add=True)
    error_message = fields.TextField(null=True)

    class Meta:
        table = "notification_logs"
