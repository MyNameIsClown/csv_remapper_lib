import os
import csv
import random
from datetime import datetime, timedelta

# Generate huge CSV for testing
data_dir = "tests/data"
os.makedirs(data_dir, exist_ok=True)
data_path = os.path.join(data_dir, "huge_test.csv")

first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hector']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis']

def generate_test_csv(path, num_records=1000):
    header = [
        'ID', 'FirstName', 'LastName', 
        'Num1', 'Num2', 
        'BaseValue', 'ValueForPct', 
        'Date1', 'Date2', 
        'Time1', 'Time2', 
        'NegativeNum', 'PositiveNum', 
        'DateString'
    ]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        start_date = datetime(2020, 1, 1)
        for i in range(1, num_records + 1):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            num1 = round(random.uniform(-1000, 1000), 2)
            num2 = round(random.uniform(-1000, 1000), 2)
            base = round(random.uniform(1, 1000), 2)
            pct_val = round(random.uniform(0, base), 2)
            date1 = start_date + timedelta(days=random.randint(0, 2000))
            date2 = start_date + timedelta(days=random.randint(0, 2000))
            date1_str = date1.strftime('%Y-%m-%d')
            date2_str = date2.strftime('%Y-%m-%d')
            time1 = (datetime.min + timedelta(seconds=random.randint(0, 24*3600-1))).time().isoformat()
            time2 = (datetime.min + timedelta(seconds=random.randint(0, 24*3600-1))).time().isoformat()
            neg = round(random.uniform(-1000, 1000), 2)
            pos = round(random.uniform(0, 1000), 2)
            date_string = random.choice([
                date1.strftime('%d/%m/%Y'),
                date2.strftime('%B %d, %Y'),
                date1.strftime('%Y-%m-%d')
            ])
            writer.writerow([
                i, fn, ln,
                num1, num2,
                base, pct_val,
                date1_str, date2_str,
                time1, time2,
                neg, pos,
                date_string
            ])

generate_test_csv(data_path, num_records=10000)
