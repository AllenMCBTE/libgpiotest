import gpiod
import time

chips = gpiod.chip_iter()
chips = list(chips)
if not chips:
    print("No /dev/gpiochip device nodes were found. The kernel may lack GPIO chardev support, or libgpiod may not be properly installed.")
else:
    print(f"Found {len(chips)} GPIO chips:")
    for c in chips:
        print(f"- {c.name} ({c.label})")