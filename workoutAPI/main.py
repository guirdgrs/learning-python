from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routers import api_router

app = FastAPI(title='WorkoutAPI')
add_pagination(app)
app.include_router(api_router)
