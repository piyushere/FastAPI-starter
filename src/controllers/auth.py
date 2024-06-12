from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from src.middlewares.auth import get_saml_auth


auth_router = APIRouter()


@auth_router.get('/login')
async def login(auth: OneLogin_Saml2_Auth = Depends(get_saml_auth)):
    callback_url = auth.login(
        return_to="http://localhost:8000/api/saml2/whoami")
    return RedirectResponse(url=callback_url)


@auth_router.post('/assert')
async def validate(auth: OneLogin_Saml2_Auth = Depends(get_saml_auth)):
    auth.process_response()
    print(auth.get_attributes())
    if not auth.get_errors() and auth.is_authenticated():
        attributes = auth.get_attributes()
        return attributes
    else:
        return auth.get_errors()


@auth_router.get('/logout')
async def logout():
    return 'logout'


@auth_router.get('/whoami')
async def whoami():
    return 'whoami'
