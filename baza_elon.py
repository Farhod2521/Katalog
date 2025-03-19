import requests
from app_materials.models import MaterialAds, Materials
from django.contrib.auth import get_user_model
from app_company.models import Regions, Districts
# Fetch data from API
response = requests.get('https://catalog1212.pythonanywhere.com/elon-baza/')
data = response.json()

# Process the API response and save the data to the MaterialAds model
for item in data:
    try:
        # Fetch the foreign key objects using the numeric IDs provided by the API
        material_name = Materials.objects.get(pk=item['material_name'])
        material_region = Regions.objects.get(pk=item['material_region']) if item['material_region'] else None
        material_district = Districts.objects.get(pk=item['material_district']) if item['material_district'] else None
        material_owner = get_user_model().objects.get(pk=item['material_owner'])
        
        # Create the MaterialAds entry
        material_ad = MaterialAds.objects.create(
            material_name=material_name,
            material_description=item.get('material_description', ''),
            material_price=float(item['material_price']),
            material_price_currency=item['material_price_currency'],
            material_measure=item['material_measure'],
            material_image=item['material_image'] if item['material_image'] else None,
            material_amount=float(item['material_amount']),
            material_amount_measure=item['material_amount_measure'],
            material_status=bool(item['material_status']),
            sertificate_blank_num=item['sertificate_blank_num'],
            sertificate_reestr_num=item['sertificate_reestr_num'],
            material_owner=material_owner,
            company_name=item.get('company_name'),
            company_stir=item.get('company_stir'),
            material_region=material_region,
            material_district=material_district
        )
        
        print(f"MaterialAd {material_ad.id} created successfully.")
    except Exception as e:
        print(f"Error processing item {item}: {str(e)}")

