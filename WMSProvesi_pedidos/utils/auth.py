import json
from jose import jwt
from urllib.request import urlopen
from django.http import JsonResponse

AUTH0_DOMAIN = "dev-146s3z5mxd0jafdm.us.auth0.com"
API_IDENTIFIER = "https://wmsprovesi-api"
ALGORITHMS = ["RS256"]

def get_token_auth_header(request):
    auth = request.headers.get("Authorization", None)
    print("🔎 Header recibido:", auth)
    if not auth:
        return JsonResponse({"message": "No Authorization header"}, status=401)
    parts = auth.split()
    if parts[0].lower() != "bearer":
        return JsonResponse({"message": "Authorization header must start with Bearer"}, status=401)
    elif len(parts) == 1:
        return JsonResponse({"message": "Token not found"}, status=401)
    token = parts[1]
    return token

def requires_auth(view_func):
    def wrapper(request, *args, **kwargs):
        token = get_token_auth_header(request)
        try:
            jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_IDENTIFIER, issuer=f"https://{AUTH0_DOMAIN}/")
        except Exception as e:
            return JsonResponse({"message": f"Token inválido: {str(e)}"}, status=401)
        request.user_auth0 = payload
        return view_func(request, *args, **kwargs)
    return wrapper
