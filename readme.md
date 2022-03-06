# ⌨️  i3 Keyboard Switcher
Allow to switch keyboard layout using 'most recent' rule.

## Install

Install dependencies
```
pip3 install fire==0.4.0
```


Link executable file
```
sudo ln -s "$(pwd)/i3_keyboard_switcher.py" /usr/bin/
```


Update i3 config

```
# Set up keyboard layout
exec i3_keyboard_switcher.py set_layout_list us ua ru
bindsym $mod+space exec i3_keyboard_switcher.py next_layout
bindsym Control+$mod+1 exec i3_keyboard_switcher.py set_layout_by_order 0
bindsym Control+$mod+2 exec i3_keyboard_switcher.py set_layout_by_order 1
bindsym Control+$mod+3 exec i3_keyboard_switcher.py set_layout_by_order 2

bar {
    status_command i3status | i3_keyboard_switcher.py i3_status
}
```


Update i3status config
```
general {
    output_format = i3bar
}
```


