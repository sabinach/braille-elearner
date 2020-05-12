# Braille E-Learner

## 6.835 Spring 2020 - Final Project

#### Design Studio
Video: https://youtu.be/wEaPDDkwDiw       
Slides: https://drive.google.com/open?id=1tEz1OheHGrnJrmK5jLfY6nWv8qXapQIAwwBbB38WqdY

#### Prototype Studio
Video: https://youtu.be/Sj2WTw3c4sc      
Slides: https://drive.google.com/open?id=1GFmHU4PHQUvV5RwFjD5UO8hYAmBete4IV2XkY2GFOoQ      

#### Implementation Studio
Video: https://youtu.be/EX9FyhGWBtQ     
Slides: https://drive.google.com/open?id=10L20eaSqH68sFVSpH1MuKFKV7kZv6fpRwQHiFs6iXlM     

#### Final Submission
Video: TBD                           
Slides: https://drive.google.com/open?id=1IzqvfLHKXQMqJVRoK4RHkVPUROoBIYn_3QGYzvxRu4Q                         
Report: https://drive.google.com/open?id=1IALhN5d4B-JnODCCNb1j1C23TWInbQ1WDDUx7BBCy9Y
Github: https://github.com/sabinach/braille-elearner

-----------------------------

### Ready-to-run (all dependencies installed, hardware set-up, etc.)

#### To activate venv
```source venv/bin/activate```

#### To run script
```cd src```            
```python2.7 main.py```  

#### PERSONAL NOTE (everyone else can ignore):
- Make sure your conda, python, and python3 aliases in ~/.bash_profile are commented out before you activate venv!
- Computer: MacOSX (Mojave 10.14.6)

-----------------------------

### Folders

#### dev/
- Test scripts used during development (reference code~ not guaranteed to work, not used in final implementation)

#### img/
- Images used for braille symbol generation

#### json/
- Settings

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
- [Leap Motion Controller](https://www.ultraleap.com/product/leap-motion-controller/) (Leap Motion SDK - Mac 2.3.1)

## Set Up Virtual Environment

1. Create new venv:	```virtualenv venv -p python2.7```
2. Activate venv:	```source venv/bin/activate```
3. Install package requirements (specified below)

## Software Package Requirements

#### PyPi Speech Recognition                   
- ```pip install SpeechRecognition```                       
- https://pypi.org/project/SpeechRecognition/                             
- https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py      

#### For microphone
- ```brew install portaudio```                
- ```pip install pyaudio```

#### Google Web Speech API
- ```pip install google-api-python-client```

#### Pygame
- ```pip install pygame```

#### Pocket Sphinx API 
- ```brew install swig git python```                        
- ```pip install pocketsphinx```

#### OpenCV
- ```pip install opencv-python```                          
- ```pip install opencv-contrib-python```                   
- ```pip install opencv-python-headless```

#### Numpy
- ```pip install numpy``` 

#### Pathlib
- ```pip install pathlib```

#### AppleScript wrapper
- ```pip install osascript```

#### Monitor and control user input devices
- ```pip install pynput```

#### Process and system monitoring
- ```pip install psutil```

#### For faster operations (optional)
- ```pip install monotonic```

#### Text-to-speech (optional)
- ```pip install pyttsx3```

---

## Physical Hardware Set Up

![Physical Hardware Set Up](https://github.com/sabinach/braille-elearner/blob/master/img/physical_setup.png)


