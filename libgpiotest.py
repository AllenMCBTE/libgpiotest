import glob
import gpiod

def fail(msg):
    print(f"[FAIL] {msg}")
    exit(1)

print("========== libgpiod test started ==========\n")

chips = sorted(glob.glob("/dev/gpiochip*"))
if not chips:
    fail("No /dev/gpiochip* devices found. The kernel may not support GPIO chardev, or libgpiod may not be installed correctly.")
print(f"Found gpiochips: ")
for i in chips:
    print("    -", i)

for chip_path in chips:
    print(f"\n--- Opening {chip_path} ---")
    try:
        chip = gpiod.Chip(chip_path)
    except Exception as e:
        print(f"Failed to open {chip_path}: {e}")
        continue

    info = chip.get_info()
    print(f"    Chip name: {info.name}")
    print(f"    Chip label: {info.label}")
    print(f"    Chip line number: {info.num_lines}")

    if info.num_lines < 1:
        print("    No line to access, skipping.")
        continue

    print("\n--- LineInfo ---")
    for offset in range(info.num_lines):
        try:
            li = chip.get_line_info(offset)
        except Exception as e:
            print(f"Failed to get the info of {offset}: {e}")
            continue
        print(f"Line {offset:3d}:")
        print(f"    Name: {li.name}")
        print(f"    Used: {li.used}")
        print(f"    Consumer: {li.consumer}")
        print(f"    Direction: {li.direction}")
        print(f"    Active_low  : {li.active_low}")
        print(f"    Bias        : {li.bias}")
        print(f"    Drive       : {li.drive}")
        print(f"    Edge        : {li.edge_detection}")
        print(f"    Event_clock : {li.event_clock}")
    
    print("--- End of LineInfo ---")
    print("\n--- Trying to request line as output ---")
    
    config = gpiod.LineSettings()
    config.direction = gpiod.line.Direction.OUTPUT
    config.drive = gpiod.line.Drive.PUSH_PULL