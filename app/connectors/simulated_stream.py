import time
import pathway as pw
from typing import Optional

class SimulatedSubject(pw.io.python.ConnectorSubject):
    def run(self) -> None:
        events = [
            {'patient_id': 'p1', 'timestamp': '2025-11-17T00:00:00Z', 'heart_rate': 88, 'bp_systolic': 120, 'bp_diastolic': 78, 'note': 'normal'},
            {'patient_id': 'p2', 'timestamp': '2025-11-17T00:00:10Z', 'heart_rate': 110, 'bp_systolic': 140, 'bp_diastolic': 90, 'note': 'elevated'},
            {'patient_id': 'p3', 'timestamp': '2025-11-17T00:00:20Z', 'heart_rate': 70, 'bp_systolic': 110, 'bp_diastolic': 70, 'note': 'normal'}
        ]
        i = 0
        try:
            while True:
                ev = events[i % len(events)]
                # send each field explicitly
                self.next(
                    patient_id=ev['patient_id'],
                    timestamp=ev['timestamp'],
                    heart_rate=ev['heart_rate'],
                    bp_systolic=ev['bp_systolic'],
                    bp_diastolic=ev['bp_diastolic'],
                    note=ev['note']
                )
                i += 1
                time.sleep(5)
        except Exception as e:
            # on error let Pathway know by closing
            self.close()

    def on_stop(self) -> None:
        # Cleanup if necessary
        pass

# Helper function to expose a pw.io.python.read table using this subject
def read_simulated_stream(autocommit_duration_ms: Optional[int] = 1000):
    class InputSchema(pw.Schema):
        patient_id: str = pw.column_definition(primary_key=True)
        timestamp: str
        heart_rate: int
        bp_systolic: int
        bp_diastolic: int
        note: str

    subject = SimulatedSubject()
    table = pw.io.python.read(
        subject,
        schema=InputSchema,
        autocommit_duration_ms=autocommit_duration_ms
    )
    return table
