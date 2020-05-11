from Carbon import AppleEvents 
from Carbon import AE

# Bundle identifiers: osascript -e 'id of app "Name of App"'
iterm_id = "com.googlecode.iterm2"
sublime_id = "com.sublimetext.3"

target = AE.AECreateDesc(AppleEvents.typeApplicationBundleID, sublime_id)
activateEvent  = AE.AECreateAppleEvent( 'misc', 'actv', target, AppleEvents.kAutoGenerateReturnID, AppleEvents.kAnyTransactionID)
activateEvent.AESend(AppleEvents.kAEWaitReply, AppleEvents.kAENormalPriority, AppleEvents.kAEDefaultTimeout)
