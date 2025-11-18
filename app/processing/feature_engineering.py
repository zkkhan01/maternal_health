import pathway as pw

def compute_trends(table):
    # Example streaming aggregation. Replace with your own logic.
    return table.groupby('patient_id').rolling(window=3, on='timestamp').aggregate({'heart_rate': 'avg'})
