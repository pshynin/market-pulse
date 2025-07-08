# MarketPulse

## Overview
MarketPulse is a web-based dashboard that helps investors quickly assess whether current market growth is a healthy bull cycle or a dangerous blow-off top by tracking and analyzing 5 key macro and technical signals.

## Features
- Real-time analysis of market signals (Green/Yellow/Red)
- Historical tracking of market conditions
- AI-powered insights on current market status
- Email alerts for significant market changes

## Tech Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React
- **Database**: PostgreSQL (with TimescaleDB)
- **Hosting**: Fly.io (backend), Cloudflare Pages (frontend)

## Project Structure
- `backend/`: FastAPI server, data collectors, and signal processing
- `frontend/`: React dashboard application
- `database/`: Database schema and migrations

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL

### Running Locally
```bash
# Start backend and frontend services
docker-compose up
```

## License
MIT
