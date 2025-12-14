# ClothesShop UML - Python script to generate PlantUML
classes = [
    "Supplier", "Category", "Customer", "Product",
    "Order", "OrderDetail", "Employee",
    "Inventory", "Payment", "Shipper"
]

relations = [
    ("Order", "OrderDetail"),
    ("OrderDetail", "Product"),
    ("Order", "Customer"),
    ("Product", "Category"),
    ("Product", "Supplier"),
    ("Inventory", "Product"),
    ("Payment", "Order"),
]

with open("ClothesShop.puml", "w") as f:
    f.write("@startuml\n")
    for cls in classes:
        f.write(f"class {cls} {{\n}}\n")
    for src, dst in relations:
        f.write(f"{src} --> {dst}\n")
    f.write("@enduml\n")

print("تم توليد ملف ClothesShop.puml")



