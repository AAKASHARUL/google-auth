from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from app.config import settings
from app.dependencies import get_db
from . import services, schemas

router = APIRouter()

# Setup Authlib for Google
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get('/login/google')
async def login_via_google(request: Request):
    # Redirects the user to the Google Login page.
    redirect_uri = request.url_for('auth_via_google') 
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth', name='auth_via_google')
async def auth_via_google(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(status_code=400, detail='Could not authenticate with Google')

        # Check if user exists, otherwise create new
        existing_user = services.get_user_by_email(db, email=user_info['email'])
        
        if not existing_user:
            new_user_data = schemas.UserCreate(
                email=user_info['email'],
                google_id=user_info['sub'],
                full_name=user_info.get('name'),
                picture=user_info.get('picture')
            )
            existing_user = services.create_google_user(db, new_user_data)

        # Generate internal JWT token for your frontend to use
        access_token = services.create_access_token(data={'sub': existing_user.email})

        return {
            'message': 'Login Successful',
            'access_token': access_token,
            'token_type': 'bearer',
            'user': {
                'email': existing_user.email,
                'name': existing_user.full_name
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
