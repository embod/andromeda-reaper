import numpy as np
import embod_client as eb
from state_stack import StateStack

class Controller:

    def __init__(self, apikey, agent_id):

        self.states = StateStack()
        self._counter = 1

        self.eb = eb.AsyncClient(apikey, agent_id, self._state_callback)

    def _get_sensor_direction(self, sensor):
        argmax = np.argmax(sensor)
        return sensor[argmax], (argmax - 5)

    async def _state_callback(self, state, reward, error):

        if error is not None:
            print(error[0].decode('UTF-8'))
            self.eb.stop()

        if not self._counter % 5:
            mbot_sensor, food_sensor, poison_sensor, xvelocity, yvelocity, zvelocity = self.states.split_means()

            max_food_sensor, food_direction = self._get_sensor_direction(food_sensor)
            max_poison_sensor, poison_direction = self._get_sensor_direction(poison_sensor)

            # No sideways motion
            xForce = 0.1

            # Always move forwards at the same speed
            yForce = 0.0

            # Turn towards the food
            zRotationForce = 0.004 * (food_direction)

            if poison_direction == 0 and max_poison_sensor > max_food_sensor:
                # Turn away from poison if we are heading for it
                zRotationForce += 0.4

            action = [xForce, yForce, zRotationForce]

            await self.eb.send_agent_action(action)

        if reward is not None:
            if reward > 0:
                print("food consumed :)")

            if reward < 0:
                print("poison consumed :(")

        self.states.add_state(state)
        self._counter += 1

    def start(self):
        self.eb.start()