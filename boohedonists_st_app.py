import json
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import streamlit as st

from book_club_viz_utils import (
    get_authors_inflection,
    get_books_inflection,
    get_column_values_as_list,
    get_genres_inflection,
    get_num_meetings_from_df,
    is_dict_has_n_or_more_consecutive_values,
    shrink_dict_consecutive_values,
)

AVG_NUM_WORDS_PER_PAGE = 300
AVG_NUM_WORDS_PER_SENTENCE = 15
PAPER_THICKNESS_IN_METERS = 0.000103

st.title(body="Книггедонисты📚")

tab_with_book_stats, tab_with_reviews = st.tabs(
    ["Статистика по книгам", "Отзывы на книги"]
)

with tab_with_book_stats:
    books_df = pd.read_excel(
        io="boohedonists_files/boohedonists_book_list.xlsx", sheet_name="Sheet1"
    )

    year_options = ["все годы"] + [
        f"{year} год" for year in sorted(books_df["voting_year"].unique())
    ]
    year_chosen_str = st.selectbox(
        label="Выберите год:",
        options=year_options,
        placeholder=year_options[0],
        help="Выберите год, за который хотите посмотреть статистику",
    )
    if year_chosen_str is None:
        year_chosen_str = year_options[0]
    if year_chosen_str != "все годы":
        year_chosen = int(year_chosen_str[:4])
        books_df = books_df[books_df["voting_year"] == year_chosen]

    books_df.index = pd.Index(data=range(1, len(books_df) + 1))
    # убираем запятые из отображения годов (1,984 -> 1984)
    styled_books_df = books_df.style.format(
        formatter={"year_written_or_published": "{:.0f}"}
    )

    st.header(
        body=f"Что мы уже выбирали для чтения (за {year_chosen_str})",
        anchor="book_list",
        divider=True,
    )

    st.dataframe(data=styled_books_df)

    st.header(
        body=f"Общая статистика (за {year_chosen_str})",
        anchor="general_stats",
        divider=True,
    )

    num_meetings = get_num_meetings_from_df(
        df=books_df, columns_subset=["voting_year", "voting_month", "voting_day"]
    )
    msg = f"Количество проведённых голосований за книги: **{num_meetings}**."
    st.write(msg)

    num_books = len(books_df)
    books_inflection_str = get_books_inflection(num_books=num_books)

    authors = get_column_values_as_list(df=books_df, column_name="author")
    authors_uniq = set(authors)
    num_authors_uniq = len(authors_uniq)
    author_inflection_str = get_authors_inflection(num_authors=num_authors_uniq)

    genres = get_column_values_as_list(df=books_df, column_name="genres")
    genres_uniq = set(genres)
    num_genres_uniq = len(genres_uniq)
    genre_inflection = get_genres_inflection(num_genres=num_genres_uniq)

    msg = (
        f"Выбрано для чтения: **{num_books}** {books_inflection_str} "
        f"**{num_authors_uniq}** {author_inflection_str} "
        f"в **{num_genres_uniq}** {genre_inflection}."
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
        f"Примерное количество страниц в выбранных книгах: **{num_pages_total_str}**. "
        "Если сложить столько страниц в одну стопку, "
        f"то её высота составит, примерно, **{pages_height_str} м.** "
        "(Из расчёта, что толщина одной страницы составляет "
        f"{PAPER_THICKNESS_IN_METERS * 1_000} мм.)"
    )
    st.write(msg)

    msg = (
        f"Примерное количество предложений в выбранных книгах: **{num_sentences_str}**. "
        f"(Из расчёта {AVG_NUM_WORDS_PER_SENTENCE} слов на предложение)"
    )
    st.write(msg)

    msg = (
        f"Примерное количество слов в выбранных книгах: **{num_words_str}**. "
        f"(Из расчёта {AVG_NUM_WORDS_PER_PAGE} слов на страницу): "
    )
    st.write(msg)

    # определяем самую толстую книгу
    max_pages = max(num_pages_col)
    max_pages_rows = books_df.loc[books_df["num_pages"] == max_pages]
    if max_pages_rows.shape[0] > 1:
        msg = "Самые толстые выбранные книги: "
    else:
        msg = "Самая толстая выбранная книга: "
    for row in max_pages_rows.itertuples():
        msg += f"**{row.author[1:-1]} *{row.title}*** ({row.num_pages} стр.), "
    msg = msg[:-2] + "."
    st.write(msg)

    # определяем самую тонкую книгу
    min_pages = min(num_pages_col)
    min_pages_rows = books_df.loc[books_df["num_pages"] == min_pages]
    if min_pages_rows.shape[0] > 1:
        msg = "Самые тонкие выбранные книги: "
    else:
        msg = "Самая тонкая выбранная книга: "
    for row in min_pages_rows.itertuples():
        msg += f"**{row.author[1:-1]} *{row.title}*** ({row.num_pages} стр.), "
    msg = msg[:-2] + "."
    st.write(msg)

    # определеяем самый популярный жанр
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

    # определяем самого популярного автора
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

    # определеяем самую популярную страну
    countries = get_column_values_as_list(df=books_df, column_name="author_country")
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
        body=f"Количество выбранных книг каждого автора (за {year_chosen_str})",
        anchor="autors",
        divider=True,
    )

    fig1, ax1 = plt.subplots(figsize=(10, 20))
    ax1.barh(
        y=range(len(authors_by_freq)),
        width=[item[1] for item in authors_by_freq],
        align="center",
    )
    ax1.set_yticks(ticks=range(len(authors_by_freq)))
    ax1.set_yticklabels(labels=[item[0] for item in authors_by_freq])
    ax1.invert_yaxis()
    ax1.xaxis.set_major_locator(locator=mticker.MultipleLocator(1))
    ax1.grid(axis="x", linestyle="dashed")
    ax1.set_xlabel(xlabel="Количество книг")

    st.pyplot(fig=fig1)

    st.header(
        body=f"Количество книг по странам (за {year_chosen_str})",
        anchor="books_by_countries",
        divider=True,
    )

    book_country_df = books_df[["title", "author_country"]]
    book_country_df = book_country_df.drop_duplicates(subset="title")
    countries = get_column_values_as_list(
        df=book_country_df, column_name="author_country"
    )
    countries_counter = Counter(countries)
    countries_by_freq = countries_counter.most_common()

    fig4, ax4 = plt.subplots()
    ax4.pie(
        x=[item[1] for item in countries_by_freq],
        labels=[f"{item[0]}\n({item[1]} кн.)" for item in countries_by_freq],
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.1] * len(countries_by_freq),
    )
    ax4.axis("equal")

    col_countries_1, col_countries_2 = st.columns(spec=(0.7, 0.3))
    with col_countries_1:
        st.pyplot(fig=fig4)
    with col_countries_2:
        freq_sum = sum(item[1] for item in countries_by_freq)
        msg = ""
        for country, freq in countries_by_freq:
            msg += f"- {country}: {freq} кн. ({freq / freq_sum * 100:.1f}%)\n"
        st.write(msg)

    st.header(
        body=f"Количество авторов по странам (за {year_chosen_str})",
        anchor="countries",
        divider=True,
    )

    authors = get_column_values_as_list(df=books_df, column_name="author")
    countries = get_column_values_as_list(df=books_df, column_name="author_country")
    author_country_dict = {
        author: country for author, country in zip(authors, countries)
    }
    countries = list(author_country_dict.values())
    countries_counter = Counter(countries)
    countries_by_freq = countries_counter.most_common()

    fig4, ax4 = plt.subplots()
    ax4.pie(
        x=[item[1] for item in countries_by_freq],
        labels=[f"{item[0]}\n({item[1]} ав.)" for item in countries_by_freq],
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.1] * len(countries_by_freq),
    )
    ax4.axis("equal")

    col_countries_1, col_countries_2 = st.columns(spec=(0.7, 0.3))
    with col_countries_1:
        st.pyplot(fig=fig4)
    with col_countries_2:
        freq_sum = sum(item[1] for item in countries_by_freq)
        msg = ""
        for country, freq in countries_by_freq:
            msg += f"- {country}: {freq} ав. ({freq / freq_sum * 100:.1f}%)\n"
        st.write(msg)

    st.header(body="Количество авторов по полу", anchor="gender", divider=True)

    authors = get_column_values_as_list(df=books_df, column_name="author")
    genders = get_column_values_as_list(df=books_df, column_name="author_gender")
    author_gender_dict = {author: gender for author, gender in zip(authors, genders)}
    genders = list(author_gender_dict.values())
    genders_counter = Counter(genders)
    genders_by_freq = genders_counter.most_common()

    fig3, ax3 = plt.subplots()
    ax3.bar(
        x=[item[0] for item in genders_by_freq],
        height=[item[1] for item in genders_by_freq],
    )
    ax3.set_xticklabels(labels=[item[0] for item in genders_by_freq], rotation=45)

    fig2, ax2 = plt.subplots()
    ax2.pie(
        x=[item[1] for item in genders_by_freq],
        labels=[f"{item[0]}\n({item[1]} ав.)" for item in genders_by_freq],
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.1] * len(genders_by_freq),
    )
    ax2.axis("equal")

    col_genders_1, col_genders_2 = st.columns(spec=(0.5, 0.5))
    with col_genders_1:
        st.pyplot(fig=fig3)
    with col_genders_2:
        st.pyplot(fig=fig2)

    st.header(
        body=f"Распределение книг по годам написания/издания (за {year_chosen_str})",
        anchor="years",
        divider=True,
    )

    years = books_df["year_written_or_published"].to_list()
    years_counter = Counter(years)
    years_counter_by_freq = years_counter.most_common()
    years_counter_by_freq = sorted(years_counter_by_freq, key=lambda x: x[0])
    years, book_counts = zip(*years_counter_by_freq)  # type: ignore

    dacades_start = years[0] - years[0] % 10
    dacades_end = years[-1] + (10 - years[-1] % 10)
    dacades = list(range(dacades_start, dacades_end + 10, 10))
    books_per_decade_dict = {
        f"{dacades[i] + 1}-{dacades[i + 1]}": 0 for i in range(len(dacades) - 1)
    }
    for year, count in zip(years, book_counts):
        decade = f"{year - year % 10 + 1}-{year + (10 - year % 10)}"
        books_per_decade_dict[decade] += count

    if is_dict_has_n_or_more_consecutive_values(
        dict_=books_per_decade_dict, value=0, n=3
    ):
        decades, num_books = shrink_dict_consecutive_values(
            dict_=books_per_decade_dict,
            value_to_shrink=0,
            num_consecutive_values_to_shrink=3,
            fill_value="...",
        )
    else:
        decades, num_books = zip(*books_per_decade_dict.items())

    fig3, ax3 = plt.subplots()
    ax3.bar(x=decades, height=num_books)
    ax3.xaxis.set_tick_params(rotation=75)
    ax3.yaxis.set_major_locator(locator=mticker.MultipleLocator(1))
    ax3.grid(axis="y", linestyle="dashed")
    ax3.set_ylabel(ylabel="Количество книг")

    st.pyplot(fig=fig3)

    st.header(
        body=f"Количество книг по жанрам (за {year_chosen_str})",
        anchor="genres",
        divider=True,
    )

    fig4, ax4 = plt.subplots()
    ax4.pie(
        x=[item[1] for item in genres_by_freq],
        labels=[f"{item[0]}\n({item[1]} кн.)" for item in genres_by_freq],
        autopct="%1.1f%%",
        startangle=90,
        explode=[0.1] * len(genres_by_freq),
    )
    ax4.axis("equal")

    col_genres_1, col_genres_2 = st.columns(spec=(0.7, 0.3))
    with col_genres_1:
        st.pyplot(fig=fig4)
    with col_genres_2:
        freq_sum = sum(item[1] for item in genres_by_freq)
        msg = ""
        for genre, freq in genres_by_freq:
            msg += f"- {genre}: {freq} кн. ({freq / freq_sum * 100:.1f}%)\n"
        st.write(msg)

    st.header(
        body=f"Количество страниц в выбранных книгах в месяц (за {year_chosen_str})",
        anchor="pages_per_month",
        divider=True,
    )

    pages_dates_df = books_df[
        ["num_pages", "voting_year", "voting_month", "voting_day"]
    ]

    pages_per_month_dict = {}
    # создаём словарь вида: {"voting_month-voting_year": "num_pages"}
    for index, row in pages_dates_df.iterrows():
        year = row["voting_year"]
        month = row["voting_month"]
        num_pages = row["num_pages"]
        if row["voting_day"] < 15:
            if month == 1:
                month = 12
            else:
                month -= 1
        if f"{month}-{year}" not in pages_per_month_dict:
            pages_per_month_dict[f"{month}-{year}"] = 0
        pages_per_month_dict[f"{month}-{year}"] += num_pages

    fig5, ax5 = plt.subplots(figsize=(20, 10))
    ax5.bar(
        x=[f"{m_y}" for m_y in pages_per_month_dict],
        height=list(pages_per_month_dict.values()),
    )
    ax5.xaxis.set_tick_params(rotation=75)
    ax5.grid(axis="y", linestyle="dashed")
    ax5.set_ylabel(ylabel="Количество страниц")

    st.pyplot(fig=fig5)

    # гистограмма толщины книг
    st.header(
        body=(
            "Распределение (гистограмма) количества страниц в книгах "
            f"(за {year_chosen_str})"
        ),
        anchor="pages",
        divider=True,
    )

    st.write("Книги какой толщины мы выбираем больше всего / меньше всего.")
    book_num_pages = books_df["num_pages"].to_list()

    fig6, ax6 = plt.subplots()
    ax6.hist(x=book_num_pages, bins=20)
    ax6.xaxis.set_major_locator(locator=mticker.MultipleLocator(100))
    ax6.yaxis.set_major_locator(locator=mticker.MultipleLocator(1))
    ax6.set_xlim(left=0)
    ax6.set_xlabel(xlabel="Количество страниц")
    ax6.set_ylabel(ylabel="Количество книг")
    ax6.grid(axis="y", linestyle="dashed")

    st.pyplot(fig=fig6)

with tab_with_reviews:
    with open(
        "boohedonists_files/boohedonists_reviews.json", "r", encoding="utf-8"
    ) as f:
        reviews = json.load(f)

    review_sets_dict = {}
    for review in reviews:
        if f"{review["book_author"]} {review["book_title"]}" not in review_sets_dict:
            review_sets_dict[f"{review['book_author']} {review['book_title']}"] = [
                review
            ]
        else:
            review_sets_dict[f"{review['book_author']} {review['book_title']}"].append(
                review
            )

    for k, review_set in review_sets_dict.items():
        num_reviews = len(review_set)
        with st.expander(
            label=(
                f"📖 **{review_set[0]["book_author"]} "
                f"*{review_set[0]["book_title"]}*** "
                f"({num_reviews} отз.)"
            ),
            expanded=False,
        ):
            for review in review_set:
                with st.chat_message(name="human"):
                    reviewer = (
                        review["reviewer_alias"]
                        if review["reviewer_alias"] != ""
                        else review["reviewer"]
                    )
                    st.write(f"**{reviewer}** ({review["date"]}):")
                    st.write(review["review"])
