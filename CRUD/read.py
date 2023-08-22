import streamlit as st
import mysql.connector
import pandas as pd

def build_header():
    st.markdown('<h1>Consultas dinâmicas para o BD Empresa🔎</h1>', unsafe_allow_html=True)
    st.markdown('<p>Realização de operações CRUD no esquema Empresa. Para efetuar quaisquer buscas (<i>queries</i>), é necessário selecionar uma tabela e especificar a condição de filtragem no campo query. Para isso, se faz necessário que a consulta no formato <code>SQL.</code></p>', unsafe_allow_html=True)

def reset_query():
    query_str = ""
    st.session_state.query_text = query_str
    return query_str

def build_filter_controls(table_names):
    selected_table = st.selectbox("Selecione uma tabela:", table_names)
    return selected_table

def build_query_controls():
    if "query_text" not in st.session_state:
        st.session_state.query_text = ""
    query_str = st.text_area("Query", height=5, value=st.session_state.query_text, placeholder="Insira a condição de filtragem (ex: coluna = valor)", help="A query de busca é case sensitive.")
    if st.button("Limpar filtros"):
        query_str = reset_query()
    st.session_state.query_text = query_str
    return query_str

def build_groupby_controls(df):
    st.write("Selecione as opções de agrupamento:")
    group_cols = st.multiselect("Agrupar por:", options=list(df.columns), default=df.columns[0])
    cols = st.multiselect("Totalizar por:", options=list(df.columns), default=df.columns[1])
    function = st.selectbox("Selecione a função de agregação:", options=['count', 'sum', 'avg', 'min', 'max'], index=0)

    if st.button("Aplicar agrupamento"):
        if group_cols and cols:
            grouped_df = df[group_cols + cols].groupby(by=group_cols).agg({col: function for col in cols}).reset_index()
            st.write("Exibindo tabela resultante do agrupamento:")
            st.dataframe(grouped_df, use_container_width=True)
        else:
            st.warning("Selecione pelo menos uma coluna de agrupamento e uma coluna para totalizar.")

def build_body(connection, cursor, selected_table, query_str):
    st.write(f"Exibindo dados da tabela '{selected_table}':")
    full_query = f"SELECT * FROM {selected_table}"
    if query_str:
        full_query += f" WHERE {query_str}"
    cursor.execute(full_query)
    data = cursor.fetchall()
    if data:
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=column_names)
        st.dataframe(df, width=1000)
        build_groupby_controls(df)
    else:
        st.write("No data available.")

def main():
    build_header()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raquel", #Se não houver senha no BD do MySQL, utiliza-se password = ""
        database="empresa_bd"
    )
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    table_names = [table[0] for table in cursor.fetchall()]
    selected_table = build_filter_controls(table_names)
    query_str = build_query_controls()
    build_body(connection, cursor, selected_table, query_str)

if __name__ == "__main__":
    main()