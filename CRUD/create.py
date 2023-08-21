import streamlit as st
import mysql.connector

def build_header():
    st.write('<h1>Interface Dinâmica para o BD Empresa‍ 💼</h1>', unsafe_allow_html=True)
    st.write('</p>Realização de operações CRUD no esquema Empresa. Para efetuar quaisquer inserções, é necessário selecionar a tabela desejada e preencher com os dados solicitados, respeitando as regras de integridade provenientes do esquema no MySQL.</p>', unsafe_allow_html=True)

def insert_funcionario(connection, pnome, minicial, unome, cpf, datanasc, endereco, sexo, salario, cpf_supervisor, dnr):
    query = "INSERT INTO funcionario (Pnome, Minicial, Unome, Cpf, Datanasc, Endereco, Sexo, Salario, Cpf_supervisor, Dnr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (pnome, minicial, unome, cpf, datanasc, endereco, sexo, salario, cpf_supervisor, dnr)
    
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    st.success("Dados inseridos na tabela de Funcionários com sucesso!")

def insert_dependentes(connection, fcpf, nome_dependente, sexo, datanasc, parentesco):
    query = "INSERT INTO departamento (Fcpf, Nome_dependente, Sexo, Datanasc, Parentesco) VALUES (%s, %s, %s, %s, %s)"
    values = (fcpf, nome_dependente, sexo, datanasc, parentesco)
    
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    st.success("Dados inseridos na tabela de Departamento com sucesso!")

def insert_departamento(connection, dnome, dnumero, cpf_gerente, data_inicio_gerente):
    query = "INSERT INTO dependentes (Dnome, Dnumero, Cpf_gerente, Data_inicio_gerente) VALUES (%s, %s, %s, %s)"
    values = (dnome, dnumero, cpf_gerente, data_inicio_gerente)
    
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    st.success("Dados inseridos na tabela de Dependentes com sucesso!")

def dnumeros(connection):
    query = "SELECT Dnumero FROM departamento ORDER BY Dnumero ASC"
    cursor = connection.cursor()
    cursor.execute(query)
    dnrs = [row[0] for row in cursor.fetchall()]
    return dnrs


def main():
    build_header()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="engprod25", #Se não houver senha no BD do MySQL, utiliza-se password = ""
        database="empresa_bd"
    )
    st.subheader("Selecione uma tabela do esquema para inserir dados:")
    select = st.radio("", ("Funcionário", "Departamento", "Dependentes"))
    
    if select == "Funcionário":
        st.subheader("Inserção de Funcionário")
        pnome = st.text_input("Primeiro Nome:")
        minicial = st.text_input("Nome do Meio:", placeholder="Somente a letra inicial.")
        unome = st.text_input("Último Nome:")
        cpf = st.text_input("CPF:", placeholder="Formato de 11 digítos, sem traços. Ex: 12345678912")
        datanasc = st.text_input("Data de Nascimento:", placeholder="Ex: 2003-01-09", help="Formato AAAA-MM-DD")
        endereco = st.text_area("Endereço", placeholder="Ex: Rua das Flores, 42, Recife, PE")
        sexo = st.radio("Sexo:", ["M", "F"])
        salario = st.number_input("Salário:", min_value=0)
        cpf_supervisor = st.text_input("CPF do Supervisor:", help="O supervisor deve estar cadastrado como um gerente de departamento.", placeholder="Formato de 11 digítos, sem traços. Ex: 123456789-12")
        unique_dnrs = dnumeros(connection)
        dnr = st.selectbox("DNR:", unique_dnrs, help="Departamento no qual o funcionário será cadastrado.")
    
        if st.button("Cadastrar Funcionário"):
            insert_funcionario(connection, pnome, minicial, unome, cpf, datanasc, endereco, sexo, salario, cpf_supervisor, dnr)
            
    elif select == "Departamento":
        st.subheader("Inserção de Departamento")
        dnome = st.text_input("Nome do Departamento:")
        unique_dnrs = dnumeros(connection)
        dnumero = st.selectbox("Selecione o Número do Departamento:", unique_dnrs)
        cpf_gerente = st.text_input("CPF do Gerente:")
        data_inicio_gerente = st.date_input("Data de Início da Gerência:", value=None, help="Formato AAAA-MM-DD")

        if st.button("Cadastrar Departamento"):
            insert_departamento(connection, dnome, dnumero, cpf_gerente, data_inicio_gerente)

    elif select == "Dependentes":
        st.subheader("Inserção de Dependentes")
        fcpf = st.text_input("CPF do Funcionário:", placeholder="Formato de 11 digítos, sem traços. Ex: 12345678912")
        nome_dependente = st.text_input("Nome do Dependente:")
        sexo = st.radio("Sexo:", ["M", "F"])
        datanasc = st.text_input("Data de Nascimento:", placeholder="Ex: 2003-01-09", help="Formato AAAA-MM-DD")
        parentesco = st.selectbox("Parentesco:", ["Filho", "Filha", "Esposa", "Marido", "Outro(a)"])

        if st.button("Cadastrar Dependente"):
            insert_dependentes(connection, fcpf, nome_dependente, sexo, datanasc, parentesco)

if __name__ == "__main__":
    main()