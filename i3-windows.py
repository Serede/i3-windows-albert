#!/usr/bin/env python

# Choose the extension trigger:
_TRIGGER_ = "!"

# i3-windows Extension for Albert
#
# Author: Serede Sixty Six <serede.dev@gmail.com>
# Code licensed under MIT License.
__version__ = "1.0"

import sys
import json
import re

# Check that i3ipc-python is present.
try:
    import i3ipc
except ImportError:
    print("i3ipc-python is required.")
    print("You can install it using pip or your favourite package manager.")
    exit(1)

def get_windows(i3):
    # Get all windows in a dict {con_id => [name, desc]}
    windows = {}
    for window in i3.get_tree().leaves():
        id_ = window.id
        class_ = window.window_class
        ws = window.workspace().name
        name = "[{}] {}".format("Scratchpad" if ws == "__i3_scratch" else ws, class_)
        desc = window.name
        if id_ is None:
            # This is not an X window, ignore it.
            continue
        if window.focused:
            # This is the focused window, ignore it.
            continue
        windows[id_] = [name, desc]
    return windows

# Check first argument.
if(len(sys.argv) > 1):
    opcode = sys.argv[1]

    if opcode == "METADATA":
        metadata = {
                "iid": "org.albert.extension.external.v1",
                "id": "org.albert.extension.external.v1.i3-windows",
                "name": "i3-windows",
                "version": "v1.0",
                "author": "Serede Sixty Six",
                "dependencies": ["i3ipc-python"],
                "providesMatches": True,
                "providesFallbacks": False,
                "runTriggeredOnly": True,
                "triggers": [_TRIGGER_]
                }
        print(json.dumps(metadata))

    elif opcode == "NAME":
        print("i3-windows")

    elif opcode == "INITIALIZE":
        pass

    elif opcode == "FINALIZE":
        pass

    elif opcode == "SETUPSESSION":
        pass

    elif opcode == "TEARDOWNSESSION":
        pass

    elif opcode == "QUERY":
        # Check second argument.
        if(len(sys.argv) > 2):
            query = sys.argv[2][1:];
            # Connect to i3.
            i3 = i3ipc.Connection()
            # Window lookup.
            results = []
            for id_, [name, desc] in get_windows(i3).items():
                if(re.search(query, name, re.IGNORECASE) or re.search(query, desc, re.IGNORECASE)):
                        results.append({
                            "id": "i3-window-" + str(id_),
                            "name": name,
                            "description": desc,
                            "icon": "window-manager",
                            "actions": [{
                                "name": "i3-msg",
                                "command": "i3-msg",
                                "arguments": ['[con_id="' + str(id_) + '"] focus']
                                }]
                            })
            # Send results to Albert.
            print(json.dumps(results))

exit(0)
