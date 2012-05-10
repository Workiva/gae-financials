CLOUD_API_KEY = ""


# we import this to provide support for local settings in the app
try:
    import settingslocal
except ImportError:
    settingslocal = None

if settingslocal:
    for setting in dir(settingslocal):
        globals()[setting.upper()] = getattr(settingslocal, setting)
