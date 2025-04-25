import streamlit as st
import pandas as pd
from docx import Document
import io
import re

# Set Streamlit page settings
st.set_page_config(page_title="Shopify Catalog Generator ", layout="wide")
st.title("🛍️ Shopify Product Catalog Generator by Random Dude")
st.write("Upload a Word (.docx) file containing product details and get a clean CSV for Shopify.")

# Upload widget
uploaded_file = st.file_uploader("Upload a Word document (.docx)", type="docx")

# --- Helper Functions ---
def clean_price(text):
    """Extract numbers safely from price field."""
    if isinstance(text, str):
        return re.sub(r"[^\d.]", "", text)
    return ""

def extract_products(doc):
    """Extract structured product info from a Word document."""
    products = []
    current = {}
    
    # Define the field labels
    fields = [
        "Name of the Product", "Product Name", "Brand Name", "Price", "Size",
        "Description", "Ingredient List", "Customer Results", "Helps With / Indication",
        "Helps With", "Key Ingredient", "Key Ingredients", "How to Use", "Combos", "Recommended Combos"
    ]

    # Helper to standardize field names
    def standardize_field(field):
        return field.lower().replace(" ", "_").replace("-", "_").replace("/", "").strip(":")
    
    # Read all non-empty paragraphs
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    i = 0
    while i < len(paragraphs):
        line = paragraphs[i]
        matched_field = next((f for f in fields if line.startswith(f + ":")), None)

        # Detect new product start
        if line.lower().startswith("bioderma") and not matched_field:
            if current:
                products.append(current)
                current = {}
            current["title"] = line.strip()

        # Capture fields
        elif matched_field:
            key = standardize_field(matched_field)
            content = line.split(":", 1)[-1].strip()
            i += 1
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

# --- Main App Logic ---
if uploaded_file:
    try:
        doc = Document(uploaded_file)
        products = extract_products(doc)

        if not products:
            st.warning("⚠️ No products found. Please check if the file format is correct.")
        else:
            df = pd.DataFrame(products)
            
            # Safely clean the price field
            if 'price' in df.columns:
                df["price"] = df["price"].apply(lambda x: clean_price(x) if pd.notna(x) else "")

            st.success(f"✅ {len(products)} products extracted successfully!")
            st.dataframe(df)

            # Prepare CSV download
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_buffer.getvalue(),
                file_name="shopify_products.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
