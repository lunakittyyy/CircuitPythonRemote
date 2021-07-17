# Quickly record and print IR pulses for use in other projects
import board
import pulseio
import adafruit_irremote

# Change 'board.IR_RX' to your microcontroller's IR reciever pin. This should work by default on CPX.
pulses = pulseio.PulseIn(board.IR_RX, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
while True:
    pulses.clear()
    pulses.resume()
    print('Waiting for pulse now...')
    pulse = decoder.read_pulses(pulses)
    print('Pulse recieved! Timings are...')
    print(pulse)
