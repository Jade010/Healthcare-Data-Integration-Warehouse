-- ============================================================
-- SQL Source Table for raw data
-- Table: dbo.lab_results
-- 100,000 rows of laboratory test results
-- Will contain quality issues
-- ============================================================

-- ============================================================
-- 1. CREATE THE DATABASE
-- ============================================================
DROP DATABASE IF EXISTS HealthcareLegacy;
CREATE DATABASE HealthcareLegacy;

USE HealthcareLegacy;   
GO

-- ============================================================
-- 2. CREATE TABLE
-- ============================================================

-- Dropping table if it exists
DROP TABLE IF EXISTS dbo.lab_results;

CREATE TABLE dbo.lab_results (
    lab_result_id INT NOT NULL PRIMARY KEY,
    patient_id VARCHAR(12) NOT NULL,
    ordering_provider_id VARCHAR(10) NOT NULL,
    test_code VARCHAR(20) NOT NULL,
    test_name VARCHAR(100) NOT NULL,
    result_value VARCHAR(50) NOT NULL, -- Setting as VARCHAR but it stores numbers AND messy strings
    result_unit VARCHAR(30) NULL,
    reference_range VARCHAR(50) NULL,
    result_status VARCHAR(20) NULL,
    collected_date VARCHAR(20) NOT NULL, -- Setting VARCHAR but it is mixed date formats
    resulted_date VARCHAR(20) NULL,
    facility_id VARCHAR(10) NULL,
    critical_flag VARCHAR(10) NULL,
    notes VARCHAR(500) NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO


-- ============================================================
-- 3. TEMP TABLES FOR REFERENCE
-- 
-- This section contains three temp tables based on lab data. I am
-- using some of my Pre-Nursing degree for this project because I love
-- working with health related information. 
--
-- The FIRST TEMP TABLE creates a lab test catalog for every blood/urine 
-- test offered with details on the test. There are 20 different lab tests.
--
-- The SECOND TEMP TABLE is a status list that contains some messy values
-- for the status of a lab result. 
--
-- The THIRD TEMP TABLE is a critical flag that marks whether a lab result
-- is dangerously abnormal that will catch the attention of a doctor. It 
-- essentially contains messy data showing all of the different ways you 
-- could say yes or no.
-- ============================================================

CREATE TABLE #TestCodes (
    test_code VARCHAR(20), test_name VARCHAR(100),
    low_val FLOAT, high_val FLOAT, unit VARCHAR(30), ref_range VARCHAR(50)
);

INSERT INTO #TestCodes VALUES
('CBC-WBC', 'White Blood Cell Count', 2.0, 18.0, 'K/uL', '4.5-11.0 K/uL'),
('CBC-RBC', 'Red Blood Cell Count', 3.0, 6.5, 'M/uL', '4.5-5.5 M/uL'),
('CBC-HGB', 'Hemoglobin', 7.0,  20.0, 'g/dL', '13.5-17.5 g/dL'),
('CBC-PLT', 'Platelet Count', 50.0, 600.0, 'K/uL', '150-400 K/uL'),
('BMP-GLU', 'Glucose', 50.0, 450.0, 'mg/dL', '70-100 mg/dL'),
('BMP-BUN', 'Blood Urea Nitrogen', 5.0, 80.0, 'mg/dL', '7-20 mg/dL'),
('BMP-CRE', 'Creatinine', 0.4, 8.0, 'mg/dL', '0.6-1.2 mg/dL'),
('LFT-ALT', 'Alanine Aminotransferase', 5.0, 300.0, 'U/L', '7-56 U/L'),
('LFT-AST', 'Aspartate Aminotransferase', 5.0, 300.0, 'U/L', '10-40 U/L'),
('LFT-ALB', 'Albumin', 1.5, 5.5, 'g/dL', '3.4-5.4 g/dL'),
('LIP-CHOL', 'Total Cholesterol', 100.0, 350.0, 'mg/dL', '<200 mg/dL'),
('LIP-LDL', 'LDL Cholesterol', 40.0, 250.0, 'mg/dL', '<100 mg/dL'),
('LIP-HDL', 'HDL Cholesterol', 20.0, 120.0, 'mg/dL', '>40 mg/dL'),
('THY-TSH', 'Thyroid Stimulating Hormone', 0.1, 10.0, 'mIU/L', '0.4-4.0 mIU/L'),
('URN-PH', 'Urine pH', 4.5, 8.5, 'pH units', '4.6-8.0'),
('HBA1C', 'Hemoglobin A1c', 4.0, 14.0, '%', '<5.7%'),
('PSA', 'Prostate Specific Antigen', 0.0,  30.0, 'ng/mL', '0-4 ng/mL'),
('INR', 'International Normalized Ratio', 0.5, 5.0, 'ratio', '0.8-1.1'),
('VIT-D', 'Vitamin D, 25-Hydroxy', 5.0, 100.0, 'ng/mL', '30-100 ng/mL'),
('FER', 'Ferritin', 2.0, 500.0, 'ng/mL', '12-300 ng/mL');

-- Status pool (contains messy data)
CREATE TABLE #Statuses (status VARCHAR(20));
INSERT INTO #Statuses VALUES
('Final'),('final'),('FINAL'),('Preliminary'),('preliminary'),('PRELIM'),
('Corrected'),('corrected'),('Cancelled'),('CANCELLED'),('Pending'),('pending'),(''),('Unknown');

-- Critical flag pool (contains messy data)
CREATE TABLE #CritFlags (flag VARCHAR(10));
INSERT INTO #CritFlags VALUES
('Y'),('N'),('Yes'),('No'),('yes'),('no'),('TRUE'),('FALSE'),('1'),('0'),('Critical'),('Normal'),('');

-- ============================================================
-- 4. POPULATE TABLE
--
-- This is where the artificial data will be created to populate
-- the source data for this project. Creating the source data
-- is really a project in itself especially because I am susceptible 
-- to scope creep!

-- This section starts off by declaring temp variables. i is just
-- my counter that will go up to 100,000 since I am needing 100,000
-- rows.
-- ============================================================

DECLARE @i INT = 1;
DECLARE @patient_id VARCHAR(12);
DECLARE @provider_id VARCHAR(10);
DECLARE @facility_id VARCHAR(10);
DECLARE @test_code VARCHAR(20);
DECLARE @test_name VARCHAR(100);
DECLARE @low_val FLOAT;
DECLARE @high_val FLOAT;
DECLARE @unit VARCHAR(30);
DECLARE @ref_range VARCHAR(50);
DECLARE @raw_val FLOAT;
DECLARE @result_val VARCHAR(50);
DECLARE @result_unit VARCHAR(30);
DECLARE @status VARCHAR(20);
DECLARE @crit_flag VARCHAR(10);
DECLARE @coll_date VARCHAR(20);
DECLARE @res_date VARCHAR(20);
DECLARE @date_fmt INT;
DECLARE @rand_offset INT;
DECLARE @base_date DATETIME;
DECLARE @notes_val VARCHAR(500);

-- Looping until there are 100,000 records
WHILE @i <= 100000
BEGIN
    -- Randomly grabbing one test from test code temp table
    SELECT TOP 1
        @test_code  = test_code,
        @test_name  = test_name,
        @low_val    = low_val,
        @high_val   = high_val,
        @unit       = unit,
        @ref_range  = ref_range
    FROM #TestCodes
    ORDER BY NEWID();

    -- Builds fake IDs, facility will purposely contain blanks 5% of the time to add to the messiness of the data
    SET @patient_id  = 'PAT' + RIGHT('000000' + CAST(ABS(CHECKSUM(NEWID())) % 150000 + 1 AS VARCHAR), 6); -- 150,000 represents possible patients
    SET @provider_id = 'PRV' + RIGHT('00000' + CAST(ABS(CHECKSUM(NEWID())) % 200 + 1 AS VARCHAR), 5); -- 200 represents possible doctors
    SET @facility_id = CASE WHEN ABS(CHECKSUM(NEWID())) % 20 = 0 THEN NULL
                            ELSE 'FAC' + RIGHT('0000' + CAST(ABS(CHECKSUM(NEWID())) % 50 + 1 AS VARCHAR), 4) -- 50 represents possible locations
                       END;

    -- Result values with messy entries, calculates random number within test range and creates a messy entry 8% of the time for data isn't all chaotic
    SET @raw_val = @low_val + (CAST(ABS(CHECKSUM(NEWID())) AS FLOAT) / 2147483647.0) * (@high_val - @low_val);
    SET @result_val =
        CASE ABS(CHECKSUM(NEWID())) % 100
            WHEN 0 THEN 'N/A'
            WHEN 1 THEN 'PENDING'
            WHEN 2 THEN 'ERROR'
            WHEN 3 THEN ''
            WHEN 4 THEN '>'  + CAST(CAST(@raw_val AS INT) AS VARCHAR)
            WHEN 5 THEN '<'  + CAST(CAST(@raw_val AS INT) AS VARCHAR)
            WHEN 6 THEN CAST(CAST(@raw_val AS INT) AS VARCHAR) -- no decimal
            WHEN 7 THEN REPLACE(CAST(ROUND(@raw_val,2) AS VARCHAR), '.', ',') -- European decimal
            ELSE CAST(ROUND(@raw_val, 2) AS VARCHAR)
        END;

    -- Unit will also be altered for messy data, sometimes missing, sometimes altered
    SET @result_unit =
        CASE ABS(CHECKSUM(NEWID())) % 15
            WHEN 0 THEN NULL
            WHEN 1 THEN LOWER(@unit)
            WHEN 2 THEN UPPER(@unit)
            ELSE @unit -- normal format
        END;

    -- Randomly grabbing a messy status
    SELECT TOP 1 @status = status FROM #Statuses ORDER BY NEWID();

    -- Randomly grabbing a messy crit flag
    SELECT TOP 1 @crit_flag = flag FROM #CritFlags ORDER BY NEWID();

    -- Dates in mixed formats
    SET @rand_offset = ABS(CHECKSUM(NEWID())) % 1826; -- Picking random date somewhere in the last 5 years
    SET @base_date = DATEADD(DAY, -@rand_offset, '2024-12-31');
    SET @date_fmt = (ABS(CHECKSUM(NEWID())) % 5) + 1;

    SET @coll_date =
        CASE @date_fmt
            WHEN 1 THEN CONVERT(VARCHAR, @base_date, 23) -- YYYY-MM-DD
            WHEN 2 THEN CONVERT(VARCHAR, @base_date, 101) -- MM/DD/YYYY
            WHEN 3 THEN REPLACE(CONVERT(VARCHAR, @base_date, 101),'/','-') -- MM-DD-YYYY
            WHEN 4 THEN REPLACE(CONVERT(VARCHAR, @base_date, 23),'-','') -- YYYYMMDD
            ELSE        CONVERT(VARCHAR, DAY(@base_date)) + '/' +
                        CONVERT(VARCHAR, MONTH(@base_date)) + '/' +
                        CONVERT(VARCHAR, YEAR(@base_date)) -- D/M/YYYY
        END;

    SET @res_date =
        CASE ABS(CHECKSUM(NEWID())) % 20
            WHEN 0 THEN NULL -- missing
            ELSE CONVERT(VARCHAR, DATEADD(HOUR, ABS(CHECKSUM(NEWID())) % 72, @base_date), 23)
        END;

    -- I want 60% of records to have no notes at all. The other 40% will get one of four lab notes
    SET @notes_val =
        CASE ABS(CHECKSUM(NEWID())) % 10
            WHEN 0 THEN 'Patient fasting confirmed'
            WHEN 1 THEN 'Hemolyzed sample - rerun recommended'
            WHEN 2 THEN 'Critical value called to physician'
            WHEN 3 THEN 'QNS - quantity not sufficient'
            ELSE NULL
        END;

    -- Final inserts 
    INSERT INTO dbo.lab_results
        (lab_result_id, patient_id, ordering_provider_id, test_code, test_name,
         result_value, result_unit, reference_range, result_status,
         collected_date, resulted_date, facility_id, critical_flag, notes)
    VALUES
        (@i, @patient_id, @provider_id, @test_code, @test_name,
         @result_val, @result_unit, @ref_range, @status,
         @coll_date, @res_date, @facility_id, @crit_flag, @notes_val);

    SET @i += 1; -- Counter for loop
END;

-- ============================================================
-- 5. SANITY CHECK
--
-- Dropping temp tables now that lab results have been created.
-- My sanity check is just looking to see if 
--      1.) Are there all 100,000 rows
--      2.) How many unique patients are there
--      3.) How many different test types show up 
--      4.) How many results are left blank
--      5.) How many records are missing a unit
--      6.) How many are missing a result date
-- ============================================================

DROP TABLE #TestCodes;
DROP TABLE #Statuses;
DROP TABLE #CritFlags;

-- Sanity check
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT patient_id) AS distinct_patients,
    COUNT(DISTINCT test_code) AS distinct_tests,
    SUM(CASE WHEN result_value = '' THEN 1 ELSE 0 END) AS blank_result_values,
    SUM(CASE WHEN result_unit IS NULL THEN 1 ELSE 0 END) AS null_units,
    SUM(CASE WHEN resulted_date IS NULL THEN 1 ELSE 0 END) AS null_resulted_dates
FROM dbo.lab_results;
GO

-- ===================================================================================
-- 6. END RESULT
--
-- total_rows = There are 100,000 rows as I wanted
-- distinct_patients = There are around 72,952 patients which makes sense since some
-- could be returning patients so they cannot all be unqiue
-- distinct_tests = All 20 tests I created are being represented which is good
-- blank_result_values = There are 1,018 blank results so 1% of the data is blank
-- null_units = There are 6,648 null units so around 6.6% are missing units
-- null_resulted_dates = There are 5,062 blank dates so around 5% are missing
-- ====================================================================================

SELECT * FROM [dbo].[lab_results];