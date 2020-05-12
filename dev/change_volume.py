import osascript

#applescript.run("set volume output volume 0")
code, out, err = osascript.run("output volume of (get volume settings)")
print(out)