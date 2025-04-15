import os
import json
from extractor import extract_text_from_pdf
from gpt_parser import extract_data_with_gpt
from reconciler import save_to_excel

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processing: {filepath}")
            text = extract_text_from_pdf(filepath)
            gpt_json = extract_data_with_gpt(text)
            try:
                parsed = json.loads(gpt_json)
                save_to_excel(parsed)
            except json.JSONDecodeError as e:
                print(f"JSON parse error for {filename}: {e}\nRaw response:\n{gpt_json}")

if __name__ == "__main__":
    process_folder("documents/purchase_orders")
    process_folder("documents/invoices")
    print("Done.")
