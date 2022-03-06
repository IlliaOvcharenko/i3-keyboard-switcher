#!/usr/bin/python3

import sys
import json
import subprocess

from fire import Fire
from pathlib import Path


def get_layout():
    out = subprocess.run(["setxkbmap", "-query"],
                         stdout=subprocess.PIPE)
    out = out.stdout.decode("utf-8")
    out = [l for l in out.split("\n") if l != ""]
    out = {l.split(":")[0]: l.split(":")[1].strip() for l in out}
    layout = out["layout"]
    return layout


def set_layout(layout_name):
    out = subprocess.run(["setxkbmap", layout_name])


class KeyboardSwitcher:
    def __init__(self):
        # print(f"work directory: {Path.cwd()}")

        self.layouts = []
        self.current_layout = None
        self.order_mode = "recent_use"

        self.state_file = Path("keyboard_switcher_state.json")
        if self.state_file.exists():
            self.load_state()
            set_layout(self.current_layout)

    def load_state(self):
        with open(self.state_file) as f:
            data = json.load(f)
            self.layouts = data["layouts"]
            self.current_layout = data["current_layout"]
            self.recent_layout = data["recent_layout"]

    def save_state(self):
        with open(self.state_file, "w") as f:
            state = {
                        "layouts": self.layouts,
                        "current_layout": self.current_layout,
                        "recent_layout": self.recent_layout
                    }
            json.dump(state, f)

    def set_layout_list(self, *layouts):
        self.layouts = layouts
        self.current_layout = self.layouts[0]
        self.recent_layout = self.current_layout

        set_layout(self.current_layout)
        self.save_state()

    def next_layout(self):
        self.current_layout, self.recent_layout = \
            self.recent_layout, self.current_layout
        set_layout(self.current_layout)
        self.save_state()

    def set_layout_by_order(self, num):
        assert num < len(self.layouts), "layout number is out of order"

        self.recent_layout = self.current_layout
        self.current_layout = self.layouts[num]

        set_layout(self.current_layout)
        self.save_state()

    def print_current_layout(self):
        layout = get_layout()
        print(layout)

    def i3_status(self):
        for line in sys.stdin:
            if line[0] == ",":
                line = line[1:]
                line = json.loads(line)
                line.append({
                    "name": "kblayout",
                    "full_text": f"🖖🏻 {get_layout()}",
                })
                line = json.dumps(line)
                line = "," + line
            sys.stdout.write(line)
            sys.stdout.flush()


if __name__ == "__main__":
    Fire(KeyboardSwitcher)

