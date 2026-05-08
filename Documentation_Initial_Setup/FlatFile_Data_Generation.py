import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setting seed for reproducibility
np.random.seed(42)

# 1. Creating CSV File: Lab_Results.csv
# Logic: The messy data has currency symbols in strings and non-standard date formats
lab_data = {
    'Lab_Report_ID': [f'LAB-{i:04d}' for i in range(1, 11)],
    'Patient_Name': [
        'Johnathon Christopher-Smith III', # Long name for truncation
        'Jane Doe',
        'Bob Brown',
        'Alice Montgomery-Smythe',
        'Charlie Day',
        'Diana Prince',
        'Edward Nigma',
        'Fiona Gallagher',
        'George Bluth',
        'Hannah Baker'
    ],
    'Test_Date': [
        '2024/31/01', '2024/15/02', '2024/28/02', '2024/10/03', '2024/22/03',
        '2024/05/04', '2024/19/04', '2024/01/05', '2024/12/05', '2024/25/05'
    ], # YYYY/DD/MM format to test date conversion logic
    'Lab_Fee': [
        '$150.00', '$200.50', '$99.99', '$350.00', '$125.75',
        '$500.00', '$75.25', '$210.00', '$180.00', '$300.40'
    ] # String with '$' to test derived column/data conversion
}
df_csv = pd.DataFrame(lab_data)
df_csv.to_csv('Lab_Results.csv', index=False)

# 2. Creating Excel File: Clinic_Appointments.xlsx
# Logic: Mixed data types in State column and numeric columns
excel_data = {
    'Appointment_ID': np.arange(5001, 5011),
    'Patient_ID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'Clinic_State': [
        'California', 'TX', 'New York', 'FL', 'Washington',
        'CA', 'Texas', 'NY', 'Florida', 'WA'
    ], # Mixed full name and codes to test CASE logic/Lookups
    'Room_Number': [101, 102, 'Room 103', 104, '105B', 106, 107, 'Suite A', 109, 110], # Mixed types to trigger import errors
    'CheckIn_Time': [datetime.now() - timedelta(days=x) for x in range(10)]
}
df_excel = pd.DataFrame(excel_data)
df_excel.to_excel('Clinic_Appointments.xlsx', index=False, sheet_name='Visits')

