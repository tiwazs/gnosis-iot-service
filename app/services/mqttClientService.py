import asyncio
import os
import aiomqtt

class MQTTClientService:
    def __init__(self):
        self.host = os.getenv("MQTT_HOST")
        self.port = int(os.getenv("MQTT_PORT"))
        self.task: asyncio.Task | None = None

    async def start(self):
        self.task = asyncio.create_task(self.run())

    async def run(self):
        topic = "gnosis/+/devices/+/coordinates"

        # Infinite loop to keep the client running even if the connection is lost
        while True:
            try:
                print(f"Connecting to MQTT broker at {self.host}:{self.port}")
                async with aiomqtt.Client(
                        self.host, 
                        self.port,
                        username=os.getenv("MQTT_USERNAME"),
                        password=os.getenv("MQTT_PASSWORD"),
                    ) as client:

                    await client.subscribe(topic)
                    print(f"Subscribed to topic: {topic}")
                    async for message in client.messages:
                        await self.handle_message(message)
            except Exception as e:
                print(f"Error in MQTT client: {e}")
                await asyncio.sleep(5)
    
    async def handle_message(self, message: aiomqtt.Message):
        # Getting the workspace id and device id from the topic
        topic = str(message.topic)

        parts = topic.split("/")
        workspace_id = parts[1]
        device_id = parts[3]
        payload = message.payload.decode()

        print(f"Received message from {workspace_id}/{device_id}: {payload}")

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            finally:
                self.task = None
                print("MQTT client stopped")

