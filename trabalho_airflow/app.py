import streamlit as st
import pandas as pd
import joblib
import sqlite3
from sklearn.preprocessing import StandardScaler

# Configurações dos caminhos
model_path = 'trabalho_airflow/modelo/car_price_model.pkl'
scaler_path = 'trabalho_airflow/modelo/scaler.pkl'
db_path = 'trabalho_airflow/data/carsAd.db'

# Carregando o modelo treinado e o scaler
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Função para obter marcas e modelos do banco de dados
def get_brands_and_models():
    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(db_path)
        
        # Consultar marcas
        query_brands = "SELECT DISTINCT Make FROM cars"
        df_brands = pd.read_sql_query(query_brands, conn)
        brands = df_brands['Make'].tolist()
        
        # Consultar modelos
        query_models = "SELECT DISTINCT Model FROM cars"
        df_models = pd.read_sql_query(query_models, conn)
        models = df_models['Model'].tolist()
        
    except Exception as e:
        st.error(f"Erro ao carregar dados do banco de dados: {e}")
        brands = []
        models = []
    
    finally:
        if conn:
            conn.close()
    
    return brands, models

# Obter marcas e modelos
marcas, modelos = get_brands_and_models()

# Dicionário para modelos por marca
marcas_modelos = {}
if marcas:
    for marca in marcas:
        # Consultar modelos para cada marca
        try:
            conn = sqlite3.connect(db_path)
            query_models_by_brand = f"SELECT DISTINCT Model FROM cars WHERE Make = '{marca}'"
            df_models_by_brand = pd.read_sql_query(query_models_by_brand, conn)
            modelos_para_marca = df_models_by_brand['Model'].tolist()
            marcas_modelos[marca] = modelos_para_marca
        except Exception as e:
            st.error(f"Erro ao carregar modelos para a marca {marca}: {e}")
        finally:
            if conn:
                conn.close()

# Título do aplicativo
st.title("Predição de Preço de Veículos")

# Subtítulo
st.markdown("Preencha os detalhes abaixo para prever o preço de um veículo.")

# Entrada dos dados
st.sidebar.subheader("Defina os atributos do veículo")
# Seleção da marca
make = st.sidebar.selectbox("Marca do Veículo", marcas)
# Filtragem dos modelos com base na marca selecionada
modelos_disponiveis = marcas_modelos.get(make, [])
# Seleção do modelo
selected_model = st.sidebar.selectbox("Modelo do Veículo", modelos_disponiveis)
# Entrada de outros atributos
Age = st.sidebar.number_input("Idade do Automóvel",min_value=0, max_value=10, value=0)
year = st.sidebar.number_input("Ano", min_value=2010, max_value=2020, value=2010)
engine_size = st.sidebar.number_input("Tamanho do Motor (L)", min_value=1.0, value=1.0, step=0.1, format="%.1f")
fuel_type = st.sidebar.selectbox("Tipo de Combustível", ["Petrol", "Diesel", "Hybrid", "Electric"])

# Mapeamento de Fuel Type para valores numéricos
fuel_mapping = {"Petrol": 1, "Diesel": 2, "Hybrid": 3, "Electric": 4}
fuel_type_num = fuel_mapping.get(fuel_type, 0)

# Botão para realizar a predição
if st.sidebar.button("Realizar Predição"):
    # Preparando os dados para a predição
    data_teste = pd.DataFrame({
        "Year": [int(year)], 
        "Engine Size (L)": [engine_size],
        "Age": [2020 - int(year)] 
    })
    
    # Normalizar os dados
    data_teste_scaled = scaler.transform(data_teste)

    # Realizando a predição
    try:
        prediction_result = model.predict(data_teste_scaled)
        st.subheader("O preço previsto para o veículo é:")
        st.write(f"USD {prediction_result[0]:,.2f}") 
    except Exception as e:
        st.error(f"Erro na predição: {e}")

# Exibindo exemplos de dados do banco de dados local
st.subheader("Exemplo de Dados de Veículos")

try:
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    
    # Consulta SQL com nomes de colunas devidamente delimitados
    query = "SELECT * FROM cars"
    # Executar a consulta e ler os dados em um DataFrame
    df_example = pd.read_sql_query(query, conn)
    
    # Mostrar o DataFrame usando Streamlit
    st.write(df_example)
    
except Exception as e:
    # Exibir mensagem de erro em caso de falha
    st.error(f"Erro ao carregar dados do banco de dados: {e}")
    
finally:
    # Garantir que a conexão seja fechada, mesmo em caso de erro
    if conn:
        conn.close()
