#!/usr/bin/env bash
uvicorn fresh_glassdoor_scraper:app --host 0.0.0.0 --port $PORT
