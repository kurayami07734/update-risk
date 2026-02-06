# UpdateRisk

**Don't update blindly**. 

UpdateRisk is a system that warns you about potentially broken package updates before you install them. 

It combines community signals from r/archlinux with LLM-powered analysis to
detect breaking changes, boot loops, or bugs reported by other users.


## Architecture

This project is a Monorepo containing two completely isolated components:

1. **Client** (/client): A lightweight Python CLI that runs on your local machine. It checks your pending updates against the risk API.

2. **Server** (/server): A centralized backend consisting of:
    1. **API**: A FastAPI service to query risk data.
    2. **Worker**: A background service that monitors Reddit, uses LLMs (Groq) to identify issues, and updates the database.
    3. **Database**: PostgreSQL storage for package risk metadata.

### Project structure (tentative)

```
.
├── client/                 # CLI Tool (Client-side)
│   ├── src/
│   │   ├── main.py         # Entry point (Typer)
│   │   └── local_scanner.py# Pacman wrappers
│   └── pyproject.toml      # Client dependencies
│
├── server/                 # Backend Services (Server-side)
│   ├── src/
│   │   ├── api/            # FastAPI endpoints
│   │   └── worker/         # Reddit Scraper & LLM Logic
│   ├── docker-compose.yml  # Database + API + Worker orchestration
│   └── pyproject.toml      # Server dependencies
│
└── README.md
```