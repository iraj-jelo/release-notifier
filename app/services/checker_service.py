from app.db.models import NotificationLog, UserPreference, WatchedProject


class ReleaseCheckService:
    def __init__(self, github_client, release_service, notification_service):
        self.github_client = github_client
        self.release_service = release_service
        self.notification_service = notification_service

    async def check_all_projects(self) -> int:
        projects = await WatchedProject.filter(is_active=True).all()
        total_new = 0

        for project in projects:
            user = await project.user
            user_pref = await UserPreference.filter(user_id=user.id).first()
            releases = await self.release_service.fetch_project_releases(project)

            for payload in releases:
                if payload.get("is_draft"):
                    continue
                release = await self.release_service.store_release_if_new(project, payload)
                if release is None:
                    continue

                total_new += 1
                await self.notification_service.notify_user(user, release, project, user_pref=user_pref)

                if user_pref and user_pref.email_enabled and user.email:
                    await NotificationLog.create(
                        user=user,
                        project=project,
                        release=release,
                        channel="email",
                        status="sent",
                    )

                if user_pref and user_pref.telegram_enabled and user.telegram_chat_id:
                    await NotificationLog.create(
                        user=user,
                        project=project,
                        release=release,
                        channel="telegram",
                        status="sent",
                    )

        return total_new

    async def check_user_projects(self, user_id: int) -> int:
        projects = await WatchedProject.filter(user_id=user_id, is_active=True).all()
        total_new = 0

        for project in projects:
            user = await project.user
            user_pref = await UserPreference.filter(user_id=user.id).first()
            releases = await self.release_service.fetch_project_releases(project)

            for payload in releases:
                if payload.get("is_draft"):
                    continue
                release = await self.release_service.store_release_if_new(project, payload)
                if release is None:
                    continue

                total_new += 1
                await self.notification_service.notify_user(user, release, project, user_pref=user_pref)

                if user_pref and user_pref.email_enabled and user.email:
                    await NotificationLog.create(
                        user=user,
                        project=project,
                        release=release,
                        channel="email",
                        status="sent",
                    )

                if user_pref and user_pref.telegram_enabled and user.telegram_chat_id:
                    await NotificationLog.create(
                        user=user,
                        project=project,
                        release=release,
                        channel="telegram",
                        status="sent",
                    )

        return total_new
