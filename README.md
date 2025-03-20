# Giphy Reddit GIF Data Collector

This repository automatically collects Giphy Reddit GIF JSON data on a daily basis and maintains a historical record of the data.

## Overview

- Data is collected daily at 04:00 UTC
- Historical data is maintained in `data.json`
- Each entry includes a timestamp and the collected data
- Uses GitHub Actions for automated collection

## Structure

- `data.json`: Contains the accumulated JSON data
- `fetch_data.py`: Python script for fetching and processing the data
- `.github/workflows/fetch-data.yml`: GitHub Actions workflow configuration

## Data Format

The data is stored in the following structure:

```json
{
  "entries": [
    {
      "timestamp": "2025-03-20 04:21:08",
      "data": {
        // Giphy Reddit GIF data
      }
    }
  ]
}
```

## Setup

1. Repository is automatically configured to fetch data
2. No additional configuration required
3. Manual runs can be triggered from the Actions tab

## Author

Created by @hhassan1230

```

```
