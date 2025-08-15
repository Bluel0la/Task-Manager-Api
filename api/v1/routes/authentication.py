from fastapi import APIRouter, HTTPException, status, Depends
from api.utils.authentication import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from api.utils.firebase import get_user_by_email, create_user
from api.v1.schemas.userSchema import UserSignin, UserSigninResponse, UserSignup, UserSignupResponse
from datetime import timedelta

auth = APIRouter(prefix="/auth", tags=["Authentication"])

@auth.post("/signup", response_model=UserSignupResponse)
def signup(user_data: UserSignup):
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = create_user(user_data)
    return {
        "id": user["id"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "username": user["username"],
        "role": user["role"],
        "created_at": user["created_at"],
    }

@auth.post("/signin", response_model=UserSigninResponse)
def signin(user_data: UserSignin):
    user = get_user_by_email(user_data.email)
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )

    return {
        "id": user["id"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "username": user["username"],
        "role": user["role"],
        "created_at": user["created_at"],
        "access_token": access_token
    }

@auth.get("/me", response_model=UserSigninResponse)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Returns the authenticated user's information using the JWT token.
    Sensitive fields like password_hash are not included.
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "firstname": current_user["firstname"],
        "lastname": current_user["lastname"],
        "username": current_user["username"],
        "role": current_user["role"],
        "created_at": current_user["created_at"]
    }