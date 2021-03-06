# Braille E-Learner

## 6.835 Spring 2020 - Final Project

#### Project Description
Braille E-Learner is a tactile, auditory, and visual (optional) multimodal learning system that teaches users Braille through an interactive feedback system. This system enables users to learn Braille by themselves without the need for an actual instructor on the side.

#### Project Deliverables
- Final Submission [[Video](https://youtu.be/giAB9cWnbE4)] [[Slides](https://drive.google.com/open?id=1IzqvfLHKXQMqJVRoK4RHkVPUROoBIYn_3QGYzvxRu4Q)] [[Paper](https://docs.google.com/document/d/1BlizAmOquUHdDrOiF7t4cDnJ6tE9qRDb2JzIRpzzC-I/edit?usp=sharing)]
- Implementation Studio [[Video](https://youtu.be/EX9FyhGWBtQ)] [[Slides](https://drive.google.com/open?id=10L20eaSqH68sFVSpH1MuKFKV7kZv6fpRwQHiFs6iXlM)]
- Prototype Studio [[Video](https://youtu.be/Sj2WTw3c4sc)] [[Slides](https://drive.google.com/open?id=1GFmHU4PHQUvV5RwFjD5UO8hYAmBete4IV2XkY2GFOoQ)]
- Design Studio [[Video](https://youtu.be/wEaPDDkwDiw )] [[Slides](https://drive.google.com/open?id=1tEz1OheHGrnJrmK5jLfY6nWv8qXapQIAwwBbB38WqdY)]

-----------------------------

### Quick Setup (only run if all dependencies installed, hardware set-up, etc.)

#### To activate venv
- ```source venv/bin/activate```

#### To run script
- ```cd src```            
- ```python2.7 main.py```  

#### PERSONAL NOTE (everyone else can ignore):
- Make sure your conda, python, and python3 aliases in ~/.bash_profile are commented out before you activate venv!

-----------------------------

### Folders

#### dev/
- Test scripts used during development (reference code~ not guaranteed to work, not used in final implementation)

#### docs/
- Miscellaneous documentation related to the project

#### img/
- Images used for braille symbol generation

#### json/
- Calibration and symbol generation settings

#### lib/
- Leap motion SDK

#### src/
- Working scripts used in the final implementation

-----------------------------

### File Descriptions

#### Top-level Script (src)     
- ```main.py``` - primary script that integrates all the separate modes together

#### Global calibration (src/modes)    
- ```calibrate_leap.py``` - set the finger minX/maxX boundaries               
- ```calibrate_camera.py``` - save cell/dot boundaries

#### User Modes (src/modes)    
- ```generate_dots.py``` - generate new symbol orders, guide users in setting up peg slate          
- ```learn.py``` - learn mode         
- ```review.py``` - review mode

#### Parameters and Helper functions (src)            
- ```params.py``` - parameters                  
- ```utils.py``` - helper functions

---

# System requirements

## Hardware
- [Peg Slate](https://www.aph.org/product/peg-slate/)
- [Logitech C270 Webcam](https://www.amazon.com/gp/product/B004FHO5Y6)
- [Leap Motion Controller, 2013](https://www.ultraleap.com/product/leap-motion-controller/) (Leap Motion Desktop Python SDK for Mac, Version 2.3.1)
- [MacBook Pro 15-inch, 2018](https://www.apple.com/shop/refurbished/mac/2018-15-inch) (MacOSX Mojave 10.14.6)

## Software
- ```virtualenv venv -p python2.7```
- ```source venv/bin/activate```
- Install package requirements (specified below)

## Package Requirements

#### PyPi Speech Recognition                   
- ```pip install SpeechRecognition```                       

#### Google Cloud Speech API
- ```pip install google-api-python-client```

#### Pygame
- ```pip install pygame```

#### Pocket Sphinx API 
- ```brew install swig git python```                        
- ```pip install pocketsphinx```

#### OpenCV (Version 4.2.0)
- ```pip install opencv-python```                          
- ```pip install opencv-contrib-python```                   
- ```pip install opencv-python-headless```

#### Numpy
- ```pip install numpy``` 

#### Pathlib
- ```pip install pathlib```

#### osascript (AppleScript wrapper)
- ```pip install osascript```

## Optional Packages (used for dev/test)

#### Monitor and control user input devices
- ```pip install pynput```

#### Process and system monitoring
- ```pip install psutil```

#### For faster operations
- ```pip install monotonic```

#### Text-to-speech
- ```pip install pyttsx3```

#### For microphone
- ```brew install portaudio```                
- ```pip install pyaudio```

---

## System Architecture

![System Architecture](https://github.com/sabinach/braille-elearner/blob/master/docs/system_architecture.png)

---

## Example Usage

![Example Usage](https://github.com/sabinach/braille-elearner/blob/master/docs/cover_image.png)

---

## Hardware Setup

![Hardware Setup](https://github.com/sabinach/braille-elearner/blob/master/docs/hardware_setup.png)

