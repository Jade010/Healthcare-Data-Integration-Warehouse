# Healthcare Database Developer Poject
**Last updated:** 05/07/2026

## Project Overview
This repository contains an end-to-end database development project focused on designing and building a data pipeline using SQL Server, SSIS, and Power BI. This scenario involves a healthcare system migrating data from siloed satellite clinics and legacy platforms into a centralized Data Warehouse. My primary objective is to demonstrate my process using ETL processes using SSIS, handling messy data issues such as data conversion, truncation hadling, data standardization, and multi-source integration.

## Business Problem & Requirements
**Scenario:** A regional hospital system is unable to gain a holistic view of patient care because patient records, lab results, and clinic visits are stored in three different formats.

**Project Goals:**
1.  **Consolidate Data:** Integrate a Legacy SQL Server table, an Excel clinic export, and a CSV lab results file.
2.  **Ensure Integrity:** Standardize location codes and validate data types.
3.  **Error Handling:** Implement a "Redirection" logic for rows that fail truncation or conversion tests to ensure the package doesn't crash during production runs.

## 4. Repository Structure
### Stage 1: Documentation & Initial Setup [Current]
* [x] Requirements & Scope
* [x] Data Generation (Python & SQL scripts)
* [x] Target Schema Design (`Hospital_DW`)

### Stage 2: Database Modeling [Not Started]
* Development of the **Staging Area** to land raw data
* Creation of the **Fact and Dimension tables** (Star Schema)
* Implementation of Primary/Foreign Key constraints

### Stage 3: ETL Development (SSIS) [Not Started]
* **Control Flow:** Implementation of Sequence Containers and Execute SQL Tasks
* **Data Flow:** Use of Derived Columns, Data Conversions, and Lookups
* **Error Handling:** Configuring Error Output paths for Truncation and Transformation failures

### Stage 4: Logic & Optimization [Not Started]
* Stored Procedures for Post-Load processing
* Indexing for performance tuning

### Stage 5: BI & Reporting [Not Started]
* Power BI integration via DirectQuery/Import
* DAX measure creation for patient visit metrics
* Interactive Dashboard design.
