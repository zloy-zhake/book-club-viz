from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import streamlit as st

from book_viz_utils import parse_string_list

AVG_NUM_WORDS_PER_PAGE = 300
AVG_NUM_WORDS_PER_SENTENCE = 15
PAPER_THICKNESS_IN_METERS = 0.000103

st.title(body="Книжный клуб «Читаем вместе», г. Алматы")

st.write("https://vk.com/chitaemvmestealmaty")
st.write("https://www.instagram.com/chitaemvmestealmaty/")

st.header(body="Что мы уже прочитали", anchor="book_list", divider=True)

books_df = pd.read_excel(io="book_list.xlsx", sheet_name="Sheet1")
styled_books_df = books_df.style.format(
    {
        "year_written_or_published": "{:.0f}",  # Format as dollar amount with two decimal places
    }
)

st.dataframe(data=styled_books_df)

st.header(body="Общая статистика", anchor="general_stats", divider=True)

dates_df = books_df[["meeting_year", "meeting_month", "meeting_day"]]

num_meetings = dates_df.drop_duplicates().shape[0]
# 0 встреч
# 1 встреча
# 2 встречи
# 3 встречи
# 4 встречи
# 5 встреч
# 6 встреч
# 7 встреч
# 8 встреч
# 9 встреч
num_meetings_last_digit = num_meetings % 10
if 5 <= num_meetings <= 20:
    meeting_inflection = "встреч"
elif num_meetings_last_digit == 1:
    meeting_inflection = "встреча"
elif 2 <= num_meetings_last_digit <= 4:
    meeting_inflection = "встречи"
else:
    meeting_inflection = "встреч"


msg = f"Проведено {dates_df.drop_duplicates().shape[0]} {meeting_inflection}."
st.write(msg)

num_books = len(books_df)

# 0 книг
# 1 книга
# 2 книги
# 3 книги
# 4 книги
# 5 книг
# 6 книг
# 7 книг
# 8 книг
# 9 книг
num_books_last_digit = num_books % 10
if 5 <= num_books <= 20:
    book_inflection = "книг"
elif num_books_last_digit == 1:
    book_inflection = "книга"
elif 2 <= num_books_last_digit <= 4:
    book_inflection = "книги"
else:
    book_inflection = "книг"

authors_col = books_df["author"].to_list()
authors = [parse_string_list(item) for item in authors_col]
authors = [item for sublist in authors for item in sublist]
authors_uniq = set(authors)

num_authors = len(authors_uniq)
# 0 авторов
# 1 автор
# 2 автора
# 3 автора
# 4 автора
# 5 авторов
# 6 авторов
# 7 авторов
# 8 авторов
# 9 авторов
num_authors_last_digit = num_authors % 10
if 5 <= num_authors <= 20:
    author_inflection = "авторов"
elif num_authors_last_digit == 1:
    author_inflection = "автор"
elif 2 <= num_authors_last_digit <= 4:
    author_inflection = "автора"
else:
    author_inflection = "авторов"

genres = books_df["genres"].to_list()
genres = [parse_string_list(item) for item in genres]
genres = [item for sublist in genres for item in sublist]
genres_uniq = set(genres)

num_genres = len(genres_uniq)
# в x0 жанрах
# в 1 жанре
# в 2 жанрах
# в 3 жанрах
# в 4 жанрах
# в 5 жанрах
# в 6 жанрах
# в 7 жанрах
# в 8 жанрах
# в 9 жанрах
num_genres_last_digit = num_genres % 10
if 2 <= num_genres <= 20:
    genre_inflection = "жанрах"
elif num_genres_last_digit == 1:
    genre_inflection = "жанре"
else:
    genre_inflection = "жанрах"


msg = (
    f"Прочитано {len(books_df)} {book_inflection} "
    f"{len(authors_uniq)} {author_inflection} "
    f"в {num_genres} {genre_inflection}."
)
st.write(msg)

num_pages_list = books_df["num_pages"].to_list()
num_pages_total = sum(num_pages_list)
num_pages_total_str = f"{num_pages_total:_.0f}".replace("_", " ")
msg = f"Примерное количество прочитанных страниц: {num_pages_total_str}."
st.write(msg)

pages_height = num_pages_total * PAPER_THICKNESS_IN_METERS
pages_height_str = f"{pages_height:.2f}".replace(".", ",")
msg = (
    f"Если сложить столько страниц в одну стопку, "
    f"то её высота составит, примерно, {pages_height_str} м."
)
st.write(msg)

num_words = num_pages_total * AVG_NUM_WORDS_PER_PAGE
num_words_str = f"{num_words:_.0f}".replace("_", " ")
msg = (
    f"Примерное количество прочитанных слов "
    f"(из расчёта {AVG_NUM_WORDS_PER_PAGE} слов на страницу): "
    f"{num_words_str}."
)
st.write(msg)

num_sentences = num_words / AVG_NUM_WORDS_PER_SENTENCE
num_sentences_str = f"{num_sentences:_.0f}".replace("_", " ")
msg = (
    f"Примерное количество прочитанных предложений "
    f"(из расчёта {AVG_NUM_WORDS_PER_SENTENCE} слов на предложение): "
    f"{num_sentences_str}."
)
st.write(msg)

# самая толстая книга
# самая тонкая книга
# самый популярный жанр
# самые популярные авторы
# самые популярные страны

st.header(body="Распределение книг по авторам", anchor="autors", divider=True)

authors_counter = Counter(authors)
authors_by_freq = authors_counter.most_common()

fig1, ax1 = plt.subplots(figsize=(10, 10))
ax1.barh(
    range(len(authors_by_freq)), [item[1] for item in authors_by_freq], align="center"
)
ax1.set_yticks(range(len(authors_by_freq)))
ax1.set_yticklabels([item[0] for item in authors_by_freq])
ax1.invert_yaxis()
ax1.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax1.set_xlabel("Количество книг")
ax1.set_title("Распределение книг по авторам")

st.pyplot(fig1)

st.header(body="Распределение авторов по странам", anchor="countries", divider=True)

countries = books_df["author_country"].to_list()
countries_counter = Counter(countries)
countries_by_freq = countries_counter.most_common()

fig4, ax4 = plt.subplots()
ax4.pie(
    [item[1] for item in countries_by_freq],
    labels=[f"{item[0]}\n({item[1]} ав.)" for item in countries_by_freq],
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.1] * len(countries_by_freq),
)
ax4.axis("equal")

st.pyplot(fig4)


st.header(body="Распределение книг по годам", anchor="years", divider=True)

years = books_df["year_written_or_published"].to_list()
years_counter = Counter(years)
years_counter_by_freq = years_counter.most_common()
years_counter_by_freq = sorted(years_counter_by_freq, key=lambda x: x[0])
years, book_counts = zip(*years_counter_by_freq)  # noqa

dacades_start = years[0] - years[0] % 10
dacades_end = years[-1] + (10 - years[-1] % 10)
dacades = list(range(dacades_start, dacades_end + 10, 10))
books_per_decade = {
    (dacades[i] + 1, dacades[i + 1]): 0 for i in range(len(dacades) - 1)
}
for year, count in zip(years, book_counts):
    decade = (year - year % 10 + 1, year + (10 - year % 10))
    books_per_decade[decade] += count

fig3, ax3 = plt.subplots()
ax3.bar(
    [f"{item[0]}-{item[1]}" for item in books_per_decade],
    list(books_per_decade.values()),
)
ax3.xaxis.set_tick_params(rotation=90)
ax3.yaxis.set_major_locator(mticker.MultipleLocator(1))
ax3.set_ylabel("Количество книг")

st.pyplot(fig3)

st.header(body="Распределение книг по жанрам", anchor="genres", divider=True)

genres_counter = Counter(genres)
genres_by_freq = genres_counter.most_common()

fig4, ax4 = plt.subplots()
ax4.pie(
    [item[1] for item in genres_by_freq],
    labels=[f"{item[0]}\n({item[1]} кн.)" for item in genres_by_freq],
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.1] * len(genres_by_freq),
)
ax4.axis("equal")

st.pyplot(fig4)
