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

IR_PIN = board.IR_RX  # Pin connected to IR receiver.

# Expected pulse, pasted in from previous recording REPL session:
mute = [9084, 4493, 595, 537, 593, 1669, 592, 539, 591, 540, 590, 541, 599, 532, 598, 532, 597, 533, 597, 1666, 594, 536, 594, 1669, 592, 1670, 590, 1672, 598, 1664, 597, 1666, 595, 535, 595, 536, 594, 537, 593, 1669, 591, 1671, 590, 541, 599, 532, 598, 1664, 597, 534, 597, 1666, 595, 1667, 593, 537, 593, 539, 592, 1671, 590, 1672, 598, 532, 598, 1665, 596]
volup = [9086, 4492, 595, 536, 594, 1667, 593, 538, 592, 538, 592, 539, 591, 540, 590, 540, 600, 531, 599, 1664, 597, 533, 597, 1666, 594, 1668, 593, 1670, 591, 1672, 599, 1663, 598, 559, 571, 533, 597, 534, 595, 1667, 593, 1669, 591, 539, 591, 539, 591, 540, 590, 541, 600, 1662, 597, 1665, 596, 561, 569, 535, 595, 1667, 593, 1669, 592, 1670, 590, 1672, 599]
voldown = [9091, 4486, 591, 540, 600, 1662, 599, 532, 598, 533, 597, 534, 596, 535, 595, 535, 595, 536, 594, 1668, 592, 539, 591, 1671, 600, 1663, 598, 1664, 597, 1665, 595, 1667, 593, 537, 593, 1669, 591, 539, 601, 530, 600, 1662, 598, 1664, 597, 534, 596, 535, 595, 536, 594, 536, 593, 1669, 592, 1670, 600, 531, 600, 531, 599, 1663, 597, 1665, 596, 1666, 594]

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

