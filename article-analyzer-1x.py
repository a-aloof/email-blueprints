import streamlit as st
import re
import pandas as pd

# --- Helper Functions ---
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def count_words(text):
    # QuillBot-style: split on spaces but exclude markdown symbols and punctuation
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_characters(text):
    return len(text)

def count_sentences(text):
    sentences = re.findall(r'[^.!?]+[.!?]', text)
    return len(sentences)

def count_paragraphs(text):
    return len([p for p in text.split("\n") if p.strip()])

def keyword_analysis(text, keywords):
    word_list = re.findall(r'\b\w+\b', text.lower())
    total_words = len(word_list)
    keyword_counts = {}
    for kw in keywords:
        kw_clean = kw.lower().strip()
        count = word_list.count(kw_clean)
        keyword_counts[kw] = {
            "count": count,
            "density": round((count / total_words) * 100, 2) if total_words > 0 else 0
        }
    return keyword_counts, total_words

def estimate_read_time(word_count):
    avg_read_speed = 200  # words per minute
    return round(word_count / avg_read_speed, 2)

# --- Streamlit UI ---
st.title("📊 Article Analyzer")

article = st.text_area("Paste your Article here", height=400)

keywords_input = st.text_input("Enter keywords (comma-separated)", "Supply Chain, Material Handling, Inventory")

if st.button("Analyze"):
    if not article.strip():
        st.warning("Please paste an article first.")
    else:
        cleaned_text = clean_text(article)
        word_count = count_words(cleaned_text)
        char_count = count_characters(cleaned_text)
        sentence_count = count_sentences(cleaned_text)
        paragraph_count = count_paragraphs(article)

        keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
        keyword_data, total_words = keyword_analysis(cleaned_text, keywords)

        total_keyword_density = round(sum(k['density'] for k in keyword_data.values()), 2)
        read_time = estimate_read_time(word_count)

        # --- Display Results ---
        st.header("📈 Article Stats")
        st.write(f"**Word Count:** {word_count}")
        st.write(f"**Character Count:** {char_count}")
        st.write(f"**Sentence Count:** {sentence_count}")
        st.write(f"**Paragraph Count:** {paragraph_count}")
        st.write(f"**Estimated Read Time:** {read_time} min")
        st.write(f"**Total Keyword Density:** {total_keyword_density}%")

        st.header("🔍 Keyword Analysis")
        df = pd.DataFrame([
            {"Keyword": kw, "Count": data['count'], "Density (%)": data['density']}
            for kw, data in keyword_data.items()
        ])
        st.dataframe(df)

        st.subheader("📊 Keyword Frequency Chart")
        chart_data = pd.DataFrame({
            'Keyword': [kw for kw in keyword_data],
            'Frequency': [keyword_data[kw]['count'] for kw in keyword_data]
        })
        chart_data = chart_data.set_index("Keyword")
        st.bar_chart(chart_data)
