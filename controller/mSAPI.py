import win32com.client as wincl

# Export text-to-speech engine as a variable
ttsEngine = wincl.Dispatch("SAPI.SpVoice")


def tts(line: str, doPrint: bool = True):
    if doPrint:
        print(line)
    ttsEngine.speak(line)
