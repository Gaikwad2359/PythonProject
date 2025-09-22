#!/usr/bin/env bash
uvicorn fresh_glssdoor_scraper:app --host 0.0.0.0 --port $PORT
