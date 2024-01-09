from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Session, create_engine, select, Field
from typing import List
from passlib.context import CryptContext

# Database setup
engine = create_engine("postgresql+asyncpg://user:password@localhost/database")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# SQLModel classes
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    password: str = Field(max_length=50)


class Org(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    url: str
    notes: str


# FastAPI application
app = FastAPI()


def get_current_user(username: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

# FastAPI routes
@app.post("/register")
async def register_user(user: User):
    user.password = pwd_context.hash(user.password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


@app.post("/login")
async def login(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": user.username}


@app.get("/orgs", response_model=List[Org])
async def get_orgs(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        orgs = session.exec(select(Org).where(Org.user_id == user.id)).all()
    return orgs



