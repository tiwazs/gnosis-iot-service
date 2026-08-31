import asyncio
import os
import ssl
import aiomqtt
from loguru import logger


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


class MQTTClientService:
    def __init__(self):
        self.host = os.getenv("MQTT_HOST")
        self.port = int(os.getenv("MQTT_PORT"))
        self.ssl_use = _env_bool("SSL_USE")
        self.task: asyncio.Task | None = None
        self.client: aiomqtt.Client | None = None

    async def publish(self, topic: str, payload: str):
        if self.client is None:
            raise Exception("MQTT client not initialized")

        await self.client.publish(topic, payload)

    async def start(self):
        self.task = asyncio.create_task(self.run())

    async def run(self):
        topic = "gnosis/+/devices/+/coordinates"

        # Infinite loop to keep the client running even if the connection is lost
        while True:
            try:
                logger.info(
                    "Connecting to MQTT broker at {}:{} (tls={})",
                    self.host,
                    self.port,
                    self.ssl_use,
                )
                tls_context = ssl.create_default_context() if self.ssl_use else None
                async with aiomqtt.Client(
                        self.host,
                        self.port,
                        username=os.getenv("MQTT_USERNAME"),
                        password=os.getenv("MQTT_PASSWORD"),
                        tls_context=tls_context,
                    ) as client:
                    
                    self.client = client

                    await self.client.subscribe(topic)
                    logger.info("Subscribed to topic: {}", topic)
                    
                    await self.handle_messages(self.client)

            except Exception:
                logger.exception(
                    "Error in MQTT client at {}:{} (tls={}), retrying in 5s",
                    self.host,
                    self.port,
                    self.ssl_use,
                )
                await asyncio.sleep(5)

    async def handle_messages(self, client: aiomqtt.Client):
        async for message in client.messages:
            await self.handle_message(message)

    async def handle_message(self, message: aiomqtt.Message):
        # Getting the workspace id and device id from the topic
        topic = str(message.topic)

        parts = topic.split("/")
        workspace_id = parts[1]
        device_id = parts[3]
        payload = message.payload.decode()

        logger.info("Received message from {}/{}: {}", workspace_id, device_id, payload)

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            finally:
                self.task = None
                logger.info("MQTT client stopped")
