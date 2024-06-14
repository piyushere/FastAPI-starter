from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse, Response
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from src.middlewares.saml2 import get_saml_auth
from src.middlewares.auth import authorize, generate_token
auth_router = APIRouter()


@auth_router.get('/login')
async def login(auth: OneLogin_Saml2_Auth = Depends(get_saml_auth)):
    callback_url = auth.login(return_to="/api/saml2/whoami")
    return RedirectResponse(url=callback_url)


@auth_router.post('/assert')
async def validate(auth: OneLogin_Saml2_Auth = Depends(get_saml_auth)):
    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        if not auth.is_authenticated():
            return Response(
                'authentication unsuccessful: please check your credentials',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        attributes = auth.get_attributes()
        token = generate_token(attributes)
        response = RedirectResponse(
            '/api/saml2/whoami',
            status_code=status.HTTP_301_MOVED_PERMANENTLY
        )
        response.set_cookie('auth_session', token)
        return response
    else:
        # TODO log the errors
        return Response(
            'Unexpted error during authentication',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@auth_router.get('/logout')
async def logout(auth: OneLogin_Saml2_Auth = Depends(get_saml_auth)):
    response = RedirectResponse('/')
    response.set_cookie('auth_session', None)
    return response
    # logout_url = auth.logout()
    # RedirectResponse(logout_url)
    # return 'logout'


@auth_router.get('/whoami', dependencies=[Depends(authorize)])
async def whoami(request: Request):
    return request.state.user
