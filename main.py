import streamlit as st
#from CRUD import create, read, update, delete

st.set_page_config(
    page_title="Página Inicial",
    page_icon="🗂️",
    layout="wide"
)

st.sidebar.title("Menu")

menu_options = ["Página Inicial", "Create", "Read", "Update", "Delete"]
selected_option = st.sidebar.selectbox("Selecione uma operação CRUD:", menu_options)

if selected_option == "Página Inicial": #Essa página ta meio borocoxo, pensei em colocar todas as tabelas do script sabes
    st.title("Página Inicial")
    st.write("Uma abordagem aliando a implementação das operações CRUD, do MySQL, com o Streamlit.")
elif selected_option == "Create":
    create()
elif selected_option == "Read":
    read()
elif selected_option == "Update":
    update()
elif selected_option == "Delete":
    delete()
