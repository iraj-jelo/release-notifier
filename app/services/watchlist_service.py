from app.db.models import User, WatchedProject


class WatchlistService:
    @staticmethod
    async def ensure_user(name: str, email: str | None = None, telegram_chat_id: str | None = None):
        user = None
        if email:
            user = await User.get_or_none(email=email)
        if user is None and name:
            user = await User.get_or_none(name=name)

        if user is not None:
            if name and not user.name:
                user.name = name
            if email and not user.email:
                user.email = email
            if telegram_chat_id and not user.telegram_chat_id:
                user.telegram_chat_id = telegram_chat_id
            await user.save()
            return user

        return await User.create(
            name=name,
            email=email,
            telegram_chat_id=telegram_chat_id,
        )

    @staticmethod
    async def add_project(
        user_id: int,
        *,
        owner: str,
        repo: str,
        source: str = "github",
        display_name: str | None = None,
        project_url: str | None = None,
    ) -> WatchedProject:
        user = await User.get(id=user_id)
        project, _ = await WatchedProject.get_or_create(
            user=user,
            source=source,
            owner=owner,
            repo=repo,
            defaults={
                "display_name": display_name or f"{owner}/{repo}",
                "project_url": project_url,
                "is_active": True,
            },
        )

        if display_name and project.display_name != display_name:
            project.display_name = display_name
        if project_url and project.project_url != project_url:
            project.project_url = project_url
        await project.save()
        return project

    @staticmethod
    async def list_active_projects_for_user(user_id: int) -> list[WatchedProject]:
        return await WatchedProject.filter(user_id=user_id, is_active=True).all()

    @staticmethod
    async def list_active_projects() -> list[WatchedProject]:
        return await WatchedProject.filter(is_active=True).all()
