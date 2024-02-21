import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv()

api = FastAPI()
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app)


@api.get("/status")
async def test():
    return {"status": "This is working!"}


@api.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)


@api.get("/hi-kevan")
async def hi_kevan():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Proxmox Slack Test</title>
    </head>
    <body>
        <h1>Yooo Kevan!</h1>
        <h2>Check this proxmox business out!</h2>
        <h3><a href="https://github.com/JNaeder/proxmox_slack_test" 
        target="_blank">GitHub Repo</a></h3>
        <h3>Super simple slack app for testing shit</h3>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.message()
def say_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8000)
