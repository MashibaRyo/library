from fastapi import APIRouter, Response, HTTPException, Depends, Path
from starlette import status

from users.auth import get_password_hash, create_access_token, authenticate_user
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.models import Users
from users.shemas import SUserAuth

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register")
async def register(user: SUserAuth, response: Response):
    existing_user = await UsersDAO.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    else:
        hashed_password = get_password_hash(user.hashed_password)
        await UsersDAO.create(name=user.name,
                              email=user.email,
                              hashed_password=hashed_password)

        user_id = await UsersDAO.find_id_by_email(user.email)
        access_token = create_access_token({"sub": str(user_id)})
        response.set_cookie(key="token", value=access_token, httponly=True)

        return "Successfully registered"

@router.post("/login")
async def login(user: SUserAuth, response: Response):
    user = await authenticate_user(user.email,
                                   user.hashed_password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = await UsersDAO.find_id_by_email(user.email)
    access_token = create_access_token({"sub": str(user_id)})
    response.set_cookie(key="token", value=access_token, httponly=True)
    return "Successfully logged in"


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="token")


@router.get("/me")
async def me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def all(current_user: Users = Depends(get_current_user)):
    return await UsersDAO().find_all()


@router.delete("/delete")
async def delete_user(response: Response, current_user: Users = Depends(get_current_user)):
    deleted_user = await UsersDAO().delete_user(user_id=current_user.id)
    response.delete_cookie(key="token")
    return deleted_user

@router.patch("/update")
async def update_user(user_data: SUserAuth):
    update_data = user_data.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    return await UsersDAO.update(user_id, update_data)
