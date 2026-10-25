
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

app = FastAPI(title="Documentation Agent")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Documentation Agent is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/sessions",
    response_model=schemas.DocumentationSessionResponse,
    status_code=201,
)
def create_session(
    session_data: schemas.DocumentationSessionCreate,
    db: Session = Depends(get_db),
):
    return crud.create_session(db, session_data)


@app.get(
    "/sessions",
    response_model=list[schemas.DocumentationSessionResponse],
)
def list_sessions(db: Session = Depends(get_db)):
    return crud.get_all_sessions(db)


@app.get(
    "/sessions/{session_id}",
    response_model=schemas.DocumentationSessionResponse,
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    db_session = crud.get_session(db, session_id)

    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return db_session


@app.post(
    "/sessions/{session_id}/steps",
    response_model=schemas.DocumentationStepResponse,
    status_code=201,
)
def add_step(
    session_id: int,
    step_data: schemas.DocumentationStepCreate,
    db: Session = Depends(get_db),
):
    step = crud.add_step(db, session_id, step_data)

    if step is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return step
