"""
This script generates a csv file with messy patient claims data, it will generate ~200,000 rows
"""

import csv
import random
import uuid
from datetime import datetime, timedelta

random.seed(42) # For reproducibility

# ---------------
# Reference Data
# ---------------
FIRST_NAMES = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Barbara",
    "David","Elizabeth","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen",
    "Christopher","Lisa","Daniel","Nancy","Matthew","Betty","Anthony","Margaret","Mark","Sandra",
    "Donald","Ashley","Steven","Dorothy","Paul","Kimberly","Andrew","Emily","Joshua","Donna",
    "Kenneth","Michelle","Kevin","Carol","Brian","Amanda","George","Melissa","Timothy","Deborah"]

LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts"]

DIAGNOSES = {
    "E11.9":  "Type 2 diabetes mellitus without complications",
    "I10":    "Essential (primary) hypertension",
    "J18.9":  "Pneumonia, unspecified organism",
    "M54.5":  "Low back pain",
    "F32.9":  "Major depressive disorder, single episode, unspecified",
    "K21.0":  "Gastro-esophageal reflux disease with esophagitis",
    "Z23":    "Encounter for immunization",
    "N39.0":  "Urinary tract infection, site not specified",
    "J06.9":  "Acute upper respiratory infection, unspecified",
    "E78.5":  "Hyperlipidemia, unspecified",
}

PROCEDURE_CODES = ["99213","99214","99215","99232","99233","93000","71046","80053","36415","99385",
                   "99386","99396","90837","90834","97110","97530","99281","99283","43239","45378"]

PROVIDERS = [f"PRV{str(i).zfill(5)}" for i in range(1, 201)]
FACILITIES = [f"FAC{str(i).zfill(4)}" for i in range(1, 51)]
INSURERS = ["RedShield","Artera","HealthMedic","Filo","Holistica","Medicaid","Medicare","Tricare"]
STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
          "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
          "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
          "VA","WA","WV","WI","WY"]

# -----------------
# Helper Functions
# -----------------
def random_date(start_year=2020, end_year=2024):
    """Creates and returns dates."""
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def fmt_date(dt, style=0):
    """Returns different date formats."""
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%Y%m%d"]
    return dt.strftime(formats[style % len(formats)])

def messy_phone():
    """Creates and returns random messy phone data."""
    n = f"{random.randint(200,999)}{random.randint(100,999)}{random.randint(1000,9999)}"
    style = random.randint(0, 4)
    if style == 0: return f"({n[:3]}) {n[3:6]}-{n[6:]}"
    if style == 1: return f"{n[:3]}-{n[3:6]}-{n[6:]}"
    if style == 2: return f"{n[:3]}.{n[3:6]}.{n[6:]}"
    if style == 3: return n
    return f"+1{n}"

def messy_gender():
    """Creates and returns random messy gender data."""
    opts = ["M","F","Male","Female","male","female","m","f","MALE","FEMALE","1","2","Unknown",""]
    return random.choice(opts)

def dirty_name(name):
    """Takes a name and returns it with a changed format."""
    r = random.random()
    if r < 0.05:  return name.upper()
    if r < 0.10:  return name.lower()
    if r < 0.12:  return ""
    if r < 0.14:  return name + " " + random.choice(["Jr.", "Sr.", "II", "III"])
    return name

def maybe_null(val, pct=0.03):
    return "" if random.random() < pct else val

def dirty_amount(amount):
    """Takes an amount and returns amount with a changed data type."""
    r = random.random()
    if r < 0.02:  return f"${amount:.2f}"   # dollar sign
    if r < 0.04:  return f"{amount:.0f}"    # no decimal
    if r < 0.045: return str(-abs(amount))  # negative
    return f"{amount:.2f}"

diag_codes = list(DIAGNOSES.keys())


with open("patient_claims.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "claim_id","patient_id","first_name","last_name","date_of_birth",
        "gender","phone","state","insurer","provider_id","facility_id",
        "service_date","diagnosis_code","procedure_code","claim_amount",
        "paid_amount","claim_status","created_at"
    ])

    date_style_cycle = 0
    for i in range(1, 200001):
        dob         = random_date(1940, 2005)
        svc_date    = random_date(2020, 2024)
        created     = svc_date + timedelta(days=random.randint(1, 60))
        diag        = random.choice(diag_codes)
        claim_amt   = round(random.uniform(50, 15000), 2)
        paid_pct    = random.uniform(0.0, 1.05)
        paid_amt    = round(claim_amt * paid_pct, 2)
        status_opts = ["Approved","Denied","Pending","approved","APPROVED","denied","DENIED","Pend","paid","Paid"]
        status      = random.choice(status_opts)

        # Rotating date formats across rows for inconsistency
        ds = date_style_cycle % 5
        date_style_cycle += 1

        writer.writerow([
            str(uuid.uuid4()),
            f"PAT{str(random.randint(1, 150000)).zfill(6)}",
            dirty_name(random.choice(FIRST_NAMES)),
            maybe_null(dirty_name(random.choice(LAST_NAMES)), 0.01),
            fmt_date(dob, ds),
            messy_gender(),
            maybe_null(messy_phone(), 0.05),
            maybe_null(random.choice(STATES), 0.02),
            maybe_null(random.choice(INSURERS), 0.02),
            random.choice(PROVIDERS),
            maybe_null(random.choice(FACILITIES), 0.03),
            fmt_date(svc_date, (ds + 2) % 5),
            maybe_null(diag, 0.04),
            maybe_null(random.choice(PROCEDURE_CODES), 0.04),
            dirty_amount(claim_amt),
            maybe_null(dirty_amount(paid_amt), 0.05),
            status,
            fmt_date(created, 0)
        ])


print("Finished processing patient_claims.csv, 200,000 rows created.")
