from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from controllers import deviceController, commandsController
from services.mqttClientService import MQTTClientService
from contextlib import asynccontextmanager
from logging_setup import setup_logging
from loguru import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt = MQTTClientService()
    app.state.mqtt = mqtt
    logger.info("Starting MQTT client")
    await mqtt.start()
    yield
    await mqtt.stop()

def create_app() -> FastAPI:
    load_dotenv()
    setup_logging()

    app = FastAPI(
        title="Gnosis IoT",
        description="Gnosis IoT is a platform for managing IoT devices and their operations.",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/iot/docs",
        openapi_url="/iot/openapi.json",
        redoc_url="/iot/redoc"
    )

    app.include_router(deviceController.router)
    app.include_router(commandsController.router)

    # CORS configuration
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()