# Tasks.org Appium Automation

Mobile UI automation framework for the Tasks.org Android app.

The framework is built around pytest, Appium, the Screen Object pattern, explicit
waits, environment-based configuration, and failure artifacts suitable for local
debugging and CI execution.

## Tech Stack

- Python 3.11+
- pytest
- Appium Python Client
- Appium UiAutomator2 driver
- Android Emulator
- pytest-html

## Project Structure

```text
mobile_automation/   Framework configuration, driver factory, waits, artifacts
screens/             Screen Object classes for Tasks.org UI flows
tests/               pytest test scenarios
apps/                Local APK storage, not committed
artifacts/           Runtime screenshots/logs, not committed
```

## Setup

1. Install Android Studio and Android SDK.

2. Add Android tools to your shell:

   ```bash
   export ANDROID_HOME="$HOME/Library/Android/sdk"
   export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
   ```

3. Install Appium and UiAutomator2:

   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```

4. Create and activate a Python virtual environment:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

5. Download the pinned Tasks.org APK from F-Droid and save it locally, for example:

   ```text
   apps/tasks-org-15.9.apk
   ```

   Current pinned APK:

   - Source: F-Droid
   - Version: `15.9`
   - Version code: `150902`
   - Package: `org.tasks`
   - Launch activity: `com.todoroo.astrid.activity.TaskListActivity`
   - Local filename: `apps/tasks-org-15.9.apk`
   - SHA-256: `8ecaaca526f42ce2f08f95abfd15381a23a8d57863a5e86fd680d757d4a9f9c9`

   Do not commit APK files.

6. Configure environment variables:

   ```bash
   export TASKS_APK_PATH="$PWD/apps/tasks-org-15.9.apk"
   export APPIUM_SERVER_URL="http://127.0.0.1:4723"
   export ANDROID_DEVICE_NAME="Android Emulator"
   export APP_PACKAGE="org.tasks"
   export APP_ACTIVITY="com.todoroo.astrid.activity.TaskListActivity"
   export NO_RESET=false
   export AUTO_GRANT_PERMISSIONS=true
   ```

7. Start an Android emulator and Appium server:

   ```bash
   emulator -list-avds
   emulator -avd <your-avd-name>
   bash scripts/start_appium.sh
   ```

You can also run the local environment check:

```bash
bash scripts/check_environment.sh
```

## Running Tests

Run the smoke suite:

```bash
bash scripts/run_android_tests.sh -m smoke
```

The Android helper script sets local defaults and validates that the APK,
Appium server, and Android emulator/device are available before pytest starts.

Run CRUD scenarios:

```bash
bash scripts/run_android_tests.sh -m crud
```

If your shell already exports all required variables, pytest can be invoked
directly:

```bash
pytest -m smoke
```

Generate an HTML report:

```bash
pytest -m smoke --html=reports/smoke.html --self-contained-html
```

Failure screenshots are saved under `artifacts/screenshots/`.

## Current Coverage

- App launch and main screen readiness
- Initial onboarding/system dialog dismissal helpers
- Task creation smoke path
- Task edit/complete/delete scaffolding

Locator candidates are centralized in screen objects and should be verified
against the pinned APK before promoting scenarios into the regression suite.

## Test Design Principles

- Prefer stable accessibility IDs and resource IDs.
- Avoid coordinate-based taps unless testing a gesture.
- Use explicit waits instead of sleeps.
- Keep test intent readable.
- Put UI mechanics in screen objects, not test bodies.
- Only add retries for known infrastructure flakiness.
- Do not automate scenarios that are better covered by unit/API tests.

## Known Limitations

- The current implementation targets Android.
- Some Tasks.org locators require validation against the pinned APK with Appium
  Inspector before the full regression suite is finalized.
- CI execution with Android Emulator is planned after local device execution is
  stable.
