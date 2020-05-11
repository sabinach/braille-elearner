#from AppKit import NSWorkspace
#activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['Visualizer']
#print activeAppName

import psutil

pythons_psutil = []
for p in psutil.process_iter():
	if p.name() == 'Visualizer':
		print(True)