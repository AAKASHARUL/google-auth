from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.database import init_db
from app.user import routers as user_routers

# Initialize Database Tables
init_db()

app = FastAPI(title='Google Login Backend')

# Session Middleware is required for Authlib (OAuth) to work
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include User Router
app.include_router(user_routers.router, tags=['Authentication'])

@app.get('/')
def root():
    return {'message': 'Google Login API is running. Go to /login/google to sign in.'}
