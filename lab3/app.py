import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

obl_dict = {
    1: "Черкаська",
    2: "Чернігівська",
    3: "Чернівецька",
    4: "АР Крим",
    5: "Дніпропетровська",
    6: "Донецька",
    7: "Івано-Франківська",
    8: "Харківська",
    9: "Херсонська",
    10: "Хмельницька",
    11: "Київська",
    12: "м. Київ",
    13: "Кіровоградська",
    14: "Луганська",
    15: "Львівська",
    16: "Миколаївська",
    17: "Одеська",
    18: "Полтавська",
    19: "Рівненська",
    20: "м. Севастополь",
    21: "Сумська",
    22: "Тернопільська",
    23: "Закарпатська",
    24: "Вінницька",
    25: "Волинська",
    26: "Запорізька",
    27: "Житомирська"
}
DEFAULTS = {
    'min_week': 1,
    'max_week': 52,
    'min_year': 1982,
    'max_year': 2024,
    'slider_week': (1,52),
    'slider_year': (1982, 2024),
    'sort_ascending': True,
    'sort_descending': False,
    'set': 'vci',
    'oblast': 'Черкаська'
}
df = pd.read_csv('df/combined_df.csv', index_col=False)

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def check_boxes(field):
    a = ['sort_ascending', 'sort_descending']
    a.remove(field)
    the_other=a[0]

    if st.session_state[field]:
        st.session_state[the_other] = False

def filter_data(min_year, max_year, min_week, max_week, set, oblast, sort_ascending, sort_descending):
    obl =  [k for k, v in obl_dict.items() if v == oblast][0]
    selected_df = df[(df['year'] >= min_year) & (df['year'] <= max_year) &
                     (df['week'] >= min_week) & (df['week'] <= max_week) &
                     (df['oblast'] == obl)]
    selected_df = selected_df[['year','week',set]]

    the_rest_df = df[(df['year'] >= min_year) & (df['year'] <= max_year) &
                     (df['week'] >= min_week) & (df['week'] <= max_week)]

    the_rest_df = the_rest_df[['year','week',set, 'oblast']]
    # ang_df = the_rest_df.groupby(['year', 'oblast'], as_index=False)[set].mean()

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=selected_df, x="year", y=set, ax=ax1, label='Обрана область')
    sns.barplot(data=the_rest_df, x = 'oblast', y=set, ax=ax2)
    # sns.lineplot(data=selected_df, x="year", y=set, ax=ax2, label='Обрана область')
    # sns.lineplot(data=ang_df, x="year", y=set, ax=ax2, label='Решта')

    if sort_ascending and not sort_descending:
        table = selected_df.sort_values(by=[set])
    elif not sort_ascending and sort_descending:
        table = selected_df.sort_values(by=[set], ascending=False)
    else:
        table = selected_df
    return table, fig1, fig2

st.markdown(
    """
    <style>
        .block-container {
            max-width: 80%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, _, col2 = st.columns([10, 1, 5])  # 3:1 співвідношення

with col1:
    col1_1, col1_2, col1_3 = col1.columns(3)

    tab1, tab2, tab3 = st.tabs(["Табличка", "Графік", "Порівняння"])


    min_year = st.session_state['min_year']
    max_year = st.session_state['max_year']
    min_week = st.session_state['min_week']
    max_week = st.session_state['max_week']
    set = st.session_state['set']
    oblast = st.session_state['oblast']
    sort_ascending = st.session_state['sort_ascending']
    sort_descending = st.session_state['sort_descending']

    table, fig1, fig2 = filter_data(min_year, max_year, min_week, max_week, set, oblast, sort_ascending, sort_descending)

    with tab1:
        st.write(table)

    with tab2:
        st.pyplot(fig1)

    with tab3:
        st.pyplot(fig2)

with col2:

    #ДВА ВИПАДНИХ СПИСКИ
    col2_1, col2_2 = col2.columns([2, 3])
    col2_1.selectbox(
        'Оберіть індекс',
        ('vci', 'tci', 'vhi'),
        key='set')

    col2_2.selectbox(
        'Оберіть область',
        obl_dict.values(),
        key='oblast')


 #СДАЙДЕР ТИЖНІ
    st.markdown("<hr>" '<b>Оберіть тижні</b>', unsafe_allow_html=True)

    slider_week = st.slider(
        " ",
        min_value=1, max_value=52,
        key='slider_week')
    st.session_state['min_week'], st.session_state['max_week'] = slider_week

  #СЛАЙДЕР РОКІВ
    st.markdown("<hr>" '<b>Оберіть роки</b>', unsafe_allow_html=True)

    slider_year = st.slider(
        " ",
        min_value=1982, max_value=2024,
        key='slider_year')
    st.session_state['min_year'], st.session_state['max_year'] = slider_year

   # -----------------------------------------------------------------------------
    # РЕЖИМ СОРТУВАННЯ
    st.markdown("<hr>" '<b>Оберіть як сортувати</b>', unsafe_allow_html=True)

    st.checkbox('За зростанням', key='sort_ascending', on_change=check_boxes, args=('sort_ascending',))
    st.checkbox('За спаданням', key='sort_descending', on_change=check_boxes, args=('sort_descending',))


    #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    def reset_filters():
        for key in DEFAULTS:
            st.session_state.pop(key, None)


    st.button("Скинути фільтри", on_click=reset_filters)

