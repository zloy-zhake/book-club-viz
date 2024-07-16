import pandas as pd
from itertools import groupby


def get_num_meetings_from_df(df: pd.DataFrame, columns_subset: list[str]) -> int:
    """TODO:"""
    dates_df = df[columns_subset]
    num_meetings = dates_df.drop_duplicates().shape[0]
    return num_meetings


def parse_string_into_list(string):
    """
    Parse a string like "[a, b, c]" and return a list of strings like ["a", "b", "c"]

    Parameters
    ----------
    string : str
        String to parse.

    Returns
    -------
    list
        List of strings.
    """
    # Remove the brackets from the string
    string = string[1:-1]

    # Split the string by commas
    string_list = string.split(", ")

    # Trim whitespace from each string
    string_list = [s.strip() for s in string_list]

    return string_list


def get_column_values_as_list(df: pd.DataFrame, column_name: str) -> list[str]:
    column_values = df[column_name].to_list()
    column_values_as_lists = [parse_string_into_list(item) for item in column_values]
    column_values_flattened = [
        item for sublist in column_values_as_lists for item in sublist
    ]
    return column_values_flattened


def get_books_inflection(num_books: int) -> str:
    """
    TODO:
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
    """
    num_books_last_digit = num_books % 10
    if 5 <= num_books <= 20:
        book_inflection = "книг"
    elif num_books_last_digit == 1:
        book_inflection = "книга"
    elif 2 <= num_books_last_digit <= 4:
        book_inflection = "книги"
    else:
        book_inflection = "книг"
    return book_inflection


def get_authors_inflection(num_authors: int) -> str:
    """
    TODO:
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
    """
    num_authors_last_digit = num_authors % 10
    if 2 <= num_authors <= 20:
        author_inflection = "авторов"
    elif num_authors_last_digit == 1:
        author_inflection = "автора"
    else:
        author_inflection = "авторов"
    return author_inflection


def get_genres_inflection(num_genres: int) -> str:
    """
    TODO:
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
    """
    num_genres_last_digit = num_genres % 10
    if 2 <= num_genres <= 20:
        genre_inflection = "жанрах"
    elif num_genres_last_digit == 1:
        genre_inflection = "жанре"
    else:
        genre_inflection = "жанрах"
    return genre_inflection


def is_dict_has_n_or_more_consecutive_values(dict_: dict, value: int, n: int) -> bool:
    """TODO:"""
    result = False
    for val, val_consecutive_group in groupby(dict_.values()):
        if val == 0 and len(list(val_consecutive_group)) >= n:
            result = True
            break
    return result


DECADE = str  # "1911-1920"
BOOK_NUM = int


def shrink_dict_consecutive_values(
    dict_: dict,
    value_to_shrink: int,
    num_consecutive_values_to_shrink: int,
    fill_value: int | str,
) -> tuple[list[DECADE], list[BOOK_NUM]]:
    """TODO:"""
    keys = list(dict_.keys())
    values = list(dict_.values())

    new_keys = []
    new_values = []
    cur_index = 0
    for val, val_consecutive_group in groupby(values):
        consecutive_val_list = list(val_consecutive_group)
        if (
            val == value_to_shrink
            and len(consecutive_val_list) >= num_consecutive_values_to_shrink
        ):
            new_keys.append(keys[cur_index])
            new_values.append(val)
            new_keys.append(fill_value)
            new_values.append(val)
            cur_index = cur_index + len(consecutive_val_list) - 1
            new_keys.append(keys[cur_index])
            new_values.append(val)
            cur_index += 1
        else:
            new_keys.extend(keys[cur_index : cur_index + len(consecutive_val_list)])
            new_values.extend(consecutive_val_list)
            cur_index = cur_index + len(consecutive_val_list)

    return new_keys, new_values
