from services.mqttClientService import MQTTClientService

class CommandsService:
    def __init__(self, mqtt_client: MQTTClientService):
        self.mqtt_client = mqtt_client
        self.commands = {
            1: {
                'id': 1,
                'name': 'turn_camera_on',
                'description': 'Turn the camera on',
                'command': 'turn_camera_on',
            },
            2: {
                'id': 2,
                'name': 'turn_camera_off',
                'description': 'Turn the camera off',
                'command': 'turn_camera_off',
            }
        }
        
    async def send_command(self, command_id: int, data: dict = None):

        topic = f"gnosis/{workspace_id}/devices/{device_id}/commands"

        payload = {
            'command_id': command_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'data': data,
            'command': self.commands[command_id]['command'],
        }
        if command in self.commands:
            await self.mqtt_client.publish(topic, json.dumps(payload))
        else:
            return None
            