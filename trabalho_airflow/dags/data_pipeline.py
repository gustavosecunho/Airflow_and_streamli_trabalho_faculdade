from airflow import DAG  
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd 
import sqlite3
import os
import logging
from datetime import timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Configurações padrão do DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Caminhos para os arquivos
path = "/home/gustavo/Documentos/trabalho_airflow/data"
path_db_producao = os.path.join(path, "carsProd.db")
path_csv_tempora = os.path.join(path, "cars.csv")
path_db_saida = os.path.join(path, "carsAd.db")
path_model = os.path.join(path, "/home/gustavo/Documentos/trabalho_airflow/modelo/car_price_model.pkl")
path_scaler = os.path.join(path, "/home/gustavo/Documentos/trabalho_airflow/modelo/scaler.pkl")
path_csv_treino = os.path.join(path, "training_history.csv")

# Verifica a existência do banco de dados de produção
if not os.path.exists(path_db_producao):
    raise FileNotFoundError(f"Banco de dados de produção não encontrado: {path_db_producao}")

if not os.path.exists(path):
    os.makedirs(path)

dag = DAG(
    dag_id='data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)


def _extract():
    try:
        logging.info("Iniciando extração de dados.")
        conn = sqlite3.connect(path_db_producao)
        
        query = """SELECT * FROM cars """
        df = pd.read_sql_query(query, conn)
        
        # Salva o DataFrame em um arquivo CSV
        df.to_csv(path_csv_tempora, index=False)
        
        logging.info("Extração concluída com sucesso.")
    except Exception as e:
        logging.error(f"Erro na extração: {e}")
    finally:
        if conn:
            conn.close()

def _transform():
    try:
        logging.info("Iniciando transformação de dados.")
        df = pd.read_csv(path_csv_tempora)
        df['Price (USD)'] = df['Price (USD)'].replace('[\$,]', '', regex=True).astype(float)
        df['Make'] = df['Make'].str.title()
        df['Engine Size (L)'] = df['Engine Size (L)'].astype(float)
        df['Age'] = 2020 - df['Year']
        df.to_csv(path_csv_tempora, index=False)
        logging.info("Transformação concluída com sucesso.")
    except Exception as e:
        logging.error(f"Erro na transformação: {e}")

def _load():
    try:
        logging.info("Iniciando carregamento de dados.")
        conn = sqlite3.connect(path_db_saida)
        df = pd.read_csv(path_csv_tempora)
        df.to_sql("cars", conn, if_exists="replace", index=False)
        logging.info("Carregamento concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro no carregamento: {e}")
    finally:
        conn.close()


def _create_training_history_csv():
    if not os.path.exists(path_csv_treino):
        logging.info("Criando arquivo de histórico de treinamento.")
        df = pd.DataFrame(columns=['model_name', 'mean_absolute_error', 'mean_squared_error', 'r2_score', 'training_date'])
        df.to_csv(path_csv_treino, index=False)
        logging.info("Arquivo de histórico de treinamento criado com sucesso.")

def _train_model():
    try:
        logging.info("Iniciando treinamento do modelo.")
        # Carregar dados para treinamento
        df = pd.read_csv(path_csv_tempora)
        
        # Seleção de recursos e variável alvo
        X = df[['Year', 'Engine Size (L)', 'Age']]
        y = df['Price (USD)']
        
        # Dividir os dados em conjuntos de treinamento e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Padronizar os recursos
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Treinar o modelo
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        # Fazer previsões
        y_pred = model.predict(X_test_scaled)
        
        # Avaliar o modelo
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logging.info(f'Mean Absolute Error: {mae}')
        logging.info(f'Mean Squared Error: {mse}')
        logging.info(f'R-squared: {r2}')
        
        # Salvar o modelo e o scaler
        joblib.dump(model, path_model)
        joblib.dump(scaler, path_scaler)

        # Salvar o histórico de treinamento no arquivo CSV
        df_history = pd.DataFrame({
            'model_name': ['Linear Regression'],
            'mean_absolute_error': [mae],
            'mean_squared_error': [mse],
            'r2_score': [r2],
            'training_date': [pd.Timestamp.now()]
        })
        
        if os.path.exists(path_csv_treino):
            df_existing = pd.read_csv(path_csv_treino)
            df_combined = pd.concat([df_existing, df_history], ignore_index=True)
            df_combined.to_csv(path_csv_treino, index=False)
        else:
            df_history.to_csv(path_csv_treino, index=False)
        
        logging.info("Treinamento do modelo concluído com sucesso e histórico salvo.")
    except Exception as e:
        logging.error(f"Erro no treinamento do modelo: {e}")

# Definição das tarefas do DAG
create_training_history_csv_task = PythonOperator(
    task_id='create_training_history_csv',
    python_callable=_create_training_history_csv,
    dag=dag,
)
extract_task = PythonOperator(
    task_id='extract',
    python_callable=_extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=_transform,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=_load,
    dag=dag,
)
train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=_train_model,
    dag=dag,
)

# Definição da ordem das tarefas
create_training_history_csv_task >> extract_task >> transform_task >> load_task >> train_model_task