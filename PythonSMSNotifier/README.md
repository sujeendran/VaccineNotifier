# Python SMS Notifier

## SETUP

1. Make necessary changes in the `CoWINNotifier.py` file to add the following:

    - Twilio Account details
    - SMS_INTERVAL can be adjusted if you don't want frequent SMS to be sent. CAUTION: Use carefully as you might miss updates if set too long.
    - Location details to search vaccine availability. For searching by state and district use below links to get STATE_ID and DISTRICT_ID
        - Use https://cdn-api.co-vin.in/api/v2/admin/location/states to get list of states and their IDs
        - Use https://cdn-api.co-vin.in/api/v2/admin/location/districts/<STATE_ID>  to get list of districts and their IDs

2. Make necessary changes in `vaccinenotifier.vbs` file to point to correct directory.

3. In windows, open Task Scheduler and click on Create Task.

    - Provide Name and Description.
    - Select option `Run whether user is logged on or not`. Disable `Do not store password`. This ensures the script runs without user interaction required.
    - In trigger tab, add a new schedule as per the frequency you wish to check.
    - In actions tab, add a `Start a program` entry pointing to the path of `vaccinenotifier.vbs`.
    - In condition tab, enable the condition `Start only if the following network connection is available`->`Any connection`. This ensures the script runs only if internet is available.
    - In settings tab, enable `Allow task to be run on demand`.

4. Double click on the task once to start the automatic routine.

5. You can find a notifier_log.txt file updated with the last check details.

6. If everything is set right you will receive SMS in your registered number.