import adafruit_hid
import board
import pulseio
import adafruit_irremote
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
kbd = Keyboard(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)
# Some of these imports are unneeded, I should trim down these a bit

# For a version check, we annoyingly need to define this version tuple to compare stringed versions
def versiontuple(v):
    return tuple(map(int, (v.split("."))))

IR_PIN = board.IR_RX  # Pin connected to IR receiver.

# Expected pulse, pasted in from previous recording REPL session:
mute = [9084, 4493, 595, 537, 593, 1669, 592, 539, 591, 540, 590, 541, 599, 532, 598, 532, 597, 533, 597, 1666, 594, 536, 594, 1669, 592, 1670, 590, 1672, 598, 1664, 597, 1666, 595, 535, 595, 536, 594, 537, 593, 1669, 591, 1671, 590, 541, 599, 532, 598, 1664, 597, 534, 597, 1666, 595, 1667, 593, 537, 593, 539, 592, 1671, 590, 1672, 598, 532, 598, 1665, 596]
volup = [9086, 4492, 595, 536, 594, 1667, 593, 538, 592, 538, 592, 539, 591, 540, 590, 540, 600, 531, 599, 1664, 597, 533, 597, 1666, 594, 1668, 593, 1670, 591, 1672, 599, 1663, 598, 559, 571, 533, 597, 534, 595, 1667, 593, 1669, 591, 539, 591, 539, 591, 540, 590, 541, 600, 1662, 597, 1665, 596, 561, 569, 535, 595, 1667, 593, 1669, 592, 1670, 590, 1672, 599]
voldown = [9091, 4486, 591, 540, 600, 1662, 599, 532, 598, 533, 597, 534, 596, 535, 595, 535, 595, 536, 594, 1668, 592, 539, 591, 1671, 600, 1663, 598, 1664, 597, 1665, 595, 1667, 593, 537, 593, 1669, 591, 539, 601, 530, 600, 1662, 598, 1664, 597, 534, 596, 535, 595, 536, 594, 536, 593, 1669, 592, 1670, 600, 531, 600, 531, 599, 1663, 597, 1665, 596, 1666, 594]
ff = [9084, 4493, 594, 537, 593, 1669, 592, 539, 592, 539, 591, 540, 590, 541, 599, 531, 599, 532, 598, 1663, 597, 533, 597, 1665, 596, 1666, 594, 1668, 593, 1669, 591, 1671, 590, 541, 599, 1663, 598, 533, 598, 533, 597, 1665, 595, 535, 595, 536, 594, 1668, 593, 538, 592, 539, 591, 1671, 590, 1672, 598, 533, 597, 1665, 596, 1666, 595, 536, 594, 1668, 592]
rw = [9084, 4492, 596, 535, 595, 1667, 594, 537, 593, 538, 592, 539, 591, 539, 591, 540, 590, 541, 590, 1672, 599, 532, 598, 1664, 597, 1665, 596, 1666, 595, 1667, 594, 1668, 592, 538, 593, 538, 592, 1670, 591, 1672, 589, 1673, 598, 532, 598, 533, 597, 1665, 596, 535, 595, 1667, 594, 537, 593, 537, 593, 538, 592, 1670, 591, 1671, 590, 541, 589, 1673, 599]
brightnessup = [9083, 4495, 593, 537, 593, 1670, 591, 540, 591, 540, 590, 567, 563, 568, 572, 559, 571, 560, 571, 1666, 595, 535, 595, 1667, 594, 1669, 592, 1670, 590, 1672, 589, 1673, 598, 533, 597, 533, 597, 534, 596, 1667, 594, 536, 594, 1669, 592, 539, 592, 540, 590, 540, 590, 1672, 599, 1664, 597, 533, 597, 1665, 595, 535, 595, 1668, 593, 1669, 592, 1671, 590]
brightnessdown = [9080, 4494, 593, 537, 593, 1669, 592, 565, 565, 539, 591, 540, 591, 540, 590, 567, 563, 567, 573, 1663, 598, 559, 572, 1664, 597, 1665, 596, 1668, 592, 1668, 593, 1669, 592, 538, 592, 1670, 590, 540, 590, 1672, 599, 532, 598, 1663, 597, 533, 598, 560, 571, 560, 570, 561, 569, 1666, 595, 562, 568, 1668, 593, 564, 567, 1669, 592, 1670, 591, 1671, 590]
scanback = [9080, 4496, 592, 539, 591, 1671, 590, 541, 600, 531, 599, 532, 598, 533, 598, 533, 597, 533, 597, 1666, 595, 536, 595, 1668, 593, 1669, 592, 1670, 591, 1671, 600, 1662, 598, 532, 598, 1664, 597, 1666, 595, 536, 595, 1668, 593, 538, 593, 538, 592, 1670, 601, 530, 600, 531, 599, 532, 599, 1664, 597, 534, 596, 1666, 595, 1668, 594, 537, 593, 1670, 591]
scanforward = [9078, 4498, 600, 531, 599, 1664, 598, 533, 597, 533, 597, 534, 596, 535, 595, 536, 595, 536, 594, 1668, 592, 539, 591, 1670, 591, 1673, 599, 1663, 597, 1665, 596, 1666, 594, 536, 594, 1669, 592, 1670, 591, 1672, 589, 1673, 598, 532, 598, 533, 597, 1665, 596, 535, 595, 536, 594, 536, 593, 537, 593, 538, 592, 1670, 591, 1672, 590, 541, 600, 1663, 598]
playpause = [9081, 4496, 593, 539, 591, 1671, 590, 541, 590, 541, 599, 532, 598, 532, 598, 533, 598, 533, 597, 1664, 597, 534, 596, 1665, 595, 1667, 594, 1668, 593, 1669, 592, 1670, 591, 540, 591, 540, 590, 1671, 601, 530, 598, 1663, 598, 533, 597, 534, 596, 1665, 596, 535, 595, 1667, 594, 537, 594, 1668, 593, 538, 592, 1670, 591, 1671, 590, 541, 589, 1672, 599]
stop = [9086, 4491, 597, 534, 596, 1666, 595, 536, 594, 537, 594, 537, 593, 538, 592, 539, 591, 540, 591, 1671, 590, 541, 600, 1663, 598, 1664, 597, 1664, 597, 1666, 595, 1666, 595, 536, 594, 1668, 593, 1669, 592, 1670, 591, 539, 591, 1671, 590, 540, 590, 1673, 598, 532, 598, 532, 628, 503, 628, 503, 627, 1634, 626, 505, 625, 1637, 624, 506, 624, 1638, 622]
eject = [9081, 4497, 592, 540, 590, 1672, 599, 532, 598, 533, 597, 533, 597, 534, 626, 505, 626, 505, 625, 1638, 623, 507, 623, 1639, 622, 1641, 620, 1642, 619, 1643, 618, 1645, 627, 505, 626, 1637, 624, 507, 623, 508, 622, 509, 622, 509, 621, 510, 620, 1642, 619, 511, 619, 512, 618, 1644, 627, 1635, 626, 1636, 624, 1638, 623, 1639, 622, 510, 621, 1642, 619]

print('IR listener')
# Fuzzy pulse comparison function:
def fuzzy_pulse_compare(pulse1, pulse2, fuzzyness=0.2):
    if len(pulse1) != len(pulse2):
        return False
    for i in range(len(pulse1)):
        threshold = int(pulse1[i] * fuzzyness)
        if abs(pulse1[i] - pulse2[i]) > threshold:
            return False
    return True

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulses.clear()
pulses.resume()
# Loop waiting to receive pulses.
while True:
    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)
    print('reading seen IR...')
    # Got a pulse, now compare.
    if fuzzy_pulse_compare(mute, detected):
        print('Muting')
        consumer_control.send(ConsumerControlCode.MUTE)
    elif fuzzy_pulse_compare(voldown, detected):
        print('Turning volume down')
        consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
    elif fuzzy_pulse_compare(volup, detected):
        print('Turning volume up')
        consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif fuzzy_pulse_compare(ff, detected):
        print('Fast forwarding')
        consumer_control.send(ConsumerControlCode.FAST_FORWARD)
    elif fuzzy_pulse_compare(rw, detected):
        print('Rewinding')
        consumer_control.send(ConsumerControlCode.REWIND)
    elif fuzzy_pulse_compare(brightnessup, detected):
        print('Turning brightness up')
        if versiontuple(adafruit_hid.__version__) >= versiontuple("5.0.1"):
            consumer_control.send(ConsumerControlCode.BRIGHTESS_INCREMENT)
        elif versiontuple(adafruit_hid.__version__) < versiontuple("5.0.1"):
            print('Current adafruit_hid version does not appear to support brightness, ignoring.')
    elif fuzzy_pulse_compare(brightnessdown, detected):
        print('Turning brightness down')
        if versiontuple(adafruit_hid.__version__) >= versiontuple("5.0.1"):
            consumer_control.send(ConsumerControlCode.BRIGHTESS_DECREMENT)
        elif versiontuple(adafruit_hid.__version__) < versiontuple("5.0.1"):
            print('Current adafruit_hid version does not appear to support brightness, ignoring.')
    elif fuzzy_pulse_compare(scanback, detected):
        print('Skipping to previous track')
        consumer_control.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
    elif fuzzy_pulse_compare(scanforward, detected):
        print('Skipping to next track')
        consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
    elif fuzzy_pulse_compare(stop, detected):
        print('Stopping')
        consumer_control.send(ConsumerControlCode.STOP)
    elif fuzzy_pulse_compare(eject, detected):
        print('Opening tray')
        consumer_control.send(ConsumerControlCode.EJECT)
    elif fuzzy_pulse_compare(playpause, detected):
        print('Playing/pausing')
        consumer_control.send(ConsumerControlCode.PLAY_PAUSE)
