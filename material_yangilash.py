import os
import django

# Django sozlamalarini import qilish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # O'zingizning loyiha nomingizni yozing
django.setup()

import openpyxl
from django.utils import timezone
from app_materials.models import MaterialAds  # O'zingizning app nomini kiritish

# Excel faylini o'qish
def update_material_prices(excel_file):
    # Excel faylini ochish
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):  # 2-qatordan boshlash, 1-qatorda sarlavhalar
        excel_id = row[0]  # Excel faylidan id olish
        excel_price = row[1]  # Excel faylidan material_price olish

        # Baza ma'lumotlarini qidirish
        try:
            material = MaterialAds.objects.get(id=excel_id)

            # ID bilan natijalarni print qilish
            print(f"ID: {excel_id}----------------")

            # Har doim material_updated_date yangilanishi kerak
            material.material_price = excel_price  # Excel faylidan narxni qo'yish
            material.material_updated_date = timezone.now()  # Yangilanish vaqtini qo'shish
            material.save()  # O'zgarishlarni saqlash
            print(f"Material ID {excel_id} ning narxi yangilandi: {excel_price}")

        except MaterialAds.DoesNotExist:
            print(f"Material ID {excel_id} bazada topilmadi.")

# Skriptni ishga tushirish
if __name__ == '__main__':
    # Excel faylini ko'rsating
    excel_file = '/home/user/backend/Katalog/materil_yangi.xlsx'  # Fayl nomi
    update_material_prices(excel_file)
