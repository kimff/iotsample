from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("", response_model=List[schemas.Device], summary="Return all devices")
def get_devices(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM devices""")
    # devices = cursor.fetchall()
    devices = (
        db.query(models.Device)
        .filter(models.Device.developer_id == current_user.user_id)
        .all()
    )
    return devices


@router.get("/{id}", response_model=schemas.Device, summary="Show a device")
def get_devices(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM devices WHERE id = %s""", (str(id)))
    # devices = cursor.fetchone()
    device = db.query(models.Device).filter(models.Device.device_id == id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"device with id: {id} not found",
        )
    if device.developer_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perfrom requested action",
        )
    return device


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a device"
)
def delete_device(
    id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM devices WHERE id = %s RETURNING *""", (str(id)))
    # deleted_device = cursor.fetchone()
    # conn.commit()
    deleted_device = db.query(models.Device).filter(models.Device.device_id == id)
    device = deleted_device.first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"device with device_id={id} does not exist",
        )
    if device.developer_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perfrom requested action",
        )
    deleted_device.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Device,
    summary="Create a device",
)
def create_device(
    device: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO devices (device_name, device_type, description, sensor_type,
    # location, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
    #     (
    #         device.device_name,
    #         device.device_type,
    #         device.description,
    #         device.sensor_type,
    #         device.location,
    #         device.user_id,
    #     ),
    # )
    # new_device = cursor.fetchone()
    # conn.commit()
    new_device = models.Device(developer_id=current_user.user_id, **device.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


@router.put("/{id}", response_model=schemas.Device, summary="Update a device")
def update_device(
    id: str,
    updated_device: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """UPDATE devices SET active = %s, device_name = %s, device_type = %s, description = %s, sensor_type = %s,
    # location = %s, user_id = %s WHERE id = %s RETURNING *""",
    #     (
    #         device.active,
    #         device.device_name,
    #         device.device_type,
    #         device.description,
    #         device.sensor_type,
    #         device.location,
    #         device.user_id,
    #         str(id),
    #     ),
    # )
    # updated_device = cursor.fetchone()
    # conn.commit()

    update_device_query = db.query(models.Device).filter(models.Device.device_id == id)
    device = update_device_query.first()

    if device == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"device with id={id} does not exist",
        )
    if device.developer_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perfrom requested action",
        )
    update_device_query.update(updated_device.dict(), synchronize_session=False)
    db.commit()
    return device
