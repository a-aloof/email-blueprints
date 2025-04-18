import streamlit as st
import re
from collections import Counter

def analyze_text(article, keywords):
    # Clean article
    article_clean = article.strip()

    # Count metrics
    word_list = re.findall(r'\b\w+\b', article_clean.lower())
    char_count = len(article_clean)
    word_count = len(word_list)
    sentence_count = len(re.findall(r'[.!?]+', article_clean))
    paragraph_count = len(article_clean.split('\n\n'))

    # Keyword processing
    keyword_counts = Counter(word_list)
    keyword_data = {}
    for kw in keywords:
        kw_lower = kw.lower()
        count = keyword_counts[kw_lower]
        density = (count / word_count) * 100 if word_count else 0
        keyword_data[kw] = {"count": count, "density": round(density, 2)}

    return word_count, char_count, sentence_count, paragraph_count, keyword_data


# Streamlit UI
st.title("📝 Article Analyzer")

article = st.text_area("Paste your article here", height=300)
keywords_input = st.text_input("Enter keywords (comma-separated)")

if st.button("Analyze"):
    if article and keywords_input:
        keywords = [k.strip() for k in keywords_input.split(",")]
        word_count, char_count, sentence_count, paragraph_count, keyword_data = analyze_text(article, keywords)

        st.subheader("📊 Text Analysis")
        st.write(f"**Word Count:** {word_count}")
        st.write(f"**Character Count:** {char_count}")
        st.write(f"**Sentence Count:** {sentence_count}")
        st.write(f"**Paragraph Count:** {paragraph_count}")

        st.subheader("🔍 Keyword Analysis")
        for kw, data in keyword_data.items():
            st.write(f"**{kw}** — Occurrences: {data['count']}, Density: {data['density']}%")
    else:
        st.warning("Please paste the article and enter at least one keyword.")
