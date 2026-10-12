import httpx

from app.config.settings import settings


class GitHubReleaseClient:
    def __init__(self, token: str | None = None):
        self.token = token or settings.github_token
        self.base_url = settings.github_api_base_url

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_latest_releases(self, owner: str, repo: str, per_page: int = 10) -> list[dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/releases"
        params = {"per_page": per_page}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self._headers(), params=params)
            response.raise_for_status()
            return response.json()

    async def get_latest_release(self, owner: str, repo: str) -> dict | None:
        releases = await self.get_latest_releases(owner, repo, per_page=1)
        if not releases:
            return None
        return releases[0]
