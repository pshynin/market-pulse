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

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
│                                                                     │
│  ┌─────────────────────────────┐        ┌────────────────────────┐  │
│  │    React Frontend App       │        │    Email Notifications │  │
│  │    (Cloudflare Pages)       │        │                        │  │
│  └──────────────┬──────────────┘        └─────────────┬──────────┘  │
└─────────────────┬─────────────────────────────────────┬─────────────┘
                  │                                     │
                  ▼                                     │
┌─────────────────────────────────────────────┐         │
│               API GATEWAY                   │         │
│          (Cloudflare/Fly.io)                │         │
└───────────────────┬─────────────────────────┘         │
                    │                                   │
                    ▼                                   │
┌───────────────────────────────────────────────────────┼──────────────┐
│                         APPLICATION LAYER             │              │
│                                                       │              │
│  ┌─────────────────────────┐    ┌────────────────────┐│              │
│  │   FastAPI Backend       │    │                    ││              │
│  │                         │    │  Scheduled Jobs    ││              │
│  │  ┌─────────────────┐    │    │                    ││              │
│  │  │  API Endpoints  │    │    │ ┌────────────────┐ ││              │
│  │  └────────┬────────┘    │    │ │ Data Collection│ ││              │
│  │           │             │    │ └────────┬───────┘ ││              │
│  │  ┌────────▼────────┐    │    │          │         ││              │
│  │  │ Signal Processor│◄───┼────┼──────────┘         ││              │
│  │  └────────┬────────┘    │    │                    ││              │
│  │           │             │    │                    ││              │
│  │  ┌────────▼────────┐    │    │ ┌────────────────┐ ││              │
│  │  │  GPT Integration│    │    │ │Email Generator ├─┼┘              │
│  │  └─────────────────┘    │    │ └────────────────┘ │               │
│  └─────────────┬───────────┘    └────────────────────┘               │
└────────────────┼─────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              PostgreSQL + TimescaleDB                       │    │
│  │                                                             │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐    │    │
│  │  │  Market Data  │  │Signal Results │  │ AI Insights   │    │    │
│  │  └───────────────┘  └───────────────┘  └───────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                  │                                │
                  ▼                                ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│    Financial Data APIs      │     │     OpenAI API (GPT-4)      │
│    (Alpha Vantage, etc.)    │     │                             │
└─────────────────────────────┘     └─────────────────────────────┘
```

The system architecture shows the separation of client, application, and data layers, with clear paths for data flow between components.

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        MarketPulse Data Flow Diagram                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                         ┌──────────────────────────┐
                         │   Scheduled Data Jobs    │
                         │   (Daily/Hourly/etc.)    │
                         └────────────┬─────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                             Data Collection Process                             │
│                                                                                 │
│  ┌────────────────────┐     ┌────────────────────┐     ┌─────────────────────┐  │
│  │  Fetch Stock Data  │────▶│  Fetch VIX Data    │────▶│ Fetch Economic Data │  │
│  │  (SPY, RSP, etc.)  │     │                    │     │ (GDP, ISM, etc.)    │  │
│  └────────────────────┘     └────────────────────┘     └─────────────────────┘  │
│                                                                │                │
│  ┌─────────────────────┐    ┌─────────────────────┐            │                │
│  │Fetch Liquidity Data │◀───│ Fetch Valuation Data│◀───────────┘                │
│  │(M2, Fed Balance)    │    │ (P/E Ratios, EPS)   │                             │
│  └──────────┬──────────┘    └─────────────────────┘                             │
└─────────────┬────────────────-──────────────────────────────────────────────────┘
              │
              ▼
┌────────────────────────┐
│ Store Raw Market Data  │
│    in Database         │
└──────────┬─────────────┘
           │
           ▼
┌───────────────────────────────────────────────────────────────┐
│                   Signal Processing                           │
│                                                               │
│  ┌─────────────────┐   ┌─────────────────┐  ┌──────────────┐  │
│  │ Market Breadth  │   │    Valuation    │  │  Volatility  │  │
│  │    Signal       │   │     Signal      │  │    Signal    │  │
│  └────────┬────────┘   └────────┬────────┘  └───────┬──────┘  │
│           │                     │                   │         │
│  ┌────────▼────────┐   ┌────────▼────────┐          │         │
│  │   Liquidity     │   │      Macro      │          │         │
│  │     Signal      │   │     Signal      │          │         │
│  └────────┬────────┘   └────────┬────────┘          │         │
│           │                     │                   │         │
│           └───────────┬─────────┴───────────────────┘         │
│                       │                                       │
│                       ▼                                       │
│               ┌────────────────┐                              │
│               │ Overall Signal │                              │
│               │ Calculation    │                              │
│               └───────┬────────┘                              │
└───────────────────────┼───────────────────────────────────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  Store Signal     │
              │  Results in DB    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │  Send Data to     │
              │  OpenAI API       │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Generate Market   │
              │ Insight with GPT  │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Store AI Insight  │
              │ in Database       │
              └─────────┬─────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│                   User Interface Layer                        │
│                                                               │
│   ┌────────────────────┐      ┌─────────────────────────┐     │
│   │                    │      │                         │     │
│   │  API Requests      │◀─────│  React Dashboard UI     │     │
│   │                    │      │                         │     │
│   └─────────┬──────────┘      └─────────────────────────┘     │
│             │                                                 │
│   ┌─────────▼──────────┐      ┌─────────────────────────┐     │
│   │                    │      │                         │     │
│   │  Display Signals,  │─────▶│  Optional Email Alerts  │     │
│   │  Charts & Insights │      │  on Signal Changes      │     │
│   │                    │      │                         │     │
│   └────────────────────┘      └─────────────────────────┘     │
└───────────────────────────────────────────────────────────────┘
```

The data flow diagram illustrates how information moves through the system, from initial data collection to signal processing, AI insight generation, and finally to the user interface.

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
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
cd ..
docker compose up --build
```

### Lint and Format
```bash
pip3 install autopep8
autopep8 --in-place --aggressive --recursive ./backend
```

## License
MIT
