import time
import json
import pathway as pw

# Example simulated stream that yields maternal event records
@pw.io.python_connector
def simulated_stream():
    # In a real deployment, replace this with a live API or Kafka stream
    events = [
        {'patient_id': 'p1', 'timestamp': '2025-11-17T00:00:00Z', 'heart_rate': 88, 'bp_systolic': 120, 'bp_diastolic': 78, 'note': 'normal'},
        {'patient_id': 'p2', 'timestamp': '2025-11-17T00:00:10Z', 'heart_rate': 110, 'bp_systolic': 140, 'bp_diastolic': 90, 'note': 'elevated'},
        {'patient_id': 'p3', 'timestamp': '2025-11-17T00:00:20Z', 'heart_rate': 70, 'bp_systolic': 110, 'bp_diastolic': 70, 'note': 'normal'}
    ]
    i = 0
    while True:
        yield events[i % len(events)]
        i += 1
        time.sleep(5)
