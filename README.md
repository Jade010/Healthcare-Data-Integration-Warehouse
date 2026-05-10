# Healthcare Database Developer Poject
***Last updated:** 05/10/2026*

An end-to-end database developer portfolio project that demonstrates my experience with ETL pipeline development, data quality remediation, dimensional data warehouse design, and business intelligence reporting using SQL Server, SSIS, Python, and Power BI.

## Business Problem
A regional health network is consolidating three separate data silos (insurance claims, provider records, and lab results) into a central data warehouse to support a new population health dashboard. Raw data from each source contains significant quality issues and must be cleaned, standardized, and validated before any reporting can occur.

## Architecture Overview

![Architecture Diagram](https://github.com/Jade010/Healthcare-Data-Integration-Warehouse/blob/main/05-documentation/Architecture%20Diagram.png)

## Repository Structure
```
Healthcare-Data-Integration-Warehouse/
│
├── README.md                        ← You are here. Welcome in!
│
├── 01-data-generation/              ← Source data scripts and output files
│   ├── README.md
│   ├── generate_csv.py
│   ├── generate_excel.py
│   ├── create_lab_results.sql
│   ├── patient_claims.csv
│   └── provider.xlsx
│
├── 02-SSIS-ETL/                     ← SSIS packages, staging and warehouse DDL (Not Started)
│   └── README.md
│
├── 03-stored-procedures/            ← All SQL stored procedures and views (Not Started)
│   └── README.md
│
├── 04-powerbi/                      ← Power BI report files and documentation (Not Started)
│   └── README.md
│
├── 05-docs/                         ← Architecture diagrams and data dictionary (Not Started)
│   └── README.md
│
└── 06-other/                        ← Miscellaneous scripts, config, and notes (Not Started)
    └── README.md
```

## Folder Summaries
 
| Folder | Purpose |
|---|---|
| `01-data-generation` | Python and SQL scripts that generate 350,000 total rows of intentionally dirty source data across three systems |
| `02-SSIS-ETL` | SSIS packages that clean and load data through staging into a star schema data warehouse |
| `03-stored-procedures` | Load procedures, audit logging, and reporting views that run on top of the warehouse |
| `04-PowerBI` | Power BI dashboard connecting to the warehouse for health reporting |
| `05-documentation` | Architecture diagrams, data flow diagrams, and a full data dictionary |
| `06-other` | Setup notes, environment config, and any miscellaneous supporting files |
 

## Tech Stack
 
| Tool | Purpose |
|---|---|
| SQL Server (I'm using Developer) | Staging database, data warehouse, stored procedures |
| SSMS | Schema management and query development |
| Visual Studio + SSIS extension | ETL package development |
| Python 3.14 | Source data generation |
| Power BI Desktop | Dashboard and reporting |
| Git + GitHub | Version control and portfolio hosting |

## How to Run the Full Project
 
Follow each folder's README in order:
 
1. **`01-data-generation`** — Generate the three source files
2. **`02-SSIS-ETL`** — Set up the database schemas and run the SSIS packages
3. **`03-stored-procedures`** — Deploy all stored procedures and views
4. **`04-powerbi`** — Open the `.pbix` file and connect to your SQL Server instance
 
 
 
