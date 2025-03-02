import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from routes import pages, upload, gallery, chat
from config import UPLOAD_DIRECTORY
from fastapi.responses import FileResponse
from constants import HOST, PORT

app = FastAPI()

# Ensure static directory exists
STATIC_DIRECTORY = "static"
os.makedirs(STATIC_DIRECTORY, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(upload.router)
app.include_router(gallery.router)
app.include_router(chat.router)

# Ensure upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
