# Data Architecture & Generation
To simulate a production environment, I used Python to generate messy source files and SQL scripts for the legacy database.

### Source System: Legacy SQL Database
* **Table:** `Legacy_Source_Data`
* **Challenge:** Contains `VARCHAR(MAX)` notes that must be truncated to fit into a `VARCHAR(50)` reporting field.

### Source System: Clinic Exports (Excel)
* **File:** `Clinic_Appointments.xlsx`
* **Challenge:** Mixed data types in the "Room Number" column and inconsistent State naming (e.g., 'California' vs 'CA').

### Source System: Lab Results (CSV)
* **File:** `Lab_Results.csv`
* **Challenge:** Date format is `YYYY/DD/MM` (requires SSIS Expression/Conversion) and fees include currency symbols (requires string manipulation).

## Setup Instructions
1.  **Database:** Execute the SQL scripts in `/SQL_Setup/` to create the Target and Legacy databases.
2.  **Data Generation:** Run the Python script `generate_data.py` to create the local CSV and Excel source files.
3.  **SSIS:** Open the Visual Studio solution and update the Connection Managers to point to your local file paths.
