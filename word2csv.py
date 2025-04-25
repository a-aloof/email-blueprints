import streamlit as st
import pandas as pd
from docx import Document
import io
import re

st.set_page_config(page_title="Shopify Product CSV Generator", layout="wide")
st.title("🛍️ Shopify Product Catalog Generator")
st.write("Upload a Word (.docx) file containing product details and get a clean CSV for Shopify.")

uploaded_file = st.file_uploader("Upload a Word document (.docx)", type="docx")

# Function to extract price numbers
def clean_price(text):
    return re.sub(r"[^\d.]", "", text)

# Main parser function
def extract_products(doc):
    products = []
    current = {}
    fields = [
        "Name of the Product", "Product Name", "Brand Name", "Price", "Size",
        "Description", "Ingredient List", "Customer Results", "Helps With / Indication",
        "Helps With", "Key Ingredient", "Key Ingredients", "How to Use", "Combos", "Recommended Combos"
    ]

    def standardize_field(field):
        return field.lower().replace(" ", "_").replace("-", "_").replace("/", "").strip(":")

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    i = 0
    while i < len(paragraphs):
        line = paragraphs[i]
        matched_field = next((f for f in fields if line.startswith(f + ":")), None)

        if line.lower().startswith("bioderma") and not matched_field:
            if current:
                products.append(current)
                current = {}
            current["title"] = line.strip()

        elif matched_field:
            key = standardize_field(matched_field)
            content = line.split(":", 1)[-1].strip()
            i += 1
            # Append multi-line content
            while i < len(paragraphs):
                next_line = paragraphs[i]
                if next_line.startswith(tuple(f + ":" for f in fields)) or next_line.lower().startswith("bioderma"):
                    break
                content += " " + next_line.strip()
                i += 1
            i -= 1
            current[key] = content

        i += 1

    if current:
        products.append(current)
    return products

# Streamlit interface
if uploaded_file:
    try:
        doc = Document(uploaded_file)
        products = extract_products(doc)

        if not products:
            st.warning("No products found. Please check if the file format is correct.")
        else:
            df = pd.DataFrame(products)
            if 'price' in df.columns:
                df["price"] = df["price"].apply(clean_price)

            st.success(f"{len(products)} products extracted!")
            st.dataframe(df)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_buffer.getvalue(),
                file_name="shopify_products.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error processing file: {e}")
