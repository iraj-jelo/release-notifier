from datetime import datetime

from app.db.models import ReleaseRecord, WatchedProject


class ReleaseService:
    def __init__(self, github_client):
        self.github_client = github_client

    async def fetch_project_releases(self, project: WatchedProject) -> list[dict]:
        if project.source != "github":
            return []

        releases = await self.github_client.get_latest_releases(project.owner, project.repo)
        normalized = []

        for release in releases:
            published_at = release.get("published_at")
            normalized.append(
                {
                    "version_tag": release.get("tag_name"),
                    "published_at": published_at,
                    "release_url": release.get("html_url"),
                    "body_summary": release.get("body", "")[:500],
                    "is_prerelease": bool(release.get("prerelease")),
                    "is_draft": bool(release.get("draft")),
                    "source": "github",
                }
            )

        return normalized

    async def store_release_if_new(self, project: WatchedProject, release_payload: dict) -> ReleaseRecord | None:
        if not release_payload.get("version_tag"):
            return None

        existing = await ReleaseRecord.filter(project=project, version_tag=release_payload["version_tag"]).first()
        if existing:
            return None

        published_at_value = release_payload.get("published_at")
        if published_at_value:
            try:
                published_at_value = datetime.fromisoformat(published_at_value.replace("Z", "+00:00"))
            except ValueError:
                published_at_value = None

        release = await ReleaseRecord.create(
            project=project,
            version_tag=release_payload["version_tag"],
            published_at=published_at_value,
            release_url=release_payload.get("release_url"),
            body_summary=release_payload.get("body_summary"),
            is_prerelease=release_payload.get("is_prerelease", False),
            is_draft=release_payload.get("is_draft", False),
            source=release_payload.get("source", "github"),
        )

        return release
