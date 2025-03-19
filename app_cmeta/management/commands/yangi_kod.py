import pandas as pd
from django.core.management.base import BaseCommand
from app_cmeta.models import Sample_Project

class Command(BaseCommand):
    help = 'Excel fayldan bazadagi Sample_Project modelini yangilash.'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Excel fayl yo‘li.')

    def handle(self, *args, **options):
        excel_file_path = options['excel_file']
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        updated_count = 0

        # Excel faylidagi har bir qatorni ko‘rib chiqish
        for _, row in df.iterrows():
            eski_kod = row['Эски коди']
            yangi_kod = row['Yangi kod']

            # Sample_Project modelidan eski_kod bilan mos yozuvni topish
            try:
                sample_project = Sample_Project.objects.get(name=eski_kod)
                sample_project.name = yangi_kod
                sample_project.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"{updated_count} - {eski_kod} muvaffaqiyatli {yangi_kod} ga yangilandi"))
            except Sample_Project.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"{eski_kod} kodi bo‘yicha yozuv topilmadi"))

        self.stdout.write(self.style.SUCCESS(f"Jami {updated_count} ta yozuv yangilandi."))

