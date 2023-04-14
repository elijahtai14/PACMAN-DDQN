import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--stream",
    action="store_true",
    dest="stream",
    help="Open a page where you can see the agent learning (no image or data saved during execution)",
)
parser.add_argument(
    "--image",
    action="store_true",
    dest="image",
    help="Save data and images",
)
parser.add_argument(
    "--ghostbonus",
    action="store_true",
    dest="ghostbonus",
    help="no reward for eating a ghost or a strawberry",
)
parser.add_argument(
    "--ghostrev",
    action="store_true",
    dest="ghostrev",
    help="train a single NN, reversing actions under power pellet"
)
args = parser.parse_args()
