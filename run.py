import argparse
from Controller import Controller

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mbot control using Simple heuristics.')
    parser.add_argument('-p', required=True, dest='api_key', help='Your embod.ai API key')
    parser.add_argument('-a', required=True, dest='agent_ids', nargs='+', help='The ids of the agents you want to control')
    parser.add_argument('-H', default="wss://api.embod.ai/environment/3b3b315b-b6b2-4610-9590-f29fdc27a889", dest='host', help="The websocket host for the environment")

    args = parser.parse_args()

    controller = Controller(args.api_key, args.agent_ids, args.host)

    controller.start()
