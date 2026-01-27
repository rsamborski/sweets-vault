# LED Matrix API

FastAPI service for controlling a 32x16 LED Matrix.

## Description

This API allows controlling a 32x16 LED Matrix divided into two 16x16 sections.
You can set a character and a locked/unlocked status icon for each section.

## Wiring

This API should be run on a Raspberry Pi device with a 32x16 LED Matrix connected
to it. For wiring please refer to
[wiring.md](https://github.com/hzeller/rpi-rgb-led-matrix/blob/02fb09a6099c84b7bc76cdfa231338d8ca81ed6d/wiring.md)

## Configuration

1.  Copy `.env.template` to `.env`:
    ```bash
    cp .env.template .env
    ```
2.  Edit `.env` and set your secret API key:
    ```
    LED_API_KEY=your-secret-key
    ```

## Installation

Using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

## Running

The API server needs to be run as `root` due to improved performance of the RGBMatrix library.

```bash
sudo /path/to/uv run main.py
```

## Authentication

All API endpoints require an API Key passed in the header:
`X-API-Key: <your-secret-key>`

## Usage

### Examples

#### Python

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "your-secret-key"
HEADERS = {"X-API-Key": API_KEY}

# Set Section 0 to 'A' and Locked
requests.post(
    f"{API_URL}/section/0",
    headers=HEADERS,
    json={"char": "A", "locked": True}
)

# Clear Matrix
requests.post(
    f"{API_URL}/clear",
    headers=HEADERS
)
```

#### Curl

**Set Section 1 to 'B' and Unlocked:**

```bash
curl -X POST "http://localhost:8000/section/1" \
     -H "X-API-Key: your-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"char": "B", "locked": false}'
```

**Clear Matrix:**

```bash
curl -X POST "http://localhost:8000/clear" \
     -H "X-API-Key: your-secret-key"
```
