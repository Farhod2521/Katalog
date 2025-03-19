import requests
import pandas as pd

# Step 1: Fetch the data from the API
url = 'https://backend-market.tmsiti.uz/bojxona/list/'
response = requests.get(url)
data = response.json()  # Assuming the API returns a JSON response

# Step 2: Parse the data to extract relevant fields
records = []
for item in data:
    gtd_info = item.get('gtdInformation', {})
    declaration_data = gtd_info.get('declarationData', {})
    date = declaration_data.get('date')
    g15 = declaration_data.get('g15')
    id_field = declaration_data.get('id')  # Extract the "id"
    
    for product in declaration_data.get('tovar', []):
        record = {
            'ID': id_field,  # Add the "id" field
            'Date': date,
            'G15': g15,
            'Unit': product.get('unit'),
            'Code Name': product.get('codeName'),
            'Additional Unit': product.get('additionalUnit'),
            'Code Tiftn': product.get('codeTiftn'),
            'Value': product.get('value'),
            'G31 Name': product.get('g31name'),
            'Net Mass': product.get('netMass')
        }
        records.append(record)

# Step 3: Convert the data to a DataFrame
df = pd.DataFrame(records)

# Step 4: Save the data to an Excel file
excel_filename = 'bojxona_data_with_id.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Data has been saved to {excel_filename}')
