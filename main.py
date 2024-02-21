import os
from fastapi import FastAPI, Request
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


@app.message()
def say_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
