import asyncio
import os
import aiomqtt
from loguru import logger


class MQTTClientService:
    def __init__(self):
        self.host = os.getenv("MQTT_HOST")
        self.port = int(os.getenv("MQTT_PORT"))
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
                logger.info("Connecting to MQTT broker at {}:{}", self.host, self.port)
                async with aiomqtt.Client(
                        self.host,
                        self.port,
                        username=os.getenv("MQTT_USERNAME"),
                        password=os.getenv("MQTT_PASSWORD"),
                    ) as client:
                    
                    self.client = client

                    await self.client.subscribe(topic)
                    logger.info("Subscribed to topic: {}", topic)
                    
                    await self.handle_messages(self.client)

            except Exception as e:
                logger.warning("Error in MQTT client, retrying in 5s: {}", e)
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
