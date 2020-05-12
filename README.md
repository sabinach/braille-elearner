# Braille E-Learner

### 6.835 Spring 2020 - Final Project

#### NOTE:
Make sure your conda, python, and python3 aliases in ~/.bash_profile are commented out before you activate venv!

#### To activate venv
```source venv/bin/activate```

#### To run script
```cd src```            
```python2.7 main.py```  

#### Global calibration
```cd src/modes```           
```python2.7  calibrate_leap.py``` (finger minX, maxX)                
```python2.7  calibrate_camera.py``` (save cell/dot boundaries) 

#### Mode Scripts
```cd src/modes```     
```python2.7  generate_dots.py```          
```python2.7  learn.py```          
```python2.7  review.py```

#### Parameters and Helper functions
```cd src```                
```vim params.py```                  
```vim utils.py```

---

### Project Checkpoints

#### Design Studio
Video: https://youtu.be/wEaPDDkwDiw       
Slides: https://drive.google.com/open?id=1tEz1OheHGrnJrmK5jLfY6nWv8qXapQIAwwBbB38WqdY

#### Prototype Studio
Video: https://youtu.be/Sj2WTw3c4sc      
Slides: https://drive.google.com/open?id=1GFmHU4PHQUvV5RwFjD5UO8hYAmBete4IV2XkY2GFOoQ      

#### Implementation Studio
Video: https://youtu.be/EX9FyhGWBtQ     
Slides: https://drive.google.com/open?id=10L20eaSqH68sFVSpH1MuKFKV7kZv6fpRwQHiFs6iXlM     

#### Final Report
Video: TBD                           
Slides: TBD                         
Paper: TBD

---

## Venv Set-up

#### To create new venv
```virtualenv venv -p python2.7```

#### To activate venv
```source venv/bin/activate```

#### To deactivate venv
```deactivate```

---

## Package Installations

#### PyPi Speech Recognition                   
```pip install SpeechRecognition```                       
https://pypi.org/project/SpeechRecognition/                             
https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py      

#### For microphone
```brew install portaudio```                
```pip install pyaudio```

#### Google Web Speech API
```pip install google-api-python-client```

#### Pygame
```pip install pygame```

#### Pocket Sphinx API 
```brew install swig git python```                        
```pip install pocketsphinx```

#### For faster operations (optional)
```pip install monotonic```

#### Text-to-speech (optional)
```pip install pyttsx3```

#### OpenCV
```pip install opencv-python```                          
```pip install opencv-contrib-python```                   
```pip install opencv-python-headless```

#### Numpy
```pip install numpy``` 

#### Pathlib
```pip install pathlib```

#### pynput (optional)
```pip install pynput```

#### psutil (optional)
```pip install psutil```

#### applescript (optional)
pip install applescript

#### osascript
pip install osascript



