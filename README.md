# fault-detection-audio-sensors
# Audio Sensors Analysis

## Overview
This project implements audio signal analysis from multiple audio sources using Python. The implementation analyzes volume levels, calculates statistical measures, and detects faulty sensors using both static and dynamic approaches.

## Audio Sources Used
- Input Device 0: Microsoft Sound Mapper (Internal Laptop microphone)
- Input Device 1: Microphone Array (Internal Laptop microphone)
- Input Device 2: Microphone (DroidCam Virtual Au) - Intentionally zero
- Input Device 3: Microphone (DroidCam Audio) - Smartphone mic via LAN
- Input Device 4: Headset (JBL TUNE BEAM) - Bluetooth earphone

## Implementation Features

### 1. Volume Display
- Implemented real-time volume display for each sensor
- Enhanced GUI with improved spacing and window sizing
- Added detailed sensor statistics display

### 2. Combined Statistics
- Calculated combined mean and variance across all audio sources
- Implemented unified buffer for multi-source analysis
- Used NumPy for efficient statistical computations

### 3. Individual Sensor Analysis
- Buffer size: 100 samples for each sensor
- Implemented FIFO data structure for sample management
- Calculated individual means and variances
- Real-time statistical updates for each sensor

### 4. Fault Detection
Two approaches implemented:

#### First Approach
- Comparison with combined mean using threshold (0.55)
- Detection of completely silent or malfunctioning sensors
- Tested with physical sensor blocking experiments

#### Second Approach (Experimental)
Classified faults into three categories:
1. Dead: Low mean and variance (broken/off mic)
2. Loose Connection: Low mean, high variance (unstable connection)
3. Frozen: Signal present but no variation (unresponsive)


## Dependencies
- Python 3.x
- PyAudio
- NumPy
- Qt for GUI

## Results
- Successfully detected malfunctioning sensors
- Accurate volume measurements across different sources
- Reliable fault detection with physical sensor tests

## Future Improvements
- Enhanced filtering mechanisms
- Optimized sensor characteristics analysis
- Improved parallelism for synchronized readings
- More robust filtering for noise reduction

## Project Structure
```
project/
│
├── src/
│   ├── audiosensors.py    # Main implementation
│
└── README.md              # Project documentation
```

## Author
Moh'd Abu Quttain

## Running Environment
Code tested and run on VSC within a Python environment.

## Note
This implementation focuses on real-time audio analysis with fault detection capabilities. The code has been tested with multiple audio sources including physical and virtual microphones.
