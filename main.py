"""
scapy-rtps-experimentation/main.py

Only run this file when launching the stack with Docker Compose. If you only
want to send packets to a certain IP, run the Python script
`amplification_vulnerability.py`, which takes in IPs from standard input.

This file sets up a simple web page on http://localhost where you enter the IP
address of the talker Docker container (see `talker/Dockerfile`). Upon
submitting, the crafted packet in `amplification_vulnerability.py` will be sent
to the talker container, which will then send packets to the collector-server
container.
"""

from typing import Annotated

from amplification_vulnerability import amplify_singular_ip
from fastapi import FastAPI, Form, status
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def basic_form():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Scanner Input</title>
        </head>
        <body>
            <form method="POST" action="/submit">
                <label for="ip">IP Address of Talker Docker Container</label>
                <input type="text" id="ip" name="ip">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/submit", status_code=status.HTTP_200_OK)
async def submit(ip: Annotated[str, Form()]):
    amplify_singular_ip(ip)
    return 200
