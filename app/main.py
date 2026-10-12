import argparse
import asyncio

from app.config.settings import settings
from app.db.database import close_db, init_db
from app.services.github_client import GitHubReleaseClient
from app.services.release_service import ReleaseService


async def run_manual_check() -> None:
    await init_db()
    try:
        client = GitHubReleaseClient()
        release_service = ReleaseService(client)

        print(f"Connected with GitHub token configured: {bool(settings.github_token)}")
        print(f"Release service initialized for {settings.app_name}")
        print("Manual check run: project wiring is ready.")
        print("Next step: iterate user watchlists and dispatch notifications.")

        _ = release_service
    finally:
        await close_db()


async def run_daemon() -> None:
    await init_db()
    try:
        print("Daemon mode started. Scheduler is ready to process release checks.")
        while True:
            await asyncio.sleep(60)
    finally:
        await close_db()


def main() -> None:
    parser = argparse.ArgumentParser(description="Release notifier")
    parser.add_argument("--check-now", action="store_true", help="Run a manual release check")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")
    args = parser.parse_args()

    if args.daemon:
        asyncio.run(run_daemon())
        return

    asyncio.run(run_manual_check())


if __name__ == "__main__":
    main()
