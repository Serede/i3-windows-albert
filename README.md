# i3-windows Extension for Albert

## Description
Intended for [i3-wm](http://i3wm.org/), this python script extends [Albert](https://github.com/ManuelSchneid3r/albert) in order to locate and focus windows from any workspace, including the scratchpad.

## Dependencies
- [Albert](https://github.com/ManuelSchneid3r/albert) (>= 0.8.11)
- [i3ipc-python](https://github.com/acrisci/i3ipc-python)

## Installation
Just copy `i3-windows.py` to your `~/.local/share/albert/external/` directory (create it if needed) and restart Albert.

## Usage
Write `!<pattern>` within Albert to find all windows related to `<pattern>`.
Note: You can change the default extension trigger `!` by modifying the `_TRIGGER_` value in the script.

## Based on
- [quickswitch for i3](https://github.com/proxypoke/quickswitch-for-i3) by @slowpoketail

## License
Code licensed under MIT License.
