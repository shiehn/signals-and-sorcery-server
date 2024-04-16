#!/usr/bin/env python3

import argparse
import time
import random

from runes_client import ui_param

parser = argparse.ArgumentParser(description="Connect to DAWNet server.")
parser.add_argument("token", help="Token for DAWNet server connection")
args = parser.parse_args()

import runes_client as runes
from runes_client.core import DAWNetFilePath


#@ui_param("a", "DAWNetNumberSlider", min=0, max=10, step=1, default=5)
# @ui_param('c', 'DAWNetMultiChoice', options=['cherries', 'oranges', 'grapes'], default='grapes')
async def arbitrary_method(input_file: DAWNetFilePath):
    try:
        print(f"Input File: {input_file}")

        # Pause execution for a random number of seconds between 1 and 30
        sleep_time = random.randint(1, 30)
        print(f"Pausing for {sleep_time} seconds")
        time.sleep(sleep_time)


        await runes.output().add_file(input_file)
        await runes.output().add_message("This is a message send to the plugin")

        return True
    except Exception as e:
        await runes.output().add_error(f"This is an error sent to the plugin: {e}")

        return False


runes.set_input_target_format("wav")
runes.set_input_target_channels(2)
runes.set_input_target_sample_rate(44100)
runes.set_input_target_bit_depth(16)

runes.set_output_target_format("wav")
runes.set_output_target_channels(2)
runes.set_output_target_sample_rate(44100)
runes.set_output_target_bit_depth(16)

runes.set_token(token=args.token)
runes.set_name("DAWNet Template")
runes.set_description(
    "This is a template intended as a starting place to create custom DAWNet functions."
)
runes.register_method(arbitrary_method)


print("REGISTERED TOKEN & " + str(arbitrary_method))
runes.connect_to_server()
