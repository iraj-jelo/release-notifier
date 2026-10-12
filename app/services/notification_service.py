from typing import Any


class EmailService:
    async def send(self, to_email: str, subject: str, body: str) -> None:
        """Placeholder implementation for sending email notifications."""
        return None


class TelegramService:
    async def send(self, chat_id: str, message: str) -> None:
        """Placeholder implementation for sending Telegram notifications."""
        return None


class NotificationService:
    def __init__(self, email_service: EmailService | None = None, telegram_service: TelegramService | None = None):
        self.email_service = email_service or EmailService()
        self.telegram_service = telegram_service or TelegramService()

    async def notify_user(self, user: Any, release: Any, project: Any) -> None:
        subject = f"New release: {project.display_name or project.repo} {release.version_tag}"
        body = (
            f"Project: {project.display_name or project.repo}\n"
            f"Version: {release.version_tag}\n"
            f"Release URL: {release.release_url}\n"
            f"Summary: {release.body_summary or 'No summary available'}"
        )

        if user.email:
            await self.email_service.send(user.email, subject, body)

        if user.telegram_chat_id:
            telegram_message = (
                f"🚀 {project.display_name or project.repo} {release.version_tag}\n"
                f"{release.release_url or 'Link not available'}"
            )
            await self.telegram_service.send(str(user.telegram_chat_id), telegram_message)
