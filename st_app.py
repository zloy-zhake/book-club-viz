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

# TODO: изменить отображаемые названия столбцов
# TODO: оформить даты как даты
books_df = pd.read_excel(io="book_list.xlsx", sheet_name="Sheet1")
# Format as dollar amount with two decimal places
styled_books_df = books_df.style.format({"year_written_or_published": "{:.0f}"})

st.dataframe(data=styled_books_df)

st.header(body="Общая статистика", anchor="general_stats", divider=True)

dates_df = books_df[["meeting_year", "meeting_month", "meeting_day"]]

num_meetings = dates_df.drop_duplicates().shape[0]
msg = f"Количество проведённых встреч: **{num_meetings}**."
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
# 1 автора
# 2 авторов
# 3 авторов
# 4 авторов
# 5 авторов
# 6 авторов
# 7 авторов
# 8 авторов
# 9 авторов
num_authors_last_digit = num_authors % 10
if num_authors_last_digit == 1:
    author_inflection = "автора"
else:
    author_inflection = "авторов"

genres_col = books_df["genres"].to_list()
genres = [parse_string_list(item) for item in genres_col]
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
    f"Прочитано: **{len(books_df)}** {book_inflection} "
    f"**{len(authors_uniq)}** {author_inflection} "
    f"в **{num_genres}** {genre_inflection}."
)
st.write(msg)

num_pages_col = books_df["num_pages"].to_list()
num_pages_total = sum(num_pages_col)
num_pages_total_str = f"{num_pages_total:_.0f}".replace("_", " ")

pages_height = num_pages_total * PAPER_THICKNESS_IN_METERS
pages_height_str = f"{pages_height:.2f}".replace(".", ",")

num_words = num_pages_total * AVG_NUM_WORDS_PER_PAGE
num_words_str = f"{num_words:_.0f}".replace("_", " ")

num_sentences = num_words / AVG_NUM_WORDS_PER_SENTENCE
num_sentences_str = f"{num_sentences:_.0f}".replace("_", " ")

msg = (
    f"Примерное количество прочитанных страниц: **{num_pages_total_str}**. "
    "Если сложить столько страниц в одну стопку, "
    f"то её высота составит, примерно, **{pages_height_str} м.** "
    "(Из расчёта, что толщина одной страницы составляет "
    f"{PAPER_THICKNESS_IN_METERS * 1_000} мм.)"
)
st.write(msg)

msg = (
    f"Примерное количество прочитанных предложений: **{num_sentences_str}**. "
    f"(Из расчёта {AVG_NUM_WORDS_PER_SENTENCE} слов на предложение)"
)
st.write(msg)

msg = (
    f"Примерное количество прочитанных слов: **{num_words_str}**. "
    f"(Из расчёта {AVG_NUM_WORDS_PER_PAGE} слов на страницу): "
)
st.write(msg)

# самая толстая книга
max_pages = max(num_pages_col)
max_pages_rows = books_df.loc[books_df["num_pages"] == max_pages]
if max_pages_rows.shape[0] > 1:
    msg = "Самые толстые прочитанные книги: "
else:
    msg = "Самая толстая прочитанная книга: "
for row in max_pages_rows.itertuples():
    msg += f"**{row.author[1:-1]} *{row.title}*** ({row.num_pages} стр.), "
msg = msg[:-2] + "."
st.write(msg)

# самая тонкая книга
min_pages = min(num_pages_col)
min_pages_rows = books_df.loc[books_df["num_pages"] == min_pages]
if min_pages_rows.shape[0] > 1:
    msg = "Самые тонкие прочитанные книги: "
else:
    msg = "Самая тонкая прочитанная книга: "
for row in min_pages_rows.itertuples():
    msg += f"**{row.author[1:-1]} *{row.title}*** ({row.num_pages} стр.), "
msg = msg[:-2] + "."
st.write(msg)

# самый популярный жанр
genres_counter = Counter(genres)
genres_by_freq = genres_counter.most_common()

most_freq_genre_num = genres_by_freq[0][1]
if genres_by_freq[1][1] == most_freq_genre_num:
    msg = "Самые популярные жанры: "
else:
    msg = "Самый популярный жанр: "
for genre, freq in genres_by_freq:
    if freq < most_freq_genre_num:
        break
    msg += f"**{genre}** ({freq} кн.), "
msg = msg[:-2] + "."
st.write(msg)

# самые популярные авторы
authors_counter = Counter(authors)
authors_by_freq = authors_counter.most_common()

most_freq_author_num = authors_by_freq[0][1]
if authors_by_freq[1][1] == most_freq_author_num:
    msg = "Самые популярные авторы: "
else:
    msg = "Самый популярный автор: "
for author, freq in authors_by_freq:
    if freq < most_freq_author_num:
        break
    msg += f"**{author}** ({freq} кн.), "
msg = msg[:-2] + "."
st.write(msg)

# самые популярные страны
country_col = books_df["author_country"].to_list()
countries = [parse_string_list(item) for item in country_col]
countries = [item for sublist in countries for item in sublist]
countries_counter = Counter(countries)
countries_by_freq = countries_counter.most_common()

most_freq_country_num = countries_by_freq[0][1]
if countries_by_freq[1][1] == most_freq_country_num:
    msg = "Самые популярные страны: "
else:
    msg = "Самая популярная страна: "
for country, freq in countries_by_freq:
    if freq < most_freq_country_num:
        break
    msg += f"**{country}** ({freq} кн.), "
msg = msg[:-2] + "."
st.write(msg)

st.header(
    body="Количество прочитанных книг каждого автора", anchor="autors", divider=True
)

fig1, ax1 = plt.subplots(figsize=(10, 20))
ax1.barh(
    range(len(authors_by_freq)), [item[1] for item in authors_by_freq], align="center"
)
ax1.set_yticks(range(len(authors_by_freq)))
ax1.set_yticklabels([item[0] for item in authors_by_freq])
ax1.invert_yaxis()
ax1.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax1.grid(axis="x", linestyle="dashed")
ax1.set_xlabel("Количество книг")

st.pyplot(fig1)

st.header(body="Распределение авторов по странам", anchor="countries", divider=True)

author_country_df = books_df[["author", "author_country"]]
author_country_df = author_country_df.drop_duplicates(subset="author")
country_col_2 = author_country_df["author_country"].to_list()
countries = [parse_string_list(item) for item in country_col_2]
countries = [item for sublist in countries for item in sublist]
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

col_countries_1, col_countries_2 = st.columns(spec=(0.7, 0.3))

with col_countries_1:
    st.pyplot(fig4)

with col_countries_2:
    freq_sum = sum(item[1] for item in countries_by_freq)
    msg = ""
    for country, freq in countries_by_freq:
        msg += f"- {country}: {freq} ав. ({freq / freq_sum * 100:.1f}%)\n"
    st.write(msg)

st.header(
    body="Распределение книг по годам написания/издания", anchor="years", divider=True
)

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
ax3.xaxis.set_tick_params(rotation=75)
ax3.yaxis.set_major_locator(mticker.MultipleLocator(1))
ax3.grid(axis="y", linestyle="dashed")
ax3.set_ylabel("Количество книг")

st.pyplot(fig3)

st.header(body="Распределение книг по жанрам", anchor="genres", divider=True)

fig4, ax4 = plt.subplots()
ax4.pie(
    [item[1] for item in genres_by_freq],
    labels=[f"{item[0]}\n({item[1]} кн.)" for item in genres_by_freq],
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.1] * len(genres_by_freq),
)
ax4.axis("equal")

col_genres_1, col_genres_2 = st.columns(spec=(0.7, 0.3))

with col_genres_1:
    st.pyplot(fig4)

with col_genres_2:
    freq_sum = sum(item[1] for item in genres_by_freq)
    msg = ""
    for genre, freq in genres_by_freq:
        msg += f"- {genre}: {freq} кн. ({freq / freq_sum * 100:.1f}%)\n"
    st.write(msg)


# количество страниц, прочитанных в месяц
# количество страниц по времени,
st.header(
    body="Количество страниц, читаемых в месяц", anchor="pages_per_month", divider=True
)

pages_dates_df = books_df[["num_pages", "meeting_year", "meeting_month", "meeting_day"]]

pages_per_month_dict = {}
# "meeting_month"-"meeting_year": "num_pages"
for index, row in pages_dates_df.iterrows():
    year = row["meeting_year"]
    month = row["meeting_month"]
    num_pages = row["num_pages"]
    # pages_per_month_dict[f"{month}-{year}"] = 0
    if row["meeting_day"] < 15:
        if month == 1:
            month = 12
        else:
            month -= 1
    if f"{month}-{year}" not in pages_per_month_dict:
        pages_per_month_dict[f"{month}-{year}"] = 0
    pages_per_month_dict[f"{month}-{year}"] += num_pages

fig5, ax5 = plt.subplots(figsize=(20, 10))
ax5.bar(
    [f"{m_y}" for m_y in pages_per_month_dict],
    list(pages_per_month_dict.values()),
)
ax5.xaxis.set_tick_params(rotation=75)
ax5.grid(axis="y", linestyle="dashed")
ax5.set_ylabel("Количество страниц")

st.pyplot(fig5)


# гистограмма толщины книг
st.header(
    body=(
        "Распределение (гистограмма) количества страниц книг  "
        "(книги какой толщины мы читаем больше всего / меньше всего)"
    ),
    anchor="pages",
    divider=True,
)

book_num_pages = books_df["num_pages"].to_list()

fig6, ax6 = plt.subplots()
ax6.hist(book_num_pages, bins=20)
ax6.xaxis.set_major_locator(mticker.MultipleLocator(100))
ax6.yaxis.set_major_locator(mticker.MultipleLocator(1))
ax6.grid(axis="y", linestyle="dashed")
ax6.set_xlabel("Количество страниц")
ax6.set_ylabel("Количество книг")

st.pyplot(fig6)
