import pandas as pd
from sqlalchemy import create_engine

# MySQL ulanish
engine = create_engine('mysql://tmsitiuz:pwd4catalogDB@localhost/tmsitiuz_catalog')

# Faqat kerakli ustunlarni tanlash
query = "SELECT material_csr_code, material_name, material_measure FROM material_resources"

# Ma'lumotlarni olish
df = pd.read_sql(query, engine)

# Excel faylga saqlash
output_file = "material_filtered.xlsx"
df.to_excel(output_file, index=False)

print(f"Ma'lumotlar {output_file} fayliga faqat kerakli ustunlar bilan saqlandi.")
