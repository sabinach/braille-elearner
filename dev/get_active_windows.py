from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo

workspace = NSWorkspace.sharedWorkspace()
activeApps = workspace.runningApplications()
for app in activeApps:
    if app.isActive():
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options,
                                                kCGNullWindowID)
        for window in windowList:
            if window['kCGWindowOwnerName'] == app.localizedName():
                print(window.getKeys_)
                break
        break