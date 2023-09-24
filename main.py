from fastapi import FastAPI, Response, status, Request

import database_connector
import jsoner

app = FastAPI()


async def validate(request: Request, call_next):
    is_valid = False

    auth_token = None
    if request.cookies.keys().__contains__("token"):
        auth_token = request.cookies.get('token')
    elif request.query_params.keys().__contains__('token'):
        auth_token = request.query_params.get("token")

    if auth_token is not None:
        cursor = database_connector.db.cursor()
        cursor.execute(f'select token from admin_access where token = "{auth_token}"')
        result = cursor.fetchall()
        is_valid = len(result) > 0
        cursor.close()

    if not is_valid:
        return Response("Unauthorized", status_code=401)
    response = await call_next(request)
    return response


@app.get("/auth")
async def auth(token: str, response: Response):
    response.set_cookie(key="token", value=token)
    return {"status": "authorized"}


@app.get("/profiles")
async def profiles():
    return jsoner.getProfiles()

@app.get("/reports")
async def reports(filter: str = None):
    return jsoner.getReports(filter)


app.middleware("http")(validate)
