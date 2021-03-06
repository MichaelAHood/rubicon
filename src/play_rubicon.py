"""
This script has 4 main steps:
- It uses Chromedriver to open a browser and navigate to the target URL.
- It creates some formatted Javascript to run via Chromedriver.
- It polls browser local storage to determine when the game starts.
- On every iteration of the game it plays the move designated by the policy until the game is over.
"""

import argparse
import time
from string import Template

from selenium import webdriver

from utils import (LocalStorage, get_game_state, get_js_helpers,
                   get_manual_policies)

GAME_URL = "https://rubicon-eng.synthesis.is"


def main(policy_name):
    print(f"Running with policy: {policy_name}")
    policy = get_manual_policies()[policy_name]
    js_helpers = get_js_helpers()

    driver = webdriver.Chrome(executable_path="chromedriver")
    storage = LocalStorage(driver)

    # Open the page and wait it for it to load and for the user
    # to paste contents of js/auto-move-override.js to src/auto-move.js in the browser
    driver.get(GAME_URL)
    time.sleep(10)

    # JS to be executed by web driver
    play_game_template = Template(js_helpers["play_game_template"])
    play_game_routine = play_game_template.substitute(moves=policy)

    # Await start of the game
    game_state = None
    count = 1
    while not game_state:
        if count % 100 == 0:
            print("Setup complete. Ready to start the game")
        time.sleep(0.1)
        game_state = get_game_state(storage)

    # As long as the game is in play, run the JS routine
    while game_state["playing"]:
        driver.execute_script(play_game_routine)
        time.sleep(0.1)
        game_state = get_game_state(storage)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--policy",
        type=str,
        dest="policy",
        help="Choose one of 'baby', 'julius', or 'caesar'.",
    )
    args = parser.parse_args()

    main(args.policy)
