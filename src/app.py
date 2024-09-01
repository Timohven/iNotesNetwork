import uvicorn
from fastapi import FastAPI, Request, Cookie
# from fastapi.responses import Response
from web import note
# import fake.note as service
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="C:/Users/ukrse/PycharmProjects/iNotesNetwork/src/uploads"), name="static")
app.include_router(note.router)


@app.get("/")
async def index(request: Request, user: str = Cookie(None)):
    print('Current user is:', user, '!')
    return {"message": user}


# @app.post("/setcookie/")
# async def setcookie(request: Request, response: Response, user: str='Admin'):
#     response.set_cookie(key="user", value=user)
#     return {"message": "Hello World"}


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
