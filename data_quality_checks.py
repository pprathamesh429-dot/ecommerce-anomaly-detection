from pathlib import Path
import pandas as pd
import numpy as np



BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = DATA_DIR / "raw_business_data.csv"



print()
print("=" * 70)
print("REVENUE LEAKAGE PROJECT")
print("STEP 2: DATA QUALITY CHECKS")
print("=" * 70)

print()
print("Loading raw business data...")

if not INPUT_FILE.exists():
    print()
    print("ERROR: Raw business data file not found.")
    print(f"Expected location:")
    print(INPUT_FILE)
    print()
    print("Run the data generator first.")
    raise SystemExit

data = pd.read_csv(INPUT_FILE)

print(f"Rows loaded    : {len(data):,}")
print(f"Columns loaded : {len(data.columns)}")




print()
print("-" * 70)
print("1. BASIC DATA INFORMATION")
print("-" * 70)

print()
print("Columns:")
for column in data.columns:
    print(f" - {column}")

print()
print("Data types:")
print(data.dtypes)


# ------------------------------------------------------------
# 4. MISSING VALUE CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("2. MISSING VALUE CHECK")
print("-" * 70)

missing = data.isnull().sum()

missing_table = pd.DataFrame({
    "column": missing.index,
    "missing_count": missing.values
})

missing_table["missing_pct"] = (
    missing_table["missing_count"] / len(data) * 100
).round(2)

print(missing_table.to_string(index=False))


# ------------------------------------------------------------
# 5. DUPLICATE CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("3. DUPLICATE CHECK")
print("-" * 70)

duplicate_count = data.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")


# ------------------------------------------------------------
# 6. NUMERIC DATA CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("4. NUMERIC DATA CHECK")
print("-" * 70)

numeric_columns = data.select_dtypes(include=np.number).columns

print()
print("Numeric columns:")

for column in numeric_columns:
    print(f" - {column}")


# ------------------------------------------------------------
# 7. NEGATIVE VALUE CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("5. NEGATIVE VALUE CHECK")
print("-" * 70)

negative_results = []

for column in numeric_columns:

    negative_count = (data[column] < 0).sum()

    negative_results.append({
        "column": column,
        "negative_count": int(negative_count)
    })

negative_table = pd.DataFrame(negative_results)

print(negative_table.to_string(index=False))


# ------------------------------------------------------------
# 8. ZERO VALUE CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("6. ZERO VALUE CHECK")
print("-" * 70)

zero_results = []

for column in numeric_columns:

    zero_count = (data[column] == 0).sum()

    zero_results.append({
        "column": column,
        "zero_count": int(zero_count)
    })

zero_table = pd.DataFrame(zero_results)

print(zero_table.to_string(index=False))


# ------------------------------------------------------------
# 9. UNIQUE VALUE CHECK
# ------------------------------------------------------------

print()
print("-" * 70)
print("7. UNIQUE VALUE CHECK")
print("-" * 70)

unique_results = []

for column in data.columns:

    unique_results.append({
        "column": column,
        "unique_values": data[column].nunique()
    })

unique_table = pd.DataFrame(unique_results)

print(unique_table.to_string(index=False))


# ------------------------------------------------------------
# 10. OUTLIER CHECK USING IQR
# ------------------------------------------------------------

print()
print("-" * 70)
print("8. OUTLIER CHECK")
print("-" * 70)

outlier_results = []

for column in numeric_columns:

    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_count = (
        (data[column] < lower_bound) |
        (data[column] > upper_bound)
    ).sum()

    outlier_results.append({
        "column": column,
        "outlier_count": int(outlier_count)
    })

outlier_table = pd.DataFrame(outlier_results)

print(outlier_table.to_string(index=False))


# ------------------------------------------------------------
# 11. DATA QUALITY SUMMARY
# ------------------------------------------------------------

print()
print("-" * 70)
print("9. DATA QUALITY SUMMARY")
print("-" * 70)

total_missing = int(data.isnull().sum().sum())
total_duplicates = int(data.duplicated().sum())

if total_missing == 0:
    missing_status = "PASS"
else:
    missing_status = "WARNING"

if total_duplicates == 0:
    duplicate_status = "PASS"
else:
    duplicate_status = "WARNING"

quality_summary = pd.DataFrame({
    "check": [
        "Row count",
        "Column count",
        "Missing values",
        "Duplicate rows"
    ],
    "value": [
        len(data),
        len(data.columns),
        total_missing,
        total_duplicates
    ],
    "status": [
        "PASS",
        "PASS",
        missing_status,
        duplicate_status
    ]
})

print()
print(quality_summary.to_string(index=False))


# ------------------------------------------------------------
# 12. SAVE QUALITY REPORTS
# ------------------------------------------------------------

print()
print("-" * 70)
print("10. SAVING DATA QUALITY REPORTS")
print("-" * 70)

quality_summary.to_csv(
    OUTPUT_DIR / "data_quality_summary.csv",
    index=False
)

missing_table.to_csv(
    OUTPUT_DIR / "missing_value_report.csv",
    index=False
)

negative_table.to_csv(
    OUTPUT_DIR / "negative_value_report.csv",
    index=False
)

zero_table.to_csv(
    OUTPUT_DIR / "zero_value_report.csv",
    index=False
)

unique_table.to_csv(
    OUTPUT_DIR / "unique_value_report.csv",
    index=False
)

outlier_table.to_csv(
    OUTPUT_DIR / "outlier_report.csv",
    index=False
)


# ------------------------------------------------------------
# 13. FINAL STATUS
# ------------------------------------------------------------

print()
print("=" * 70)
print("DATA QUALITY CHECKS COMPLETED")
print("=" * 70)

print()
print("Reports created:")
print(" - data_quality_summary.csv")
print(" - missing_value_report.csv")
print(" - negative_value_report.csv")
print(" - zero_value_report.csv")
print(" - unique_value_report.csv")
print(" - outlier_report.csv")

print()
print(f"Output folder:")
print(OUTPUT_DIR)

print()
print("=" * 70)