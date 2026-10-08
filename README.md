# ⚽ FPL Manager Analytics

**A Python-based Fantasy Premier League Manager Analytics System**

Track FPL manager performance, analyze historical squads, monitor transfers and chips, and explore gameweek scoring across the 2026/27 season.

**Status:** 🚧 Active Development | **Language:** Python | **Season:** 2026/27

---

## 📖 Project Overview

FPL Manager Analytics is a personal software development and data analytics project that uses the Fantasy Premier League API to collect, process, and analyze manager data.

The goal is to build a system that can track any FPL manager throughout an entire season, providing insights into squad selections, individual player contributions, transfer decisions, and overall performance.

The project is being developed incrementally using a modular Python architecture, automated testing, and GitHub project management.

## ✨ Implemented Features

### Manager Tracking

- Retrieve manager information using an FPL Entry ID
- Retrieve historical gameweek squads
- Track starting XI, substitutes, captains, and vice-captains
- Identify squad changes between gameweeks
- Retrieve transfer history and chip usage
- Generate complete manager gameweek snapshots
- Build a historical manager timeline

### Player Performance Analytics

- Retrieve historical player gameweek statistics
- Track minutes, goals, assists, clean sheets, and bonus points
- Calculate starting XI and bench points
- Calculate scores using FPL pick multipliers
- Compare calculated gameweek scores against official FPL results

### Scoring Engine — In Development

- Formation validation
- Goalkeeper and outfield substitution logic
- Multiple substitution handling
- Official automatic-substitution comparison
- Reconstruction of original XI membership from finalized historical picks

**Known limitation:** Historical FPL picks may reflect finalized automatic substitutions. Original bench priority cannot always be recovered, so independent historical substitution replay is not yet fully supported.

## 🛠️ Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Core application and analytics |
| Requests | FPL API integration |
| Fantasy Premier League API | Football and manager data |
| Git & GitHub | Version control |
| VS Code | Development environment |
| Python tests | Functional and scoring validation |

## 📁 Project Structure

```text
FPL-Manager-Analytics-App/
├── api/
│   └── fpl_client.py
├── tracker/
│   ├── squad_tracker.py
│   ├── player_performance.py
│   ├── gameweek_snapshot.py
│   ├── manager_timeline.py
│   └── scoring_engine.py
├── tests/
├── docs/
│   └── data-model.md
├── .gitignore
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3
- Git
- Internet access for FPL API requests

### Installation

Clone the repository:

```bash
git clone https://github.com/Billyoung777/FPL-Manager-Analytics-App.git
cd FPL-Manager-Analytics-App
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run an existing test module:

```bash
python -m tests.test_squad_tracker
```

Other useful checks:

```bash
python -m tests.test_manager_timeline
python -m tests.test_scoring_engine
```

The project currently provides Python modules and test scripts rather than a finished graphical interface.

## 📊 Development Roadmap

| Milestone | Status |
| --- | --- |
| M0 — Project Foundation | Completed |
| M1 — FPL Data Engine | Completed core functionality |
| M2 — Manager Tracker | Completed core functionality |
| M3 — Analytics & Scoring Engine | In Progress |
| M4 — Mini-League Analytics | Planned |
| M5 — Database Integration | Planned |
| M6 — Interactive Dashboard | Planned |
| M7 — Automation | Planned |
| M8 — Testing & Release | Planned |

### Planned Features

- Full-season player contribution analysis
- Manager decision and transfer analytics
- Mini-league comparisons
- Persistent historical data storage
- Interactive analytics dashboard
- Automated gameweek updates
- Advanced FPL scoring validation

## 🧪 Testing

The project includes tests for API integration, squad tracking, player performance, gameweek snapshots, manager timelines, and scoring logic.

Initial gameweek score calculations have been checked against official FPL results for GW1–GW5 of the 2026/27 season.

Further testing is required for automatic substitutions, captain fallback, chip-specific scoring, and transfer deductions.

## 🎯 Project Objectives

This project is intended to demonstrate practical experience in:

- Python software development
- REST API integration
- Data collection and transformation
- Object-oriented programming
- Football data analytics
- Modular application architecture
- Software testing and debugging
- Git-based development workflows

## 👨‍💻 Developer

**Billyoung Lusenga**

IT Support Technician | Software Development & Networking Enthusiast

GitHub: [@Billyoung777](https://github.com/Billyoung777)

## ⚠️ Disclaimer

This is an independent, unofficial project developed for educational and portfolio purposes. It is not affiliated with or endorsed by the Premier League or Fantasy Premier League.

---

**Built with Python, football knowledge, and a passion for data-driven decision-making.**
