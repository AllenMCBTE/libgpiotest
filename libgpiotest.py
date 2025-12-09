import glob
import time
import sys

import gpiod
from gpiod.line import Direction, Value

def fail(msg):
    print("[FAIL]", msg)
    exit(1)

print("=== libgpiod v2 functionality test ===\n")
chips = sorted(glob.glob("/dev/gpiochip*"))
if not chips:
    fail("No /dev/gpiochip* devices found. The kernel may not support GPIO chardev, or libgpiod may not be installed correctly.")
print(f"Found gpiochips: ")
for i in chips:
    print(i)

for chip_path in chips:
    try:
        print(f'Accessing chip {chip_path}')
        chip = gpiod.Chip(chip_path)
        info = chip.get_info()
        if info.num_lines < 1:
            print(f'No line associated with chip {chip_path} available. Moving on to the next chip.')
            chip = None
            continue
        break
    except Exception as e:
        try:
            chip.close()
        except Exception:
            pass
        print(f'Failed to access chip {chip_path} Moving on to the next chip.')
        chip = None
if not chip:
    fail('No chip available.')

print(f'Chip {chip_path} successfully accessed. Info: ')
print(f'    Name: {info.name}')
print(f'    Label: {info.label}')
print(f'    Number of lines: {info.num_lines}')

