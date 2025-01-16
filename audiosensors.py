import sys          # System manipulation
import time         # Used to pause execution in threads as needed
import keyboard     # Register keyboard events (keypresses)
import threading    # Threads for parallel execution
import pyaudio      # Audio streams
import numpy as np  # Matrix/list manipulation
import audioop      # Getting volume from sound data

# GUI dependencies
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import * 

# Constants for streams, modify with care!
CHUNK = 1024*4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

print("Available audio devices:")
# Check the input devices
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
p.terminate()

def log_sound(index, label):
    global buffer       
    
    # Open stream
    stream = p.open(
        format = FORMAT,           # Format of stream data
        channels = CHANNELS,       # Number of input channels
        rate = RATE,               # Frequency of audio
        input = True,              # Stream reads data
        frames_per_buffer = CHUNK, # Number of inout frames for each buffer
        input_device_index = index # Input device
    )

    while True:
        # Read a chunk of data from the stream
        data = stream.read(CHUNK)
        
        # Calculate the volume from the "chunk" of data
        volume = audioop.rms(data, 2)
        
        # Append the necessary data to the buffer
        buffer[index].append(volume)
        
        # change 3: Calculate and display individual statistics
        if len(buffer[index]) > 0:
            mean_value = np.mean(buffer[index])
            var_value = np.var(buffer[index])
            #update our display
            label.setText(f"Sensor {index}: Volume = {volume}    Mean = {mean_value:.2f}    Var = {var_value:.2f}")
        
        # Check for quit command
        if keyboard.is_pressed('q') or quit_flag:
            print("Closing stream", index)
            stream.stop_stream()
            stream.close()
            break
            
def exitMethod():
    global quit_flag
    quit_flag = True
    
def mainThread(mean_label, var_label):
    global buffer
    # change 3: Increased buffer width to store 100 values
    buffer_width = 100
    
    while True:
        # Check the exit condition and join the threads if it is met
        if keyboard.is_pressed('q') or quit_flag:
            for x in threads:
                x.join()
            p.terminate()
            break
            
        # Limit buffers to the buffer_width
        for i in range(len(buffer)):
            buffer[i] = buffer[i][-buffer_width:]  

#########################################################################
#################### TODO: Implement your code there ####################
            
        #change 2: Calculate combined mean and variance over all sound sources
        if len(buffer) > 0:  # Make sure we have at least one buffer
            # Combine all buffers into a single list
            all_values = []
            for buf in buffer:
                if len(buf) > 0:  # To make sure the buffer has values
                    all_values.extend(buf)
            
            if len(all_values) > 0:  # Making sure we have values to calculate
                # change 2: Calculate mean and variance using numpy
                combined_mean = np.mean(all_values)
                combined_variance = np.var(all_values)
                
                # change 2: Update the labels with formatted values
                # change 3: Add individual sensor statistics to the display
                stats_text = f"Combined Mean: {combined_mean:.2f}    "  #guifixesfortask3: Added extra spaces
                for i, buf in enumerate(buffer):
                    if len(buf) > 0:
                        sensor_mean = np.mean(buf)
                        #sensor_var = np.var(buf)
                        # stats_text += f"   Sensor {i}: Mean = {sensor_mean:.2f}, Var = {sensor_var:.2f}    "  # #guifixesfortask3: Added spacing between sensor stats
                        #change 4 Detect if sensor is faulty by comparing with combined mean
                        # Collect faulty sensors
                faulty_sensors = []
                for i, buf in enumerate(buffer):
                    if len(buf) > 0:
                        sensor_mean = np.mean(buf)
                        sensor_variance = np.var(buf)
                        if sensor_mean < combined_mean * 0.55:  # Threshold at 10% of combined mean
                            faulty_sensors.append(i)
                
                # Print faulty sensors if any found
                if faulty_sensors:
                    print(f"\rFaulty sensors detected: {faulty_sensors} -faulty or maybe  muted. Combined mean: {combined_mean:.2f}", end="")
                        
                mean_label.setText(stats_text)
                var_label.setText(f"Combined Variance: {combined_variance:.2f}    ")  # #guifixesfortask3: Added extra spaces
            else:
                mean_label.setText("Mean: No data")
                var_label.setText("Variance: No data")

    print("Execution finished")

# Store threads and labels
threads = []
labels = []
buffer = []
quit_flag = False

# GUI
app = QApplication(sys.argv)
app.aboutToQuit.connect(exitMethod)

# Initializing window
window = QWidget()
window.setWindowTitle('Soundwave log')
window.setGeometry(50, 50, 800, 800)  # #guifixesfortask3: Increased window height to accommodate more statistics
window.move(500, 500)

# Initialize pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

# Run the threads
for i in range(0, numdevices):
    # Check if the device takes input
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        # Initialize labels
        labels.append(QLabel("____________", parent = window))
        labels[-1].setMinimumWidth(800)  # #guifixesfortask3: Increased width to show all sensor statistics
        # change 3: Adjusted vertical spacing for better readability of stats
        labels[-1].move(20, (35 * (i+1)))  # #guifixesfortask3: Increased vertical spacing between sensors
        labels[-1].setFont(QFont('Arial', 10))
        
        # Append a new buffer to the global list
        buffer.append([])
        
        # Start threads
        threads.append(threading.Thread(target=log_sound, args=(i, labels[i])))
        threads[i].start()

# Calculate base position for statistics labels (just below the last sensor label)
base_position = (35 * (len(labels) + 1))  # #guifixesfortask3: Added dynamic positioning based on number of sensors

# Init. labels for combined data        
mean = QLabel("Mean: 0.00", parent = window)  #change 2: Initialize with 0
mean.setMinimumWidth(500)  # #guifixesfortask3: Increased width to accommodate all sensor statistics
mean.setMinimumHeight(200)  # #guifixesfortask3: Added height to ensure all text is visible
mean.move(20, base_position)  # #guifixesfortask3: Position dynamically based on number of sensors
mean.setFont(QFont('Arial', 12))

variance = QLabel("Variance: 0.00", parent = window)  #change 2: Initialize with 0
variance.setMinimumWidth(300)  # #guifixesfortask3: Set minimum width to prevent text truncation
variance.move(20, base_position + 220)  # #guifixesfortask3: Added extra spacing below mean label
variance.setFont(QFont('Arial', 12))

# Start the main thread
main_thread = threading.Thread(target = mainThread, args=[mean, variance])
main_thread.start()

# Show window
window.show()
# Run GUI-application loop
app.exec_()