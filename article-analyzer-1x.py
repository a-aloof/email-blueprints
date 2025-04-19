import streamlit as st
import re
from collections import Counter
import matplotlib.pyplot as plt
import string

# ----------- FUNCTIONS -----------

def quillbot_style_word_count(text):
    # Strip markdown, punctuation and count real words
    text_clean = re.sub(r'(\*\*|__|##+|[*`~_>\[\]()!#])', '', text)  # remove markdown
    words = re.findall(r"\b[\w'-]+\b", text)  # more liberal than split()
    return len(words), words

def calculate_reading_time(word_count, wpm=250):
    minutes = word_count / wpm
    return round(minutes, 2)

def compute_keyword_density(words):
    lower_words = [word.lower() for word in words]
    word_counts = Counter(lower_words)
    total_words = len(words)
    density = {word: round((count / total_words) * 100, 2) for word, count in word_counts.items()}
    return word_counts, density

def plot_keyword_chart(word_counts, top_n=10):
    common = word_counts.most_common(top_n)
    words, counts = zip(*common)
    fig, ax = plt.subplots()
    ax.bar(words, counts, color='skyblue')
    plt.xticks(rotation=45)
    plt.title(f"Top {top_n} Keywords")
    plt.xlabel("Keyword")
    plt.ylabel("Frequency")
    st.pyplot(fig)

# ----------- STREAMLIT UI -----------

st.title("📝 Article Analyzer (QuillBot Style)")

article_text = st.text_area("Paste your article here:", height=400)

if article_text:
    # Word Count
    word_count, words = quillbot_style_word_count(article_text)
    st.write(f"**Word Count (QuillBot style):** {word_count}")

    # Reading Time
    read_time = calculate_reading_time(word_count)
    st.write(f"**Estimated Reading Time:** {read_time} minutes")

    # Keyword Density
    word_freqs, word_density = compute_keyword_density(words)
    total_keywords = len(word_freqs)
    st.write(f"**Total Unique Keywords:** {total_keywords}")

    # Show top keywords
    top_keywords = dict(word_freqs.most_common(10))
    st.subheader("🔑 Top Keyword Frequency")
    st.write(top_keywords)

    # Plot Chart
    st.subheader("📊 Keyword Frequency Chart")
    plot_keyword_chart(word_freqs)
