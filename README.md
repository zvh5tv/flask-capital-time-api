# Capital Time API

This is a simple Flask API that returns the current local time and UTC offset for a given capital city. It uses token-based authentication and integrates `geopy` and `timezonefinder` to determine location and timezone.

## Features

- Returns local time and UTC offset based on capital city name
- Secured with token-based authentication
- Lightweight and easy to run with Flask
- Includes a test route (`/api/hello`) to confirm the server is running

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flask-capital-time-api.git
cd flask-capital-time-api

## A request for Tokyo
curl -H "Authorization: Bearer supersecrettoken123" \
"http://34.133.233.43:5000/api/time?capital=Tokyo"

