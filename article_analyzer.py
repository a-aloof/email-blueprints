 import streamlit as st
import re
import math

# ---------- Text Analysis Functions ----------

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

def count_characters(text):
    return len(text)

def count_sentences(text):
    return len(re.findall(r'[.!?]+', text))

def count_paragraphs(text):
    return len([p for p in text.split('\n') if p.strip()])

def estimate_read_time(text):
    words_per_minute = 200  # Average reading speed
    total_words = count_words(text)
    return math.ceil(total_words / words_per_minute)

def analyze_keywords(text, keywords):
    keyword_stats = []
    word_count = count_words(text)

    total_density = 0.0

    for keyword in keywords:
        pattern = re.escape(keyword.lower())
        matches = re.findall(r'\b' + pattern + r'\b', text.lower())
        count = len(matches)
        density = (count / word_count) * 100 if word_count else 0
        total_density += density

        keyword_stats.append({
            'keyword': keyword,
            'count': count,
            'density': round(density, 2)
        })

    return keyword_stats, round(total_density, 2)

# ---------- Streamlit App Layout ----------

st.set_page_config(page_title="Article Analyzer", layout="centered")

st.title("📊 Article Analyzer")
st.markdown("Analyze your article for structure, read time, and keyword density.")

article = st.text_area("📄 Paste your article here:", height=400)

keywords_input = st.text_area("🔍 Enter keywords (one per line):", height=150)

if st.button("Analyze"):
    if not article.strip():
        st.warning("Please paste an article.")
    else:
        keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]

        # Text metrics
        word_count = count_words(article)
        char_count = count_characters(article)
        sentence_count = count_sentences(article)
        paragraph_count = count_paragraphs(article)
        read_time = estimate_read_time(article)

        # Keyword stats
        keyword_stats, total_density = analyze_keywords(article, keywords)

        # ---------- Results ----------

        st.subheader("📈 Text Analysis")
        st.write(f"**Word Count:** {word_count}")
        st.write(f"**Character Count:** {char_count}")
        st.write(f"**Sentence Count:** {sentence_count}")
        st.write(f"**Paragraph Count:** {paragraph_count}")
        st.write(f"**Estimated Read Time:** {read_time} minute(s)")

        st.subheader("🔎 Keyword Analysis")
        if keyword_stats:
            for stat in keyword_stats:
                st.markdown(f"**{stat['keyword']}** — Occurrences: {stat['count']}, Density: {stat['density']}%")
            st.markdown(f"**📊 Total Combined Keyword Density:** {total_density}%")
        else:
            st.info("No keywords provided.")
