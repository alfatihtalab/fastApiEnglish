from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from dependencies import *
from models.models import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}, )


# get all users
@router.get("/")
async def read_users():
    """Get all users from database"""
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="No users")
        return [user for user in results]


@router.get("/{user_id}")
async def read_user(user_id: int):
    """Get user by id"""
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        user_match = {}
        for user in results:
            if user.id == user_id:
                user_match = user.dict()
        return user_match


# add new user

@router.post("/register")
async def add_user(user: User):
    """Create new user"""
    users = await read_users()
    users_imie = [u.imie for u in users]
    users_phone = [u.phone for u in users]
    user_dict = user.dict()
    # if user.account_id in [1001, 1002, 1003] and user.imie not in users_imie:
    if user.phone not in users_phone and user.imie not in users_imie:
        try:
            user.insert()
        except:
            return {"message": "error in transaction"}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="Can not added")

# delete user

@router.delete("/")
async def delete_user(phone: str):
    with Session(engine) as session:
        statement = select(User).where(User.phone == phone)

        results = session.exec(statement)
        # if not results.one():
        #     raise HTTPException(status_code=404, detail= f"No users with {phone}")
        try:
            user = results.one()
            session.delete(user)
            session.commit()
        except:
            raise HTTPException(status_code=404, detail=f"No users with {phone}")
        finally:
            return await read_users()
