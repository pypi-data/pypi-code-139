VARIATIONS = ['CHROME', 'CHROME_CANARY', 'CHROMIUM']
DEFAULT_VARIATION = VARIATIONS[0]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'


LOCATIONS = {
    # macOS
    'Darwin': {
        'CHROME': '/Library/Application Support/Google/Chrome',
        'CHROME_CANARY': '/Library/Application Support/Google/Chrome Canary',
        'CHROMIUM': '/Library/Application Support/Chromium'
    },
    'Windows': {
        'CHROME': '\\Google\\Chrome\\User Data',
        'CHROME_CANARY': '\\Google\\Chrome SxS\\User Data',
        'CHROMIUM': '\\Chromium\\User Data'
    },
    'Linux':{ 
        'CHROME': '/.config/google-chrome',
        'CHROME_CANARY': '/.config/google-chrome-beta',
        'CHROMIUM': '/.config/chromium'
    }
}

ENV_KEY = 'CHROFILE_PROFILE_DIR'