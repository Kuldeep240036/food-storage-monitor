# Sensor Data Validation and Repeated Testing

## Data Source

FreshChoice SafeStore uses a software-based sensor simulator rather than physical sensor hardware. The simulator generates temperature, humidity and storage-unit status readings for testing the prototype workflow.

Normal test readings use:
- Temperature: 2.0°C to 8.0°C
- Humidity: 45% to 65%
- Status: NORMAL

Abnormal test readings are deliberately generated outside the normal thresholds to verify detection and alert behaviour.

## Test Method

Testing was performed through the GitHub Actions Sensor Simulator Verification workflow.

Each workflow run verifies both:
1. Normal sensor simulation
2. Abnormal sensor simulation

## Repeated Test Results

| Test Run | Branch | Result | Observation |
|---|---|---|---|
| Test 1 | feature/sensor-data-validation | PASS | Normal and abnormal simulator execution completed successfully |
| Test 2 | feature/sensor-data-validation | PASS | Normal and abnormal simulator execution completed successfully |

## Issues Observed

No sensor-simulator execution failure was observed during these two Iteration 3 validation runs.

GitHub Actions displayed environment warnings concerning runner/action versions. These warnings did not cause the sensor verification job to fail.

## Outcome

The repeated validation confirms that the software sensor simulator can execute normal and abnormal test scenarios successfully and provides repeatable evidence for the Iteration 3 testing requirement.
