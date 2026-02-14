# EMF Camp Countdown App for Tildagon Badge

A simple countdown app for the Tildagon badge that displays the number of days until the next EMF Camp (July 16-19, 2026 at Eastnor Castle).

## Features

- Displays days remaining until EMF 2026
- Shows the event dates and location
- Color-coded display with EMF-themed colors
- Automatically calculates days based on the badge's system time

## Installation

### Option 1: Testing on your badge (during development)

1. Create a `metadata.json` file in the app directory:
```json
{
  "name": "EMF Countdown",
  "path": "apps.emf_countdown.app"
}
```

2. Install mpremote:
```bash
pip install mpremote
```

3. Connect your badge via USB and copy the app:
```bash
mpremote connect /dev/ttyACM0 mkdir :apps
mpremote connect /dev/ttyACM0 mkdir :apps/emf_countdown
mpremote connect /dev/ttyACM0 cp app.py :apps/emf_countdown/app.py
mpremote connect /dev/ttyACM0 cp metadata.json :apps/emf_countdown/metadata.json
```

4. Restart your badge by holding the reboop button for 2 seconds

### Option 2: Testing with the simulator

1. Clone the Tildagon badge software:
```bash
git clone https://github.com/emfcamp/badge-2024-software.git
cd badge-2024-software
git submodule update --init --recursive
```

2. Install dependencies (Python 3.9 recommended):
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Copy your app to the sim/apps directory:
```bash
mkdir -p sim/apps/emf_countdown
cp /path/to/emf-countdown/app.py sim/apps/emf_countdown/
```

4. Run the simulator:
```bash
python sim/__init__.py
```

### Option 3: Publish to the App Store

To make your app available to all Tildagon users:

1. Create a GitHub repository with your app
2. Ensure you have `app.py` and `tildagon.toml` in the root
3. Remove any `metadata.json` file
4. Follow the publishing guide at: https://tildagon.badge.emfcamp.org/tildagon-apps/publish/

## Controls

- Press the **CANCEL** button to exit the app and return to the badge menu

## How it Works

The app calculates the number of days from the current date (using the badge's system time) to July 16, 2026 (the start date of EMF 2026). The calculation accounts for:
- Different month lengths
- Leap years
- Year transitions

## Customization

You can easily modify the app for future EMF events by changing these variables in `app.py`:

```python
self.emf_year = 2026
self.emf_month = 7
self.emf_day = 16
```

And updating the display text in the `draw()` method.

## Future EMF Events

EMF Camp is held every two years. After EMF 2026, the next event would typically be in 2028. The Tildagon badge is designed to be reusable across multiple EMF events, so this app can be easily updated for future years!

## Resources

- [Tildagon Badge Documentation](https://tildagon.badge.emfcamp.org/)
- [EMF Camp Website](https://www.emfcamp.org/)
- [Tildagon App Directory](https://apps.badge.emfcamp.org/)
- [Badge 2024 Software Repository](https://github.com/emfcamp/badge-2024-software)

## License

MIT License - feel free to modify and share!

## Credits

Built for the EMF Camp community and the Tildagon badge platform.
