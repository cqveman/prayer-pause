# prayer-pause

prayer-pause is a desktop (mainly Windows) background app that fetches daily prayer times for your current location, shows adhan
reminders before each prayer, and opens a temporary full-screen lock screen during prayer time.


## Features

- Automatically detects your city and country from your public IP.
- Fetches today’s prayer times from [AlAdhan API](https://aladhan.com/prayer-times-api).
- Sends a startup desktop notification.
- Schedules:
    - **Reminder notification** _N_ minutes before each prayer.
    - **Lock screen** for _M_ minutes at prayer time.
- Runs in the system tray with:
    - **Settings** menu to update reminder/lock durations.
    - **Quit** action.
  

## Installation & Setup

### Standalone Executable

1. Download the latest `.exe` from the [Releases](https://github.com/cqveman/prayer-pause/releases) page.
2. Run the `prayer-pause.exe`.
3. You're all set!

You can change the settings via the tray icon.

### Manual Installation

#### 1. Clone the repository
```bash
git clone https://github.com/cqveman/prayer-pause.git
```
```bash
cd prayer-pause
```

#### 2. Activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Install dependencies
``` bash
pip install -r requirements.txt
```

#### 4. Run
``` bash
python prayer_pause\main.py
```


## Configuration

**Config file location**: `%APPDATA%/PrayerPause/config.json`

Use tray menu **Settings**:

- `Notify (minutes)`: Time before prayer to show the adhan reminder.
- `Lock (minutes)`: Lock screen duration at prayer time.

> **Note:** Both values must be greater than `0`.


## Packaging / distribution

The project uses `PyInstaller` for building executables.

Example using the included `.spec` file:

```bash
pyinstaller --clean prayer-pause.spec
```

If you encounter issues with the `.spec` file, you can delete it and run:

```bash
pyinstaller --clean --onefile --windowed --add-data "app.ico;." --hidden-import plyer.platforms.win.notification --icon=app.ico --name prayer-pause ./prayer_pause/main.py
```


## TODOs
- [ ] Offline mode.
- [ ] Auto start on system login (Windows/Linux).


## Troubleshooting

If you encounter unexpected behavior:  

- Verify your system date, time, and timezone.
- Ensure network access to APIs.
- Open **Settings** and re-save to reload the scheduler.
- Delete `config.json`; the app will regenerate it with default values on the next start.
- Ensure saved values are positive integers.

If the issue persists, feel free to open an [issue](https://github.com/cqveman/prayer-pause/issues)

## License

MIT
