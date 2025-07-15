from fastapi import Depends, HTTPException, status
from app.database import DBConnection

def get_db_conn() -> Generator[Session, None, None]:
    with Session(DBConnection) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db_conn)]