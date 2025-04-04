import openpyxl
from app_cmeta.models import CmetaCategory, Cmeta  # Import the necessary models

def yuklash(serverga_hujjat):
    wb = openpyxl.load_workbook(serverga_hujjat)
    sheet = wb.active
    for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
        if i != 1:  # Skip the first row
            print(row)  # Print the row
            # Check if the row has the correct number of columns
            if len(row) >= 4:
                category_id = row[1]  # Assuming the second column is the category ID
                name = row[2]  # Assuming the third column is the name
                code = row[3]  # Assuming the fourth column is the code
                measure = row[4]
           
                
                # Create a new Cmeta instance and save it
                category = CmetaCategory.objects.get(id=category_id)
                Cmeta.objects.create(
                    category=category,
                    name=name,
                    code=code,
                    measure=measure, 
                  
                )
            else:
                print("Incorrect number of data:", row)

# Load the Excel file
yuklash('/home/user/django/sinov.xlsx')
