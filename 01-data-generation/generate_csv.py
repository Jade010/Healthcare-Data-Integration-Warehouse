"""
Generates patient_claims.csv with 200,000 rows of messy claims data.
"""
import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42)  # For reproducibility

# ----------------
# Reference Data
# ----------------
FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
               "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
               "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
               "Steven", "Dorothy", "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna",
               "Kenneth", "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
               "Timothy", "Deborah"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
              "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
              "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
              "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
              "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
              "Carter", "Roberts"]

DIAGNOSIS_CODES = ["E11.9", "I10", "J18.9", "M54.5", "F32.9","K21.0", "Z23", "N39.0", "J06.9", "E78.5"]

PROCEDURE_CODES = ["99213", "99214", "99215", "99232", "99233", "93000", "71046", "80053", "36415",
                   "99385", "99386", "99396", "90837", "90834", "97110", "97530", "99281", "99283",
                   "43239", "45378"]

PROVIDERS  = [f"PRV{str(i).zfill(5)}" for i in range(1, 201)]
FACILITIES = [f"FAC{str(i).zfill(4)}" for i in range(1, 51)]
INSURERS = ["RedShield", "Artera", "HealthMedic", "Filo", "Holistica", "Medicaid", "Medicare", "Tricare"]
STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
          "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
          "VA", "WA", "WV", "WI", "WY"]

# ------------------
# Helper Functions
# ------------------
def rand_date(start_year, end_year):
    """Returns a random date between Jan 1 of start_year and Dec 31 of end_year."""
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def fmt_date(dt, style):
    """Formats a date in one of five mixed styles to simulate inconsistent source systems."""
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%Y%m%d"]
    return dt.strftime(formats[style % len(formats)])

def messy_phone():
    """Returns a phone number in one of five formats: (xxx) xxx-xxxx, xxx-xxx-xxxx,
    xxx.xxx.xxxx, plain digits, or with a +1 country code prefix."""
    n = f"{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    return random.choice([
        f"({n[:3]}) {n[3:6]}-{n[6:]}",
        f"{n[:3]}-{n[3:6]}-{n[6:]}",
        f"{n[:3]}.{n[3:6]}.{n[6:]}",
        n,
        f"+1{n}"
    ])

def messy_gender():
    """Returns gender in mixed formats (M/F/Male/Female/1/2/blank etc.)."""
    return random.choice(["M", "F", "Male", "Female", "male", "female",
                           "m", "f", "MALE", "FEMALE", "1", "2", "Unknown", ""])

def dirty_name(name):
    """Returns a name with occasional casing issues, blanks, or suffixes appended."""
    r = random.random()
    if r < 0.05: return name.upper()
    if r < 0.10: return name.lower()
    if r < 0.12: return ""
    if r < 0.14: return name + " " + random.choice(["Jr.", "Sr.", "II", "III"])
    return name

def maybe_null(val, pct=0.03):
    """Returns blank instead of the value pct% of the time to simulate missing data."""
    return "" if random.random() < pct else val

def dirty_amount(amount):
    """Returns a dollar amount with occasional formatting issues: dollar sign prefix,
    no decimal, or a negative value."""
    r = random.random()
    if r < 0.02:  return f"${amount:.2f}"
    if r < 0.04:  return f"{amount:.0f}"
    if r < 0.045: return str(-abs(amount))
    return f"{amount:.2f}"

# --------------
# Generate CSV
# --------------
with open("patient_claims.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "claim_id", "patient_id", "first_name", "last_name", "date_of_birth",
        "gender", "phone", "state", "insurer", "provider_id", "facility_id",
        "service_date", "diagnosis_code", "procedure_code", "claim_amount",
        "paid_amount", "claim_status", "created_at"
    ])

    for i in range(200000):
        svc_date  = rand_date(2020, 2024)
        claim_amt = round(random.uniform(50, 15000), 2)
        paid_amt = round(claim_amt * random.uniform(0.0, 1.05), 2)
        ds = i % 5 # cycles through 5 date formats across rows

        writer.writerow([
            str(uuid.uuid4()),
            f"PAT{str(random.randint(1, 150000)).zfill(6)}",
            dirty_name(random.choice(FIRST_NAMES)),
            maybe_null(dirty_name(random.choice(LAST_NAMES)), 0.01),
            fmt_date(rand_date(1940, 2005), ds),
            messy_gender(),
            maybe_null(messy_phone(), 0.05),
            maybe_null(random.choice(STATES), 0.02),
            maybe_null(random.choice(INSURERS), 0.02),
            random.choice(PROVIDERS),
            maybe_null(random.choice(FACILITIES), 0.03),
            fmt_date(svc_date, (ds + 2) % 5),
            maybe_null(random.choice(DIAGNOSIS_CODES), 0.04),
            maybe_null(random.choice(PROCEDURE_CODES), 0.04),
            dirty_amount(claim_amt),
            maybe_null(dirty_amount(paid_amt), 0.05),
            random.choice(["Approved", "Denied", "Pending", "approved", "APPROVED",
                           "denied", "DENIED", "Pend", "paid", "Paid"]),
            fmt_date(svc_date + timedelta(days=random.randint(1, 60)), 0)
        ])

print("Processing finished,patient_claims.csv created with 200,000 rows.")
