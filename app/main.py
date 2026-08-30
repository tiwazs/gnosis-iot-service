from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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
        redoc_url="/iot/redoc",
        swagger_ui_parameters={"persistAuthorization": True},
    )

    app.include_router(deviceController.router, prefix="/iot")
    app.include_router(commandsController.router, prefix="/iot")

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        openapi_schema.setdefault("components", {})["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT from main-service login, or an API key. Paste the token only; Swagger sends Authorization: Bearer <token>.",
            }
        }
        openapi_schema["security"] = [{"bearerAuth": []}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

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