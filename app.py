import os
import secrets
import uvicorn
from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from contextlib import asynccontextmanager
from fastapi.openapi.docs import get_swagger_ui_html
from src.config.config import PORT
from src.cronjob.reddit_cronjob import run_reddit_cronjob


VALID_USERNAME = os.getenv('SWAGGER_USERNAME')
VALID_PASSWORD = os.getenv('SWAGGER_PASSWORD')
SWAGGER_LOCKED = os.getenv('SWAGGER_LOCKED',"true")



    
@asynccontextmanager
async def lifespan(app: FastAPI):
    run_reddit_cronjob()
    
    yield


app = FastAPI(docs_url=None, redoc_url=None,lifespan=lifespan)


security = HTTPBasic()



if str(SWAGGER_LOCKED) in ["true","True"]:

    @app.get("/docs")
    def get_docs(credentials: HTTPBasicCredentials = Depends(security)):
        correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
        correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")

else:

    @app.get("/docs")
    def get_docs():
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")



@app.get('/')
async def root():
    return {'message': 'Health OK'}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)