from fastapi import FastAPI, Depends
from .database import engine
from . import models
from .routers import device, user, auth, stream
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from fastapi.responses import HTMLResponse
from . import schemas, models, oauth2

# import random
from sqlalchemy.orm import Session
from .database import get_db
import json

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(device.router)
app.include_router(stream.router)
app.include_router(user.router)
app.include_router(auth.router)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/live");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/ws")
async def get():
    return HTMLResponse(str(html))


# @app.websocket("/ws/live")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


# @app.websocket("/ws/sample")
# async def websocket_endpoint(websocket: WebSocket):
#     print("Accepting client connection...")
#     await websocket.accept()
#     while True:
#         try:
#             # Wait for any message from the client
#             await websocket.receive_text()
#             # Send message to the client
#             resp = {"value": random.uniform(0, 1)}
#             await websocket.send_json(resp)
#         except Exception as e:
#             print("error:", e)
#             break
#     print("Bye..")


@app.websocket("/ws/live/{device_id}")
async def websocket_stream_by_device(
    websocket: WebSocket, device_id: str, db: Session = Depends(get_db)
):
    print("Accepting client connection...")
    await websocket.accept()
    # websocket.send_text("Connection established !!")

    def new_messages():
        check_count = (
            db.query(models.Data).filter(models.Data.device_id == device_id).count()
        )

        if check_count == 0:
            return None
        else:
            return True

    previous_data = ""

    while True:
        if new_messages():
            data_stream = (
                db.query(models.Data)
                .filter(models.Data.device_id == device_id)
                .order_by(models.Data.id.desc())
                .first()
            )

            if dict(data_stream.data) != previous_data:
                print("new entry detected..")
                await websocket.send_json(json.dumps(dict(data_stream.data)))
                # await websocket.send_text(str(dict(data_stream.data)))
                # await websocket.send_text(str(dict(data_stream.data)))
            previous_data = dict(data_stream.data)
