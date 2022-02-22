from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from dependencies import *
from models.models import *

router = APIRouter(
    prefix="/levels",
    tags=["levels"],
    responses={404: {"description": "Not found"}}, )


# get all levels
@router.get("/")
async def read_levels():
    """Get all users from database"""
    with Session(engine) as session:
        statement = select(Level)
        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="No users")
        return [level for level in results]

