"""
Generates provider_directory.xlsx with 50,000 rows of messy data
"""
import random
from datetime import datetime, timedelta
import openpyxl

random.seed(99)  # For reproducibility

# ---------------
# Reference Data
# ---------------
SPECIALTIES = ["Cardiology", "Oncology", "Orthopedics", "Pediatrics", "Neurology",
               "Dermatology", "Psychiatry", "Gastroenterology", "Endocrinology", "Radiology",
               "Emergency Medicine", "Family Medicine", "Internal Medicine", "OB/GYN", "Urology",
               "Pulmonology", "Nephrology", "Rheumatology", "Infectious Disease", "Hematology"]

# Messy version mixed into specialties
SPECIALTY_MESSY = SPECIALTIES + ["cardiology", "CARDIOLOGY", "Cardiologist", "Onco", "ortho", "Peds", "Neuro",
                                 "Derm", "psych", "GI", "Endo", "Rad", "EM", "FM", "IM", "OB", "Uro", "Pulm", "Nephro", "Rheum"]

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
          "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
          "VA", "WA", "WV", "WI", "WY"]

# A few states have specific cities
CITIES_BY_STATE = {
    "CA": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "Fresno"],
    "TX": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"],
    "NY": ["New York", "Buffalo", "Albany", "Rochester", "Syracuse"],
    "FL": ["Miami", "Orlando", "Tampa", "Jacksonville", "Tallahassee"],
    }

DEFAULT_CITIES = ["Springfield", "Franklin", "Clinton", "Georgetown", "Salem",
                  "Madison", "Jefferson", "Lincoln", "Washington", "Arlington"]

HOSPITAL_NAMES = ["General Hospital", "Medical Center", "Regional Medical", "University Hospital",
                  "Community Health", "St. Mary's Hospital", "Memorial Hospital",
                  "Mercy Medical", "Providence Hospital", "Children's Hospital"]

SUFFIXES = ["MD", "DO", "MD, PhD", "DO, MPH", "MD, MBA", "", "PhD", "NP", "PA-C"]

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
               "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy", "Matthew"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
              "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris"]

# ------------------
# Helper Functions
# ------------------

def rand_npi():
    """Generates a random 10-digit NPI number. 2% of rows reuse a duplicate to create data quality issues."""
    return str(random.randint(1000000000, 1999999999))

def rand_ein():
    """Returns an EIN in one of four messy formats: formatted (12-3456789),
    unformatted (123456789), missing, or prefixed with 'EIN:'."""
    r = random.random()
    n = f"{random.randint(10, 99)}{random.randint(1000000, 9999999)}"
    if r < 0.25: return f"{n[:2]}-{n[2:]}" # standard formatted
    if r < 0.50: return n # no hyphen
    if r < 0.55: return "" # missing
    return f"EIN:{n[:2]}-{n[2:]}" # prefixed

def rand_phone():
    """Returns a phone number in one of five formats: (xxx) xxx-xxxx,
    xxx-xxx-xxxx, xxx.xxx.xxxx, plain digits, or blank."""
    n = f"{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    styles = [f"({n[:3]}) {n[3:6]}-{n[6:]}", f"{n[:3]}-{n[3:6]}-{n[6:]}",
              f"{n[:3]}.{n[3:6]}.{n[6:]}", n, ""]
    return random.choice(styles)

def rand_zip():
    """Returns a ZIP code as standard 5-digit, ZIP+4, truncated (4 digits), or blank."""
    z = str(random.randint(10000, 99999))
    r = random.random()
    if r < 0.05: return z + f"-{random.randint(1000, 9999)}" # ZIP+4
    if r < 0.08: return z[:4] # truncated
    if r < 0.10: return "" # missing
    return z

def rand_date(start, end):
    """Returns a random date between start and end as a datetime object."""
    return start + timedelta(days=random.randint(0, (end - start).days))

def fmt_date(dt):
    """Formats a date in one of four mixed formats to simulate inconsistency."""
    return dt.strftime(random.choice(["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y"]))

def rand_accepting():
    """Returns accepting new patients status in messy mixed formats (Yes/No/Y/N/1/0/blank etc.)."""
    return random.choice(["Yes", "No", "yes", "no", "Y", "N", "TRUE", "FALSE",
                           "1", "0", "Accepting", "Not Accepting", "", "Limited"])

def rand_rating():
    """Returns a patient rating as a float (normal), integer, formatted string (x/5.0), or blank."""
    r = random.random()
    if r < 0.05: return ""
    if r < 0.08: return random.randint(1, 5)
    if r < 0.10: return f"{random.uniform(1, 5):.1f}/5.0"
    return round(random.uniform(1.0, 5.0), 1)

def rand_years_exp():
    """Returns years of experience as an integer, a string like '10 years', or blank."""
    r = random.random()
    if r < 0.05: return ""
    if r < 0.08: return f"{random.randint(1, 40)} years"
    return random.randint(1, 40)

# ----------------
# Generate Excel
# ---------------
wb = openpyxl.Workbook()
ws = wb.active

ws.append([
    "provider_id", "npi_number", "first_name", "last_name", "credentials",
    "specialty", "sub_specialty", "facility_name", "address_line1", "city",
    "state", "zip_code", "phone", "fax", "email", "ein_number",
    "license_number", "license_state", "license_expiry", "board_certified",
    "accepting_new_patients", "years_experience", "patient_rating", "languages_spoken",
    "telehealth_available", "last_updated"
])

for i in range(1, 50001):
    state = random.choice(STATES)
    city = random.choice(CITIES_BY_STATE.get(state, DEFAULT_CITIES))
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    npi = rand_npi() if random.random() > 0.02 else "1234567890"  # 2% duplicate NPIs

    ws.append([
        f"PRV{str(i).zfill(5)}",
        npi,
        fn if random.random() > 0.02 else fn.upper(), # occasional ALL CAPS first name
        ln if random.random() > 0.02 else "", # occasional missing last name
        random.choice(SUFFIXES),
        random.choice(SPECIALTY_MESSY),
        random.choice(SPECIALTIES) if random.random() > 0.4 else "",
        random.choice(HOSPITAL_NAMES) if random.random() > 0.1 else "",
        f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Park', 'Lake', 'Hill', 'River'])} St",
        city,
        state,
        rand_zip(),
        rand_phone(),
        rand_phone() if random.random() > 0.3 else "", # fax sometimes missing
        f"{fn.lower()}.{ln.lower()}@{'healthsystem' if random.random() > 0.3 else 'hospital'}.{'com' if random.random() > 0.1 else 'org'}" if random.random() > 0.08 else "",
        rand_ein(),
        f"LIC{random.randint(100000, 999999)}",
        random.choice(STATES) if random.random() > 0.05 else "",
        fmt_date(rand_date(datetime(2024, 1, 1), datetime(2028, 12, 31))),
        random.choice(["Yes", "No", "yes", "no", "Y", "N", "Board Certified", "", "BC", "Not Certified"]),
        rand_accepting(),
        rand_years_exp(),
        rand_rating(),
        random.choice(["English", "English, Spanish", "English, Mandarin", "English, French",
                       "Spanish", "English;Spanish", "Eng/Spa", "English | Spanish", ""]),
        random.choice(["Yes", "No", "Y", "N", ""]),
        fmt_date(rand_date(datetime(2022, 1, 1), datetime(2024, 12, 31)))
    ])

wb.save("provider_directory.xlsx")
print("Processing finished, provider_directory.xlsx created with 50,000 rows.")