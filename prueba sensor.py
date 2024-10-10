import machine
import utime

# Define pins
TRIG_PIN = 14
ECHO_PIN = 15

# Setup Trig and Echo pins
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def measure_distance():
    # Ensure trigger is low initially
    trig.low()
    utime.sleep_us(2)
    
    # Trigger high for 10 microseconds to send a pulse
    trig.high()
    utime.sleep_us(10)
    trig.low()
    
    # Wait for echo response
    start_time = utime.ticks_us()
    while echo.value() == 0:
        start_time = utime.ticks_us()
    
    # Measure how long the echo signal stays high
    stop_time = utime.ticks_us()
    while echo.value() == 1:
        stop_time = utime.ticks_us()
        
    # Calculate pulse duration
    duration = utime.ticks_diff(stop_time, start_time)
    
    # Calculate distance (in cm)
    distance = (duration * 0.0343) / 2
    
    return distance

def check_signal():
    # Send measurement and handle no response
    try:
        distance = measure_distance()
        if distance > 400:
            print("No signal or object is too far!")
        else:
            print("Distance: {:.2f} cm".format(distance))
    except OSError:
        print("Failed to receive echo signal.")

# Main loop
while True:
    check_signal()
    utime.sleep(1)
