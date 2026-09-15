# FPL Manager Analytics — Data Model

## Purpose

This document defines the data structure used by the FPL Manager Analytics system.

The system must support tracking one or more FPL managers from GW1 through GW38.

---

## 1. Manager

Represents an FPL manager.

### Fields

- `manager_id`
- `team_name`
- `player_first_name`
- `player_last_name`

---

## 2. Gameweek

Represents a manager's performance during a specific gameweek.

### Fields

- `gameweek`
- `points`
- `total_points`
- `overall_rank`
- `bank`
- `team_value`
- `event_transfers`
- `event_transfers_cost`
- `points_on_bench`

---

## 3. Squad

Represents the manager's 15-player squad for a gameweek.

### Fields

## 3. Squad

### Fields

- `player_id`
- `player_name`
- `position`
- `starting`
- `captain`
- `vice_captain`
- `multiplier`

A squad contains up to 15 players.

---

## 4. Player Gameweek Performance

Represents a player's performance during a specific gameweek.

## 4. Player Gameweek Performance

### Fields

- `player_id`
- `gameweek`
- `team`
- `position`
- `minutes`
- `points`
- `goals`
- `assists`
- `clean_sheets`
- `bonus`
- `bps`
- `yellow_cards`
- `red_cards`
- `saves`

---

## 5. Transfers

Represents transfer activity associated with a manager and gameweek.

### Fields

- `gameweek`
- `player_out`
- `player_in`
- `transfer_cost`
- `transfer_time`

Transfers must be interpreted together with chips.

A Wildcard represents a squad rebuild and should not be treated as a normal transfer decision.

---

## 6. Chips

Represents chips used by a manager.

### Fields

- `gameweek`
- `chip_name`
- `time_used`

Supported chip types may include:

- Wildcard
- Free Hit
- Bench Boost
- Triple Captain

---

## 7. Relationships

The main relationship structure is:

Manager
→ Gameweek
→ Squad
→ Player
→ Player Gameweek Performance

Manager
→ Gameweek
→ Transfers

Manager
→ Gameweek
→ Chips

---

## 8. Manager Gameweek Snapshot

A complete manager gameweek snapshot combines:

- Manager information
- Gameweek performance
- Squad
- Starting XI
- Bench
- Captain
- Vice-captain
- Player performance
- Transfers
- Chips

Conceptually:

Manager
→ GW
→ Performance
→ Squad
→ Player Performance
→ Transfers
→ Chips

---

## 9. Historical Tracking

The system must support:

- GW1 through GW38
- Multiple managers
- Historical squads
- Player ownership by gameweek
- Player performance while owned
- Transfers
- Chips
- Gameweek scores
- Overall rank movement

---

## 10. Future Analytics

This data model should support future calculations including:

- Points while player was owned
- Goals while player was owned
- Assists while player was owned
- Clean sheets while player was owned
- Captaincy performance
- Bench points
- Transfer impact
- Chip impact
- Manager performance trends
- Mini-league comparisons
