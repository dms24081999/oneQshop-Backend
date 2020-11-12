import os, sys
import pandas as pd

categoriesDf = pd.DataFrame(columns=["id", "name", "short_name"])
productImagesDf = pd.DataFrame(columns=["id", "image", "main_image"])
productsDf = pd.DataFrame(
    columns=["barcode", "name", "short_name", "categories", "images"]
)

# py run.py "F:\Projects\BE Project\data\style dataset (do not delete)"
path = sys.argv[1]

print()
category_id = 1
product_id = 1
for folder in os.listdir(path):
    if os.path.isdir(os.path.join(path, folder)):
        print(folder)
        categoriesDf = categoriesDf.append(
            {"id": category_id, "name": folder, "short_name": folder}, ignore_index=True
        )
        for file in os.listdir(os.path.join(path, folder)):
            print(file)
            productImagesDf = productImagesDf.append(
                {"id": product_id, "image": file, "main_image": True}, ignore_index=True
            )
            no_ext = os.path.splitext(file)[0]
            productsDf = productsDf.append(
                {
                    "barcode": product_id,
                    "name": no_ext,
                    "short_name": no_ext,
                    "categories": category_id,
                    "images": product_id,
                },
                ignore_index=True,
            )
            product_id = product_id + 1
        category_id = category_id + 1

print(categoriesDf)
print(productImagesDf)
print(productsDf)

categoriesDf.to_csv("categoriesDf.csv", index=False)
productImagesDf.to_csv("productImagesDf.csv", index=False)
productsDf.to_csv("productsDf.csv", index=False)
