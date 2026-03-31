from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import os

from database import SessionLocal, engine, Base
import models
from auth import hash_password, verify_password

# Create tables (after DB is ready)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ IMPORTANT: use correct variable name
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory="templates")

# ---------------- DB Dependency ---------------- #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- HOME ---------------- #
@app.get("/")
def home():
    return RedirectResponse("/login")

# ---------------- SIGNUP ---------------- #
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if user:
        return {"message": "User already exists"}

    new_user = models.User(
        email=email,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()

    return RedirectResponse("/login", status_code=303)

# ---------------- LOGIN ---------------- #
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    # If user not found → redirect to signup
    if not user:
        return RedirectResponse("/signup", status_code=303)

    # Check password
    if not verify_password(password, user.password):
        return {"message": "Incorrect password"}

    return {"message": f"Welcome {email} 🎉"}