import re
import string
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

# Function to clean text (remove markdown, symbols, etc.)
def clean_text(text):
    text = re.sub(r'\*\*|__|##+|[*#>-]', '', text)  # remove markdown symbols
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    return text.strip()

# Function to count words like QuillBot
def quillbot_style_word_count(text):
    cleaned = clean_text(text)
    words = re.findall(r"\b[\w’'-]+\b", cleaned)  # includes hyphenated and apostrophized words
    return len(words), words

# Function to calculate keyword density
def keyword_density(words, top_n=10):
    freq = Counter(words)
    total_words = len(words)
    top_keywords = freq.most_common(top_n)
    density_data = [(word, count, round((count/total_words)*100, 2)) for word, count in top_keywords]
    return density_data, freq

# Function to estimate reading time
def reading_time(word_count):
    words_per_minute = 250  # average reading speed
    time_minutes = word_count / words_per_minute
    return round(time_minutes, 2)

# Streamlit UI
st.title("📝 Article Analyzer with Keyword Density & Read Time")

user_input = st.text_area("Paste your article below:", height=400)

if user_input:
    word_count, word_list = quillbot_style_word_count(user_input)
    density_data, freq_dict = keyword_density(word_list)
    total_density = round(sum([item[2] for item in density_data]), 2)
    read_minutes = reading_time(word_count)

    st.markdown(f"### 📊 Results")
    st.write(f"**Total Words (QuillBot-style):** {word_count}")
    st.write(f"**Estimated Reading Time:** {read_minutes} minutes")
    st.write(f"**Total Combined Keyword Density (Top {len(density_data)}):** {total_density}%")

    # Show keyword density table
    st.markdown("#### 🔑 Top Keywords")
    df = pd.DataFrame(density_data, columns=["Keyword", "Count", "Density (%)"])
    st.dataframe(df, use_container_width=True)

    # Plotting frequency chart
    st.markdown("#### 📈 Keyword Frequency Chart")
    fig, ax = plt.subplots()
    keywords, counts = zip(*[(k, c) for k, c, _ in density_data])
    ax.bar(keywords, counts, color='skyblue')
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Keyword')
    ax.set_title('Top Keyword Frequency')
    st.pyplot(fig)
