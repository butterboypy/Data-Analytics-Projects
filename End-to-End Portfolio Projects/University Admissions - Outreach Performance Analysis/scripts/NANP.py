# import pandas as pd
# import re

# input_file = 'NANP_Area_Codes_Corrected.xlsx' 
# output_file = 'Cleaned_Area_Codes.xlsx'

# def extract_codes(text):
#     # Standardizing regex to find exactly 3-digit sequences
#     return re.findall(r'\b\d{3}\b', str(text))

# try:
#     # 1. Process United States
#     df_usa = pd.read_excel(input_file, sheet_name="United States")
#     usa_labels = df_usa.iloc[:, 0]
#     usa_text = df_usa.iloc[:, 1:].fillna('').astype(str).agg(' '.join, axis=1)
#     usa_codes = pd.DataFrame(usa_text.apply(extract_codes).tolist())
#     usa_codes.columns = [f'Code_{i+1}' for i in range(usa_codes.shape[1])]
#     final_usa = pd.concat([usa_labels, usa_codes], axis=1)

#     # 2. Process Canada
#     df_can = pd.read_excel(input_file, sheet_name="Canada")
#     can_labels = df_can.iloc[:, 0]
#     can_text = df_can.iloc[:, 1:].fillna('').astype(str).agg(' '.join, axis=1)
#     can_codes = pd.DataFrame(can_text.apply(extract_codes).tolist())
#     can_codes.columns = [f'Code_{i+1}' for i in range(can_codes.shape[1])]
#     final_can = pd.concat([can_labels, can_codes], axis=1)

#     # 3. Carribbean & Bermuda
#     df_cb = pd.read_excel(input_file, sheet_name = "Caribbean & Bermuda")
#     split_codes = df_cb['Codes'].str.split(',', expand=True)
#     split_codes = split_codes.apply(lambda x: x.str.strip())
#     split_codes.columns = [f'Code_{i+1}' for i in range(split_codes.shape[1])]
#     final_cb = pd.concat([df_cb['Nation / Territory'], split_codes], axis=1)

#     # 4. Save both to the SAME file using ExcelWriter
#     with pd.ExcelWriter(output_file) as writer:
#         final_usa.to_excel(writer, sheet_name ="United States", index=False)
#         final_can.to_excel(writer, sheet_name ="Canada", index=False)
#         final_cb.to_excel(writer, sheet_name="Caribbean & Bermuda", index=False)

#     print(f"Done! Both sheets saved to: {output_file}")

# except Exception as e:
#     print(f"An error occurred: {e}")


########################## NANP LOOKUP ##########################

import pandas as pd

# File configuration
lookup_file = 'Cleaned_Area_Codes.xlsx'
main_file = 'AOC.xlsx'  # Update if your file name is different
output_file = 'AOC_Updated_Leads.xlsx'

try:
    # 1. Build the Area Code Search Map
    print("Building area code mapping...")
    xls_lookup = pd.ExcelFile(lookup_file)
    area_code_map = {}

    for sheet in xls_lookup.sheet_names:
        df_sheet = pd.read_excel(xls_lookup, sheet_name=sheet)
        
        # We look at all columns except the first one (which contains the names)
        # We flatten all 'Code' columns into a single list to scan every cell
        for col in df_sheet.columns[1:]:
            for val in df_sheet[col].dropna():
                try:
                    # Clean the value: convert to float -> int -> string
                    # This removes decimals like '.0' often seen in Excel imports
                    code_str = str(int(float(val))).strip()
                    area_code_map[code_str] = sheet
                except (ValueError, TypeError):
                    continue # Skip non-numeric data

    # 2. Load the main data file
    print("Loading main data file...")
    # Loading the 'Main' sheet as seen in your screenshot
    df_main = pd.read_excel(main_file, sheet_name='Main')

    # 3. Define the Filling Logic
    def fill_fix_country(row):
        # A. Check if 'Fix Country' is empty/NaN
        current_val = str(row['Fix Country']).strip()
        if pd.isna(row['Fix Country']) or current_val == "" or current_val.lower() == "nan":
            
            # B. Clean and check the Phone_Number
            phone = str(row['Phone_Number']).strip()
            
            # C. Check if it starts with '1' and has enough digits for an area code
            if phone.startswith('1') and len(phone) >= 4:
                # Extract the 3 digits after the '1'
                extracted_code = phone[1:4]
                
                # D. Match against our Map and return the Sheet Name if found
                return area_code_map.get(extracted_code, row['Fix Country'])
        
        # If already filled or no match found, keep the original value
        return row['Fix Country']

    # 4. Apply the logic across the entire table
    print("Processing phone numbers and filling blanks...")
    df_main['Fix Country'] = df_main.apply(fill_fix_country, axis=1)

    # 5. Save the final result
    df_main.to_excel(output_file, index=False)
    print(f"Assignment Complete! File saved as: {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
