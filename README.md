Descrição do Trabalho Acadêmico: Pipeline de Dados e Predição de Preço de Veículos com Airflow e Streamlit
Objetivo
O objetivo deste trabalho acadêmico é desenvolver e implementar um pipeline de dados para a predição de preços de veículos, utilizando ferramentas modernas de automação e visualização de dados. O projeto combina Apache Airflow para orquestração de tarefas e Streamlit para a criação de uma interface interativa que permite a previsão de preços de veículos com base em dados históricos.

Componentes Principais
Apache Airflow

Descrição: Apache Airflow é uma plataforma open-source de workflow que permite a programação, monitoramento e gestão de workflows de dados.
Objetivo no Projeto: Automatizar o pipeline de dados, que inclui extração, transformação e carregamento (ETL) dos dados, bem como o treinamento de um modelo de machine learning para prever preços de veículos.
Funcionalidades Implementadas:
Extração: Conectar-se a um banco de dados SQLite e extrair dados sobre veículos.
Transformação: Limpar e transformar os dados extraídos, incluindo a normalização dos preços e ajustes nas variáveis.
Carregamento: Armazenar os dados transformados em um banco de dados SQLite separado.
Treinamento de Modelo: Utilizar um modelo de regressão linear para prever preços de veículos com base em características como ano, tamanho do motor e idade.
Histórico de Treinamento: Registrar o desempenho do modelo e salvar o histórico de treinamento em um arquivo CSV.
Streamlit

Descrição: Streamlit é uma ferramenta open-source para criar aplicativos web interativos de visualização de dados com facilidade e rapidez.
Objetivo no Projeto: Criar uma interface de usuário onde os usuários podem inserir detalhes sobre um veículo e obter uma previsão de seu preço.
Funcionalidades Implementadas:
Interface de Entrada: Permite ao usuário selecionar a marca e o modelo do veículo, além de fornecer informações como ano de fabricação e tamanho do motor.
Predição: Utiliza o modelo treinado para prever o preço do veículo com base nas entradas fornecidas.
Visualização de Dados: Exibe exemplos de dados de veículos armazenados no banco de dados, permitindo aos usuários visualizar informações reais para validação.
Arquitetura do Sistema
Pipeline de Dados com Airflow

O DAG (Directed Acyclic Graph) do Airflow é responsável por coordenar a execução das tarefas de ETL e treinamento do modelo.
O pipeline realiza a extração dos dados do banco de dados de produção, transforma os dados conforme necessário, e carrega os dados transformados em um novo banco de dados.
Após a transformação e carregamento, o modelo é treinado e os resultados do treinamento são armazenados para referência futura.
Aplicação Interativa com Streamlit

A aplicação Streamlit interage com os usuários para coletar informações sobre veículos e apresenta previsões baseadas no modelo treinado.
Exibe dados históricos de veículos armazenados no banco de dados, permitindo aos usuários comparar e validar os preços previstos.
Desafios e Soluções
Desafios de Integração: A integração entre Airflow e Streamlit foi um desafio inicial, especialmente na sincronização dos dados e na validação das previsões. Soluções foram implementadas para garantir que os dados extraídos e transformados pelo Airflow estivessem disponíveis para a aplicação Streamlit.

Preprocessamento de Dados: Houve dificuldades com a padronização e normalização dos dados, que foram resolvidas com ajustes no pipeline de transformação e no treinamento do modelo.

Predição de Preços: Problemas com a precisão das previsões foram abordados revisando o pré-processamento dos dados e ajustando os hiperparâmetros do modelo de regressão linear.

Conclusão
Este trabalho demonstra a eficácia da integração de ferramentas modernas como Apache Airflow e Streamlit para criar soluções robustas de gerenciamento de dados e visualização. O pipeline de dados automatizado e a interface interativa fornecem uma base sólida para futuras extensões e melhorias na previsão de preços e na análise de dados de veículos.
