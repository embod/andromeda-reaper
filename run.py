import argparse
from Controller import Controller

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mbot control using Simple heuristics.')
    parser.add_argument('-p', required=True, dest='apikey', help='Your embod.ai API key')
    parser.add_argument('-a', required=True, dest='agent_id', help='The id of the agent you want to control')
    parser.add_argument('-H', default="wss://api.embod.ai", dest='host', help="The websocket host for the environment")

    args = parser.parse_args()

    controller = Controller(args.apikey, args.agent_id)

    controller.start()
