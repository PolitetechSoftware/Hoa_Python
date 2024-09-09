# Project Setup Instructions

This document provides instructions for setting up and running the project locally. Follow the steps below to activate
the Python virtual environment, install dependencies, run Docker Compose, and start Celery workers.

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.x** (with `venv` module)
- **Docker Compose**

## Steps to Set Up the Project

### 1. Create and Activate the Virtual Environment

Create a Python virtual environment to isolate the project's dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 2. Install the Python Dependencies

```bash 
pip install -r requirements.txt
```

### 3. Run Docker Compose

You need to install docker compose before can run this command

```bash 
docker-compose up -d
```

### 4. Start the Celery Worker

Open new terminal and run the celery worker

```bash
celery -A celery_config worker --loglevel=info
```

### 5. Start collect metrics data

```bash
python3 metrics_collector.py
```
