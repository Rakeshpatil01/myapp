import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from .crud import ConnectionManager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}", response_model=schemas.UserUpdate)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.dict(exclude_unset=True)
    db_user = crud.update_user(db, user_data, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/token")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    if not db_user.password == user.password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

manager = ConnectionManager()
MESSAGE_STREAM_DELAY = 2  # seconds


def new_messages():
    results = engine.execute("SELECT count(*) FROM sensors_view_1s")
    return None if results.fetchone()[0] == 0 else True


async def event_generator():
    if new_messages():
        connection = engine.raw_connection()
        with connection.cursor() as cur:
            cur.execute("DECLARE c CURSOR FOR TAIL sensors_view_1s")
            cur.execute("FETCH ALL c")
            for row in cur:
                yield row

    await asyncio.sleep(MESSAGE_STREAM_DELAY)


@app.websocket("/airquality")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            async for data in event_generator():
                await websocket.send_json(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
