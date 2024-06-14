from fastapi import Request
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser
from onelogin.saml2.auth import OneLogin_Saml2_Auth


IdPsettings: dict = OneLogin_Saml2_IdPMetadataParser.parse_remote(
    'https://mocksaml.com/api/saml/metadata')
settings = {
    "strict": False,
    "debug": True,
    "idp": IdPsettings.get('idp'),
    "security": {},
    "sp": {
        'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
        "entityId": "saml-client",
        "assertionConsumerService": {
            "url": "http://localhost:8000/api/saml2/assert/",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        }
    }
}


async def get_saml_auth(request: Request):
    form = await request.form()
    saml_request = {
        "http_host": request.client.host,
        "server_port": request.url.port,
        "script_name": request.url.path,
        "post_data": {
            "RelayState": form.get("RelayState"),
            "SAMLResponse": form.get("SAMLResponse")
        },
        "get_data": request.query_params,
    }
    auth = OneLogin_Saml2_Auth(saml_request, settings)
    return auth
