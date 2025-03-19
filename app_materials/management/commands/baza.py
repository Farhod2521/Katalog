import pandas as pd
from django.core.management.base import BaseCommand
from app_materials.models import MatVolumes, MatCategories, MatGroups, Materials

class Command(BaseCommand):
    help = 'Excel fayldan bazaga materiallarni yuklash.'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Excel fayl yo‘li.')

    def handle(self, *args, **optQions):
        excel_file_path = optQions['excel_file']
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        S= 0
        # Qatorlarni ko‘rib chiqib, modellarga ma'lumotlarni qo‘shish
        for _, row in df.iterrows():
            # MatVolumes (Бўлим) uchun
            volume, _ = MatVolumes.objects.get_or_create(volume_name=row['Бўлим'])

            # MatCategories (Категория) uchun
            category, _ = MatCategories.objects.get_or_create(
                category_name=row['Категория'],
                category_volume=volume
            )

            # MatGroups (ГУРУХ) uchun
            group, _ = MatGroups.objects.get_or_create(
                group_name=row['ГУРУХ'],
                group_category=category
            )

            # Materials uchun
            material_csr_code = row['Yangi kod']
            material_name = row['Книга 3 материал номи']
            material_measure = row['mensuar']  # O'lchov birligini o'zgartiring, kerakli ma'lumotni qo'shing

            # 'ГОСТ' ustunini tekshirish va qiymatini olish
            if 'ГОСТ' in row and not pd.isna(row['ГОСТ']):
                material_gost = row['ГОСТ']
            else:
                material_gost = None
            if 'mxik_kod' in row and not pd.isna(row['mxik_kod']):
                mxik_soliq = row['mxik_kod']
            else:
                mxik_soliq = None

            material, _ = Materials.objects.get_or_create(
                material_csr_code=material_csr_code,
                defaults={
                    'material_name': material_name,
                    'material_measure': material_measure,
                    'material_group': group,
                    'materil_gost': material_gost,
                    'mxik_soliq': mxik_soliq,
                }
            )
            S+=1
            self.stdout.write(self.style.SUCCESS(f'{S}---{material_name} materiali muvaffaqiyatli yuklandi'))

