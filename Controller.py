import numpy as np
import embod_client as client
from state_stack import StateStack
from uuid import UUID

class Controller:

    def __init__(self, api_key, agent_ids, host):

        self._states = StateStack()
        self._counter = 1

        self._agent_ids = [UUID(agent_id) for agent_id in agent_ids]

        self._client = client.AsyncClient(api_key, self._connect_callback, self._state_callback, host)

    async def _connect_callback(self):
        for agent_id in self._agent_ids:
            await self._client._add_agent(agent_id)

    async def _state_callback(self, agent_id, state, reward, error):

        if error is not None:
            print(error[0].decode('UTF-8'))

        if not self._counter % 5:
            mbot_sensor, food_sensor, poison_sensor, xvelocity, yvelocity, zvelocity = self._states.split_means()

            max_food_sensor, food_direction = self._get_sensor_direction(food_sensor)
            max_poison_sensor, poison_direction = self._get_sensor_direction(poison_sensor)

            # Always move forwards at the same speed
            xForce = 0.1

            # No sideways motion
            yForce = 0.0

            # Turn towards the food
            zRotationForce = 0.004 * (food_direction)

            if poison_direction == 0 and max_poison_sensor > max_food_sensor:
                # Turn away from poison if we are heading for it
                zRotationForce += 0.4

            action = [xForce, yForce, zRotationForce]

            await self._client.send_agent_action(agent_id, action)

        if reward is not None:
            if reward > 0:
                print("food consumed :)")

            if reward < 0:
                print("poison consumed :(")

        self._states.add_state(state)
        self._counter += 1

    def _get_sensor_direction(self, sensor):
        argmax = np.argmax(sensor)
        return sensor[argmax], (argmax - 5)

    def start(self):
        self._client.start()