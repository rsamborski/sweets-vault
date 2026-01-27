# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import board
import digitalio
import signal
import sys

# Drawers class
class Drawers:
    drawers = [
        digitalio.DigitalInOut(board.C0),
        digitalio.DigitalInOut(board.C1),
    ]

    def __init__(self):
        for drawer_id, drawer in enumerate(self.drawers):
            drawer.direction = digitalio.Direction.OUTPUT
            self.lock(drawer_id)    # lock by default

    def unlock(self, drawer_id):
        self.drawers[drawer_id].value = False
        print(f"Drawer {drawer_id} unlocked")

    def lock(self, drawer_id):
        self.drawers[drawer_id].value = True
        print(f"Drawer {drawer_id} locked")

    def do_for_all(self, func):
        for drawer_id, _ in enumerate(self.drawers):
            func(drawer_id)

# Global drawers object
drawers = Drawers()

# Handle closure gracefully
def graceful_exit(signum, frame):
    print(f"\nCaught signal {signum}. Unlocking all drawers")
    drawers.do_for_all(drawers.unlock)
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)
signal.signal(signal.SIGTERM, graceful_exit)

def main():
    while True:
        time.sleep(5)
        drawers.unlock(0)
        time.sleep(5)
        drawers.unlock(1)
        time.sleep(5)
        drawers.lock(0)
        time.sleep(5)
        drawers.lock(1)


if __name__ == "__main__":
    main()
