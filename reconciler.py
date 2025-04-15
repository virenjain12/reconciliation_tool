import pandas as pd
import os
from rapidfuzz import fuzz

EXCEL_PATH = "output/reconciliation_report.xlsx"

def save_to_excel(parsed_data):
  
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
    else:
        df = pd.DataFrame(columns=[
            "type", "document_number", "vendor", "date",
            "item", "quantity", "unit_price", "total_price",
            "grand_total", "flag"
        ])

    new_rows = []

    for item in parsed_data["items"]:
        row = {
            "type": parsed_data["type"],
            "document_number": parsed_data["document_number"],
            "vendor": parsed_data["vendor"],
            "date": parsed_data["date"],
            "item": item["item"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "total_price": item["total_price"],
            "grand_total": parsed_data["grand_total"],
            "flag": ""
        }


        if parsed_data["type"].strip().lower() == "invoice":
            po_rows = df[
                (df["type"].str.lower() == "purchase order") &
                df["vendor"].apply(lambda v: fuzz.partial_ratio(v.strip().lower(), parsed_data["vendor"].strip().lower()) > 90) &
                df["item"].apply(lambda i: fuzz.partial_ratio(i.strip().lower(), item["item"].strip().lower()) > 90)
            ]

            if po_rows.empty:
                row["flag"] = "No matching PO"
            else:
                po = po_rows.iloc[0]
                try:
                    if float(item["unit_price"]) != float(po["unit_price"]):
                        row["flag"] = f"Price mismatch (PO: {po['unit_price']})"
                    elif int(item["quantity"]) > int(po["quantity"]):
                        row["flag"] = f"Qty > PO (PO: {po['quantity']})"
                except Exception as e:
                    row["flag"] = f"Comparison error: {e}"

        new_rows.append(row)


    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # Drop exact duplicates
    df.drop_duplicates(
    subset=["type", "document_number", "vendor", "date", "item"],
    keep="last",  
    inplace=True)

    df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")
