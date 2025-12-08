import glob
import gpiod

def fail(msg):
    print(f"[FAIL] {msg}")
    exit(1)

chips = sorted(glob.glob("/dev/gpiochip*"))
if not chips:
    fail("No /dev/gpiochip* devices found. The kernel may not support GPIO chardev, or libgpiod may not be installed correctly.")