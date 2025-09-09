# Case iFood - Analista de dados

O atual projeto foi parte de um processo seletivo da empresa iFood, que forneceu um conjunto de dados que simula metainformações sobre o cliente e as interações da campanha iFood com esse cliente.

É seu desafio entender os dados, encontrar oportunidades e insights de negócios e propor qualquer ação orientada por dados para otimizar os resultados das campanhas e gerar valor para a empresa.

## A Empresa do Projeto

- Empresa consolidada no setor de varejo de alimentos, com milhares de clientes e atendendo cerca de um milhão de consumidores anualmente. 
- Vende produtos de cinco categorias principais: vinhos, carnes, frutas exóticas, peixes e doces. Os produtos podem ser classificados como gold ou regulares. Os canais de vendas incluem: lojas físicas, catálogos e site da empresa.
- Opera globalmente com receitas estáveis nos últimos três anos, mas com perspectivas de crescimento de lucros desfavoráveis para o futuro próximo, e está tomando algumas iniciativas de marketing para inverter essa situaçaõ
   
## Principais Objetivos

- Melhorar o desempenho das atividades de marketing, focando em campanhas mais eficazes. O departamento de marketing busca uma abordagem mais quantitativa para a tomada de decisões.
- Construir um modelo preditivo para a próxima campanha de marketing direto, com o objetivo de maximizar o lucro.
- A campanha piloto teve um prejuízo de -3.046MU, com uma taxa de sucesso de 15%. O objetivo é reverter esse cenário na próxima campanha, e também identificar as características dos clientes mais propensos a comprar para otimizar as campanhas futuras.

## Entregáveis do Projeto

1. Explorar os dados - ser criativo e prestar atenção aos detalhes. Fornecer para a equipe de marketing uma melhor compreensão das características dos respondentes;
2. Criar e descrever uma segmentação de clientes com base no comportamento dos clientes;
3. Criar e descreva um modelo preditivo (classificação) que permita à empresa maximizar o lucro da próxima campanha de marketing.

## Execução do Projeto

As informações abaixo demonstrarão como esse projeto foi executado, trazendo a metodologia e observações importantes usadas / obtidas em cada uma das etapas solicitadas nos entregáveis do projeto. 

### 1) Análise Exploratória

Num primeiro momento para ter maior compreensão da base de dados foi utilizado a biblioteca **YDataProfiling** para obter um relatório pronto, que pode ser visto através do arquivo [EDA_Case_iFood.html](relatorios/EDA_Case_iFood.html) (obs: devido tamanho do arquivo a previsualização não está disponível, sendo necessário fazer download para visualizar)

Posteriormente segui com a análise manual para realizar o tratamento da base de dados, eliminando alguns dados nulos, eliminando alguns outliers, e realizando o processo de *Feature Engineering* para criar variáveis que possam ser úteis para os modelos de segmentação de clientes e de classificação.

Diversas análises gráficas foram feitas e podem ser vistas através do notebook [EDA_Principal](notebooks/01_EDA_principal.ipynb). 

Um dos gráficos mais úteis dessa etapa são as correlações das features com a variável 'Response', que demonstra quais clientes responderam positivamente à campanha de marketing piloto

<div align="center"> <img src="relatorios/Correlacao das Features com Response.png" title="Correlações " height="500"/> </div>


### 2) Segmentação dos Clientes - Clusters

O notebook para essa etapa do projeto pode ser encontrado através do link [Segmentação dos Clientes](notebooks/02.Clusterizacao_clientes_sem_PCA.ipynb)

Os dados tratados da análise exploratória passaram por etapas de **preprocessamento**, como *One_Hot_Encoder, StandardScaler, PowerTransform e MinMaxScaler* para ajuste e normalização de escala, a fim de melhorar os resultados dos modelos de segmentação de clientes. 

Através do ‘Silhouette Method’ e ‘Elbow Method’ foi definido que a segmentação dos clientes ocorreria em **3 Clusters**, conforme análise dos gráficos abaixo

<div align="center"> <img src="relatorios/Elbow and Silhouette Method.png" title="Elbow e Silhouette Method " height="700"/> </div>

Com o modelo **KMeans** segmentamos os clientes em 3 clusters.

A maioria dos clientes de cada cluster tem perfil conforme a tabela abaixo:

| Renda   | Padrão de Gasto / Consumo| Filhos em casa?  | Propensão à comprar após campanhas de marketing | % Resposta Campanha Piloto | Cluster |
|---------|--------------------------|------------------|-------------------------------------------------|----------------------------|---------|
| Alta    | Alto                     | Provavelmente Não| Um pouco maior                                  | 29%                        | 0       |
| Baixa   | Baixo                    | Provavelmente Sim| Geralmente não                                  | 9%                         | 1       |
| Mediana | Mediano (variando)       | Provavelmente Sim| Menor                                           | 11%                        | 2       |

Para maior detalhamento da segmentação dos clientes em cada feature, os links a seguir demonstram a segmentação dos clientes para as [Segmentação - Features Numéricas](relatorios/Separacao%20dos%20Clusters%20-%20Boxplot%20para%20features%20numericas.png) e [Segmentação - Features Categóricas](relatorios/Separacao%20dos%20Clusters%20-%20Histograma%20para%20features%20categoricas.png)
 
Os base de dados original do projeto, após passar pelo tratamento dos dados e a segmentação dos clientes em cada clusters, foi extraída com o nome ‘customers_clustered.csv’ e está na pasta ‘./dados’


### 3) Modelo Preditivo - Classificação

O notebook para essa etapa do projeto pode ser encontrado através do link [Modelo de Classificação](notebooks/03.Modelo_classificacao_campanha_marketingipynb)

Para **Seleção de Features** foi dotado os **Testes Estatísticos** de *Mann-Whitneyu e Qui-Quadrado* para eliminar features que não influenciavam a coluna ‘Response’ referente a campanha de marketing piloto. Posteriormente foi aplicado as mesmas etapas de *preprocessamento* dos dados descritas na etapa de segmentação de clientes acima. 

Diversos **Modelos de Classificação** - como *LogisticRegression, DecisionTreeClassifier, XGBClassifier, LGBMClassifier, SVC, KNeighborsClassifier* -  foram treinados e submetidos à validação cruzada para avaliar seus resultados em métricas como recall, precisão, acurácia, área de baixo da curva ROC e curva precisão-recall

**Métricas** - Nessa aplicação é pior não oferecer a campanha para um possível comprador, do que oferecer pra alguém que não vai comprar. Portanto, para esse problema o *recall* é mais importante que a precisão. Mas também é bom ter um balanço de precisão e recall para não gastar dinheiro excessivamente nas campanhas de marketing com clientes que não serão influenciados pela campanha, então a métrica *average_precision* também deve ser levada em consideração para escolha do melhor modelo.

Baseado nessas métricas o modelo que apresentou melhores resultados foi o **LogisticRegression**, que ainda foi otimizado através do *GridSearch* com grade de parâmetros para maximizar ‘recall’. Para esse modelo otimizado, foi analizado os coeficientes da regressão para entender quais features tem maior influencia (positiva e negativa) na variável alvo ‘Response’ referente à taxa de resposta das campanhas de marketing. O gráfico dos coeficientes de cada feature pode ser visto abaixo:

<div align="center"> <img src="relatorios/Coeficientes do modelo regressao logistica.png" title="Coeficientes " height="700"/> </div>

Baseado nas features acima, o perfil de cliente que deverá ter o direcionamento de marketing da próxima campanha segue as características abaixo:
- Clientes que aceitaram campanhas de marketing anteriores (mais propensos a aceitar a próxima campanha)
- Clientes antigos (cadastrados na base de dados a mais tempo - DaysSinceEnrolled)
- Preferência por clientes solteiros do que com algum parceiro.
- Clientes que não estão a muitos dias sem fazer compras (Recency)
- Clientes que compram mais no site da empresa ou conforme catálogo, e não tanto na loja.
- Clientes que preferem comprar mais carnes e não tanto vinhos
- Clientes com maiores níveis educacionais (PHD), evitar clientes com educação básica apenas

A **Matriz de Confusão** do modelo de classificação otimizado obtido nesse projeto pode ser vista na imagem abaixo.

<div align="center"> <img src="relatorios/Matriz de confusao.png" title="Matriz de Confusao " height="300"/> </div>

### **Estimando o ROI - Retorno do Investimento**

Baseado na campanha piloto aplicada em 2240 clientes, que teve custo de 6.720MU e receita de 3.674MU concluímos que:
- Custo por cliente da campanha piloto: 3037,97
- Receita por cliente da campanha piloto: 11033,03

Aplicando esses dados de custo e receita da campanha piloto por cliente, nos resultados obtidos conforme a matriz de confusão acima, também podemos estimar o custo, receita e ROI bruto e percentual da próxima campanha de marketing utilizando o modelo preditivo criado nesse projeto.

CAMPANHA                     | GASTO    | RECEITA  | ROI BRUTO   | ROI (%)
-----------------------------|----------|----------|------------ |---------
Piloto                       | 6.720MU  | 3.674MU  |-3.046MU 🔴  | - 45% 🔴 
Previsão da Próxima Campanha | 18.136MU | 31.113MU | 12.976MU 🟢 | 72% 🟢

**Conclusão**: com esse projeto de ciência dos dados conseguimos sair de uma campanha piloto com 45% de prejuízo para um modelo cuja previsão é gerar um ROI referente à 72% de lucro sobre o investimento da campanha de marketing.


### Apresentação Resumida do Projeto

Como foi solicitado nos entregáveis do projeto, foi criado uma apresentação Power Point com as informações resumidas do projeto. 

Esse arquivo está no diretório principal e pode ser obtido através do link [Apresentação_Projeto.pptx](Apresentacao_Projeto.pptx) (devido tamanho do arquivo a pré-visualização não está disponível, sendo necessário fazer o download do arquivo para acessá-lo).

-----------------------------------------------------------------------------------------------------------------------------------------

## Organização de pastas do projeto

```
├── .env                        <- Arquivo de variáveis de ambiente (não versionar)
├── .gitignore                  <- Arquivos e diretórios a serem ignorados pelo Git
├── ambiente.yml                <- O arquivo de requisitos para reproduzir o ambiente de análise
├── LICENSE                     <- Licença de código aberto se uma for escolhida
├── README.md                   <- README principal para desenvolvedores que usam este projeto.
├── Apresentacao_Projeto.pptx   <- Apresentação do Power Point com resumo do projeto.
|
├── dados              <- Arquivos de dados para o projeto.
|
├── modelos            <- Modelos treinados e otimizado durante o projeto para uso posterior
|
├── notebooks          <- Cadernos Jupyter onde foi desenvolvido o projeto.
│
|   └──src             <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      └── "arquivos".py  <- Demais Scripts contendo funções para obter graficos, treinar e testar modelos, analisar métricas, remover outliers, ete
|
├── relatorios         <- Análises geradas em HTML, PDF, gráficos e figuras gerados para serem usados em relatórios
|
├── referencias        <- Pasta onde está o dicionário de dados do projeto
