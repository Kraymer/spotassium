#! /usr/bin/python
from Foundation import *  # NOQA


def is_playing():
    """Return True if spotify player is currently playing.
    """
    apple_script_code = """
    set currentState to getCurrentPlayerState()
    displayTrackName(currentState)
    return currentState

    on getCurrentPlayerState()
        tell application "Spotify"
            set currentState to player state as string
            return currentState
        end tell
    end getCurrentPlayerState

    on displayTrackName(trackName)
        display notification trackName

        delay 1

    end displayTrackName
    """

    s = NSAppleScript.alloc().initWithSource_(apple_script_code)
    player_state = s.executeAndReturnError_(None)[0].stringValue()
    return player_state == 'playing'
