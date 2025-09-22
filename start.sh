#!/usr/bin/env bash
echo "Starting application..."
echo "RENDER environment variable: $RENDER"
echo "PORT environment variable: $PORT"

if [ "$RENDER" = "true" ]; then
  echo "Starting in Render production mode on port $PORT"
  uvicorn fresh_glassdoor_scraper:app --host 0.0.0.0 --port $PORT
else
  echo "Starting in local development mode"
  uvicorn fresh_glassdoor_scraper:app --host 127.0.0.1 --port 8000 --reload
fi
