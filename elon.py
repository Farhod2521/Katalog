import pandas as pd
from django.core.management.base import BaseCommand
from app_materials.models import MaterialAds, Materials
from app_company.models import    Regions, Districts
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
def import_material_ads(file_path):
    # Load Excel data into a DataFrame
    df = pd.read_excel(file_path)
    
    # Print column names for validation
    print("Column names:", df.columns)

    # Iterate through each row in the Excel data
    for _, row in df.iterrows():
        material_code = row.get('id')
        
        # Skip rows without a valid material code
        if pd.isna(material_code):
            print(f"Skipping row with missing 'id': {row}")
            continue

        # Fetch the related Material instance
        try:
            material_name = Materials.objects.get(material_csr_code=material_code)
        except ObjectDoesNotExist:
            print(f"Material matching query does not exist: {material_code}")
            continue

        # Fetch the material owner (user)
        try:
            material_owner = get_user_model().objects.get(id=row['material_owner'])
        except ObjectDoesNotExist:
            print(f"Skipping row with invalid 'material_owner': {row['material_owner']}")
            continue

        # Fetch the region and district if available
        try:
            material_region = Regions.objects.get(id=row['material_region']) if pd.notna(row['material_region']) else None
        except ObjectDoesNotExist:
            print(f"Invalid 'material_region': {row['material_region']}")
            material_region = None

        try:
            material_district = Districts.objects.get(id=row['material_district']) if pd.notna(row['material_district']) else None
        except ObjectDoesNotExist:
            print(f"Invalid 'material_district': {row['material_district']}")
            material_district = None

        # Create MaterialAds entry
        try:
            MaterialAds.objects.create(
                material_name=material_name,
                material_description=row.get('material_description', ''),
                material_price=row.get('material_price', 0),
                material_price_currency=row.get('material_price_currency', 'UZS'),
                material_measure=row.get('material_measure', ''),
                material_image=row.get('material_image', None),
                material_amount=row.get('material_amount', 0),
                material_amount_measure=row.get('material_amount_measure', ''),
                material_status=row.get('material_status', True),
                material_created_date=row.get('material_created_date', pd.NaT),
                material_updated_date=row.get('material_updated_date', pd.NaT),
                material_deactivated_date=row.get('material_deactivated_date', pd.NaT),
                sertificate_blank_num=row.get('sertificate_blank_num', ''),
                sertificate_reestr_num=row.get('sertificate_reestr_num', ''),
                material_owner=material_owner,
                company_name=row.get('company_name', ''),
                company_stir=row.get('company_stir', ''),
                material_region=material_region,
                material_district=material_district,
            )
        except Exception as e:
            print(f"Error importing row with id {material_code}: {e}")

    print("Data import completed.")
