#!/bin/bash
osascript <<'APPLESCRIPT'
tell application "Finder"
    if (count of windows) is 0 then
        set p to POSIX path of (path to home folder)
    else
        set p to POSIX path of (target of front window as alias)
    end if
end tell
return p
APPLESCRIPT
