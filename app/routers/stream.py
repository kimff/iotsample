from urllib import request
from fastapi import (
    FastAPI,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Request,
)
from sse_starlette.sse import EventSourceResponse
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List
import uuid
import asyncio

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 5000  # milisecond

router = APIRouter(prefix="/streams", tags=["Data"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DataStream,
    summary="Create a data stream",
)
def create_stream(
    data: schemas.DataStreamCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    new_data = models.Data(
        developer_id=current_user.user_id, stream_id=str(uuid.uuid4()), **data.dict()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.get("", response_model=List[schemas.DataStream], summary="Return all stream")
def get_streams(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM devices""")
    # devices = cursor.fetchall()
    data_stream = (
        db.query(models.Data)
        .filter(models.Data.developer_id == current_user.user_id)
        .all()
    )
    db.close()
    return data_stream


@router.get(
    "/{device_id}",
    response_model=List[schemas.DataStream],
    summary="Return all stream that belong to a certain device",
)
def get_stream_by_device(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    data_stream = db.query(models.Data).filter(models.Data.device_id == device_id).all()
    db.close()
    return data_stream


@router.get(
    "/live/{device_id}",
    summary="client auto update (SSE)",
)
async def get_stream_live_by_device(
    requests: Request, device_id: str, db: Session = Depends(get_db)
):
    def new_messages():
        check_count = (
            db.query(models.Data).filter(models.Data.device_id == device_id).count()
        )

        if check_count == 0:
            return None
        else:
            return True

    async def event_generator():
        previous_data = ""
        while True:
            if await requests.is_disconnected():
                print("Client disconnected!")
                break

            if new_messages():
                data_stream = (
                    db.query(models.Data)
                    .filter(models.Data.device_id == device_id)
                    .order_by(models.Data.id.desc())
                    .first()
                )

                if dict(data_stream.data) != previous_data:
                    yield {
                        "data": [
                            dict(data_stream.data),
                            {
                                "date": str(data_stream.created_at),
                                "developer_id": str(data_stream.developer_id),
                                "device_id": str(data_stream.device_id),
                                "stream_id": str(data_stream.stream_id),
                            },
                        ]
                    }
                    previous_data = dict(data_stream.data)
            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())
