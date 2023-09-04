import streamlit as st
import mysql.connector

def build_header():
    st.markdown('<h1>Operações dinâmicas de Atualização para o BD Empresas 📲</h1>', unsafe_allow_html=True)
    st.markdown('<p>Execução de operações CRUD no contexto da estrutura de dados da Empresa. Ao efetuar operações de atualização, é fundamental selecionar a tabela relevante e especificar a condição de filtragem no campo de consulta. Para isso, é necessário fornecer o valor atualizado do campo correspondente.</p>', unsafe_allow_html=True)

def build_filter_controls(table_names):
    selected_table = st.radio("Selecione a tabela:", table_names)
    return selected_table

def build_update_form(selected_table, connection, cursor):
    st.write(f"Operações na tabela '{selected_table}':")

    operation_type = st.selectbox("Escolha o tipo de operação:", ["Modificar um atributo", "Modificar um ou mais atributos", "Adicionar uma coluna"])

    if operation_type == "Modificar um atributo":
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        column_names = [column[0] for column in cursor.fetchall()]
        update_form = st.form(key='update_form')
        update_form.header("Formulário de Atualização")
        attribute_to_update = update_form.selectbox("Selecione um atributo para efetuar a atualização:", column_names)
        new_value = update_form.text_input(f"Novo valor a ser inserido:")
        where_clause = update_form.text_input("Clausúla WHERE (ex: id = 1):", help="Operadores AND e OR são permitidos.")

        if update_form.form_submit_button("Update"):
            update_query = f"UPDATE {selected_table} SET {attribute_to_update} = %s WHERE {where_clause}"
            cursor.execute(update_query, (new_value,))
            connection.commit()
            st.success("Atualização aplicada com sucesso!")

    elif operation_type == "Modificar um ou mais atributos":
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        column_names = [column[0] for column in cursor.fetchall()]
        update_form = st.form(key='update_form')
        update_form.header("Formulário de Atualização")
        attributes_to_update = update_form.multiselect("Selecione atributos para atualização:", column_names)
        new_values_input = update_form.text_input("Novos valores (separados por vírgula):")
        new_values = [value.strip() for value in new_values_input.split(',')]
        where_clause = update_form.text_input("Clausúla WHERE (ex: id = 1):", help="Operadores AND e OR são permitidos.")

        if update_form.form_submit_button("Update"):
            if len(attributes_to_update) != len(new_values):
                st.error("O número de valores fornecidos deve ser igual ao número de atributos selecionados.")
            else:
                set_clause = ', '.join([f"{attr} = %s" for attr in attributes_to_update])
                update_query = f"UPDATE {selected_table} SET {set_clause} WHERE {where_clause}"
                cursor.execute(update_query, tuple(new_values))
                connection.commit()

                st.success("Atualizações aplicadas com sucesso!")

    elif operation_type == "Adicionar uma coluna":
        new_column_name = st.text_input("Nome da nova coluna:")
        new_column_datatype = st.text_input("Tipo de dado da nova coluna (ex: INT, VARCHAR(255), etc.):")

        if st.button("Adicionar Coluna"):
            alter_table_query = f"ALTER TABLE {selected_table} ADD COLUMN {new_column_name} {new_column_datatype}"
            cursor.execute(alter_table_query)
            connection.commit()

            st.success("Coluna adicionada com sucesso!")

def main():
    build_header()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Viana9802*",
        database="empresa_keila"
    )

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    table_names = [table[0] for table in cursor.fetchall()]
    selected_table = build_filter_controls(table_names)
    build_update_form(selected_table, connection, cursor)

if __name__ == "__main__":
    main()