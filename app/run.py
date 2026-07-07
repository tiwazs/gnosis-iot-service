import uvicorn
from dotenv import load_dotenv, find_dotenv
import os

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    uvicorn.run("main:app", host=os.getenv("SERVER_HOST"), port=int(os.getenv("SERVER_PORT")), log_level=os.getenv("LOGGER_LEVEL"), reload=True)
