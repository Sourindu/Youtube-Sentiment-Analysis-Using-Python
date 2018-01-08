import webbrowser

def openURL(videoID):
    try:
        url = 'https://www.youtube.com/watch?v='+videoID

        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        webbrowser.get(chrome_path).open(url)
        
        return True
    
    except SomeError as e:
        return False
    

openURL('9IezBgi7S0I')
