#!/usr/bin/env bash
if [ "$RENDER" = "true" ]; then
  uvicorn fresh_glassdoor_scraper:app --host 0.0.0.0 --port $PORT
else
  uvicorn fresh_glassdoor_scraper:app --host 127.0.0.1 --port 8000 --reload
fi
