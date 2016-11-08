#!/usr/bin/env python

# i3-windows Extension for Albert
#
# Author: Serede Sixty Six <serede.dev@gmail.com>
#
# MIT License
# 
# Copyright (c) 2016 Serede Sixty Six
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    # Get all windows.
    windows = i3.get_tree().leaves()
    return create_lookup_table(windows)

def create_lookup_table(windows):
    # Create a lookup table from the given list of windows.
    # The returned dict is in the format window_name => con_id.
    rename_nonunique(windows)
    lookup = {}
    for window in windows:
        id_ = window.id
        class_ = window.window_class
        name = window.name
        if id_ is None:
            # This is not an X window, ignore it.
            continue
        if window.focused:
            # This is the focused window, ignore it.
            continue
        lookup[id_] = [class_, name]
    return lookup

def rename_nonunique(windows):
    # Rename all windows which share a name by appending an index.
    window_names = [window.name for window in windows]
    for name in window_names:
        count = window_names.count(name)
        if count > 1:
            for i in range(count):
                index = window_names.index(name)
                window_names[index] = "{} [{}]".format(name, i + 1)
    for i in range(len(windows)):
        windows[i].name = window_names[i]

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
                "triggers": ["!"]
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
            windows = get_windows(i3)
            results = []
            for id_, [class_, name] in windows.items():
                if(re.search(query, name, re.IGNORECASE)):
                        results.append({
                            "id": "i3-window-" + str(id_),
                            "name": class_,
                            "description": name,
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
