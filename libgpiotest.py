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
print(f"Found gpiochip(s): ")
for i in chips:
    print(i)

done = False
for chip_path in chips:
    try:
        print(f'Accessing chip {chip_path}')
        chip = gpiod.Chip(chip_path)
    except Exception as e:
        try:
            chip.close()
        except Exception:
            pass
        print(f'Failed to access chip {chip_path} Moving on to the next chip.')
        chip = None
        continue
    try:
        info = chip.get_info()
        if info.num_lines < 1:
            print(f'No line associated with chip {chip_path} available. Moving on to the next chip.')
            continue
        print(f'Chip {chip_path} successfully accessed. Info: ')
        print(f'    Name: {info.name}')
        print(f'    Label: {info.label}')
        print(f'    Number of lines: {info.num_lines}')
        print(f'\n--- Start of the tests to chip {chip_path} ---\n')
        line_done = False
        for offset in range(info.num_lines):
            try:
                line_info = chip.get_line_info(offset)
                print(f'Testing line {offset:3d}. Info: ')
                print(f'    Name: {line_info.name!r}')
                print(f'    Used: {line_info.used}')
                print(f'    Consumer: {line_info.consumer!r}')
                print(f'    Direction: {line_info.direction}')
                print(f'    Bias: {line_info.bias}')
                print(f'    Drive: {line_info.drive}')
                print(f'    Edge: {line_info.edge_detection}')
                print('--- Start of the request for line as output ---')
                cfg = {offset: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}
                with gpiod.request_lines(chip_path, consumer="gpiod_v2_test_out", config=cfg) as req:
                    print(f"Successfully requested line {offset} as OUTPUT")
                    req.set_value(offset, Value.ACTIVE)
                    v1 = req.get_value(offset)
                    print(f"The returned value after inputting 1: {v1}")
                    req.set_value(offset, Value.INACTIVE)
                    v0 = req.get_value(offset)
                    print(f"The returned value after inputting 0: {v0}")
            except Exception as e:
                print(f'Exception occured while testing line {offset}: {e} Moving on to the next line.')
        if line_done:
            print(f'\n--- End of the tests to chip {chip_path} ---\n')
            done = True
            break
        else:
            print('No tests to any line succeeded. Moving on to the next chip.')
            continue
    except Exception as e:
        print(f'Exception occured while testing chip {chip_path}: {e} Moving on to the next chip.')
if not chip:
    fail('No chip available.')
if done:
    print("\n=== End of libgpiod v2 functionality test ===")
else:
    fail('\n=== libgpiod v2 functionality test failed. ===')