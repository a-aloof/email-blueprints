import streamlit as st
import pandas as pd
from docx import Document
import io
import re

st.title("🧴 Shopify Product Uploader from Word")
st.markdown("Upload a `.docx` product catalog file and download the CSV ready for Shopify.")

uploaded_file = st.file_uploader("Upload Word (.docx) file", type="docx")

def clean_price(text):
    return re.sub(r"[^\d.]", "", text)

def extract_products(doc):
    products = []
    current = {}
    fields = [
        "Name of the Product", "Product Name", "Brand Name", "Price", "Size",
        "Description", "Ingredient List", "Customer Results", "Helps With / Indication", 
        "Key Ingredient", "Key Ingredients", "How to Use", "Combos", "Recommended Combos"
    ]

    field_set = set(fields)

    def is_new_product_start(line):
        return line.strip().lower().startswith("bioderma") and "product" not in line.lower()

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    i = 0
    while i < len(paragraphs):
        line = paragraphs[i]

        if is_new_product_start(line):
            if current:
                products.append(current)
            current = {"Title": line}

        elif any(line.startswith(f + ":") for f in fields):
            for field in fields:
                if line.startswith(field + ":"):
                    content = line.split(":", 1)[-1].strip()
                    i += 1
                    while i < len(paragraphs) and not any(paragraphs[i].startswith(f + ":") or is_new_product_start(paragraphs[i]) for f in fields):
                        content += "\n" + paragraphs[i]
                        i += 1
                    i -= 1
                    key = field.replace(" / ", "_").replace(" ", "_").replace("-", "_")
                    current[key] = content
                    break
        i += 1

    if current:
        products.append(current)
    return products

if uploaded_file:
    doc = Document(uploaded_file)
    products = extract_products(doc)

    if not products:
        st.warning("No products found. Please check the format.")
    else:
        df = pd.DataFrame(products)
        df["Price"] = df["Price"].apply(clean_price)

        st.dataframe(df)

        # CSV download
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_buffer.getvalue(),
            file_name="bioderma_products.csv",
            mime="text/csv"
        )
