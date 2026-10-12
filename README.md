# Release Notifier

A Python service for tracking GitHub releases for projects of interest and notifying users through email and Telegram.

This project is intentionally built as a practical MVP with a clean starting architecture for:

- watching GitHub repositories
- tracking release history in SQLite
- sending notifications with Email and Telegram
- supporting both manual checks and daemon-mode scheduling
- allowing user-specific frequency and channel preferences

## Goals

- Monitor release events for projects users care about
- Prevent duplicate notifications by tracking release history
- Support configurable polling frequency: hourly, daily, or weekly
- Keep the project easy to extend for other release sources later (PyPI, npm, GitLab, RSS)

## Current status

This project has a functional code skeleton and startup flow for the MVP. The repository is structured for implementing the working release-checker, scheduler, database models, and notification hooks.

## Tech stack

- Python 3.11+
- Tortoise ORM
- SQLite
- APScheduler
- httpx
- pydantic-settings
- python-telegram-bot
- aiosmtplib

## Project structure

- `app/` – application code
- `data/` – runtime SQLite data and local files
- `.env.example` – environment variable template
- `requirements.txt` – Python dependencies
- `pyproject.toml` – project metadata and dependencies
- `README.md` – project overview

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required values.
4. Run a manual release check:
   ```bash
   python -m app.main --check-now
   ```
5. Or start daemon mode:
   ```bash
   python -m app.main --daemon
   ```

## Planned MVP features

- GitHub release fetcher
- user/watchlist storage in SQLite
- release deduplication
- email notifications
- Telegram notifications
- hourly/daily/weekly scheduling
- manual check and background daemon modes

## License

MIT
