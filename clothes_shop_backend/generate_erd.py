# generate_erd.py
from eralchemy import render_er

# هنا حط الـ URI الخاص بالـ SQL Server بتاعك
db_uri = (
    "mssql+pyodbc://@3MoElJo\\SQLEXPRESS/ClothesShopDB"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

# يولد ملف ERD بصيغة PNG
render_er(db_uri, "erd_from_models.png")

print("ERD generated successfully as erd_from_models.png")
