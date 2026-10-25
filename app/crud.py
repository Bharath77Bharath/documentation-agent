
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


def create_session(
    db: Session,
    session_data: schemas.DocumentationSessionCreate,
) -> models.DocumentationSession:
    db_session = models.DocumentationSession(
        title=session_data.title
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session


def get_session(
    db: Session,
    session_id: int,
) -> models.DocumentationSession | None:
    return (
        db.query(models.DocumentationSession)
        .options(selectinload(models.DocumentationSession.steps))
        .filter(models.DocumentationSession.id == session_id)
        .first()
    )


def get_all_sessions(
    db: Session,
) -> list[models.DocumentationSession]:
    return (
        db.query(models.DocumentationSession)
        .order_by(models.DocumentationSession.created_at.desc())
        .all()
    )


def add_step(
    db: Session,
    session_id: int,
    step_data: schemas.DocumentationStepCreate,
) -> models.DocumentationStep | None:
    db_session = get_session(db, session_id)

    if db_session is None:
        return None

    db_step = models.DocumentationStep(
        session_id=session_id,
        step_number=step_data.step_number,
        title=step_data.title,
        instructions=step_data.instructions,
        image_path=step_data.image_path,
    )

    db.add(db_step)
    db.commit()
    db.refresh(db_step)

    return db_step
