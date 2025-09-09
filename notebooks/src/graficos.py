import os
os.environ["OMP_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from matplotlib.colors import ListedColormap
from matplotlib.ticker import PercentFormatter


PALETTE = "coolwarm"
SCATTER_ALPHA = 0.2



def grafico_elbow_silhouette(X, random_state=42, intervalo_k=(2, 11)):
    """Gera os gráficos para os métodos Elbow e Silhouette.

    Parameters
    ----------
    X : pandas.DataFrame
        Dataframe com os dados.
    random_state : int, opcional
        Valor para fixar o estado aleatório para reprodutibilidade, por padrão 42
    range_k : tuple, opcional
        Intervalo de valores de cluster, por padrão (2, 11)
    """
    
    # OBS: O "X" precisa ser um dataframe só com valores numéricos, colunas categóricas precisam ter passado por preprocessamento.

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,5), tight_layout=True)

    elbow = {}
    silhouette = []

    k_range = range(*intervalo_k)

    for numero in k_range:
        kmeans = KMeans(n_clusters=numero, n_init= 10, random_state=random_state)
        kmeans.fit(X)         

        elbow[numero] = kmeans.inertia_      # inertia_ : soma da distância quadrada de cada ponto para o centroide de seu cluster
        labels = kmeans.labels_              # labels_: nome de cada cluster
        
        silhouette.append(silhouette_score(X, labels))       
        # silhouete_score: dentro de cada cluster ele calcula a distância média de cada ponto, e compara com a distânia do ponto pro cluster mais próximo que ele não pertence
        # silhouete_score: varia de -1 a 1, quanto maior melhor, mais bem dividido estão os clusters. Valor igual a 0 quer dizer que o ponto está na distancia igual entre o centro de 2 cluster
        # silhouette_score(kmeans.transform(X)): pra calcular esse score o X precisa estar transformado pelas etapas de preprocessamento do kmeans 

    # OBS: lineplot precisa dos valores em formato de lista
    sns.lineplot( x = list(elbow.keys()), y = list(elbow.values()), ax=ax[0], marker='o')
    ax[0].set_title('Elbow Method')
    ax[0].set_xlabel('K')
    ax[0].set_ylabel('Inertia')

    sns.lineplot( x = list(k_range), y = silhouette, ax=ax[1], marker='o')
    ax[1].set_title('Silhouette Method')
    ax[1].set_xlabel('K')
    ax[1].set_ylabel('Silhouette Score')

    fig.suptitle('Definição do número de Clusters', fontsize=15, fontweight='bold')

    plt.show()



def pairplot(dataframe, columns, hue_column=None, alpha=0.5, corner=True):
    """Função para gerar pairplot.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    hue_column : str, opcional
        Coluna utilizada para hue, por padrão None
    alpha : float, opcional
        Valor de alfa para transparência, por padrão 0.5
    corner : bool, opcional
        Se o pairplot terá apenas a diagonal inferior ou será completo, por padrão True
    palette : str, opcional
        Paleta a ser utilizada, por padrão "tab10"
    """

    analysis=columns.copy() + [hue_column]
    
    sns.pairplot(
        dataframe[analysis], 
        diag_kind='kde', 
        hue=hue_column, 
        plot_kws=dict(alpha=alpha),
        corner=corner
    )



def plot_columns_percent_by_cluster(
        dataframe,
        columns,
        column_cluster='cluster',
        rows_cols=(2,3),
        figsize=(15, 8),
        palette='tab10'
):
    """Função para plotar como está a distribuição percentual das variáveis de cada feature dentro de cada cluster.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    column_cluster : str, opcional
        Coluna utilizada para cluster, por padrão 'cluster'
    rows_cols : Tuple[int, int], opcional
        Tupla com o número de linhas e colunas do grid de subplots, por padrão (2, 3)
    figsize : Tuple[int, int], opcional
        Tamanho da figura, por padrão (15, 8)
    palette : str, opcional
        Paleta a ser utilizada, por padrão 'tab10'
    """

    fig, axs = plt.subplots(nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True)

    if axs is not isinstance(axs, np.ndarray):  # Verifica se axs é um array numpy ---> método para ser usado caso queiramos gerar apenas 1 gráfico (1,1)
        axs = np.array(axs)                     # Se não for, converte para um array numpy de um único elemento 

    for ax, coluna in zip(axs.flatten(), columns):
        h = sns.histplot(x=column_cluster, hue=coluna, data=dataframe, ax=ax, multiple='fill', stat='percent', discrete=True, shrink=0.8, palette=palette)

        n_clusters = dataframe[column_cluster].nunique()      # Pra pegar automaticamente uma lista com o número dos clusters
        h.set_xticks(range(n_clusters))                       # Define os ticks do eixo X como o número de clusters (para não ficar com valores float, como 0.5, 1.0, 1.5 ...)
        h.yaxis.set_major_formatter(PercentFormatter(1))      # Formata o eixo Y para mostrar porcentagens de 0 a 1
        h.set_ylabel("")                                      # Remove o rótulo do eixo Y, pois já está formatado como porcentagem
        h.tick_params(axis='both', which='both', length=0)    # Remove os ticks dos eixos X e Y para deixar o gráfico mais limpo

        for bars in h.containers:
            h.bar_label(bars, label_type='center', labels=[f'{b.get_height():.1%}' for b in bars], color='white', weight='bold', fontsize=10)

        for bar in h.patches:                                 # Remove as bordas das barras para deixar o gráfico mais limpo
            bar.set_linewidth(0)

    plt.subplots_adjust(wspace=0.25)                          # Para controlar o espaçamento entre os gráficos (mas precisa tirar o tight_layout)

    # multiple = 'fill' para mostrar as barras empilhadas,
    # stat='percent' para mostrar a porcentagem de cada categoria dentro de cada barra
    # discrete=True para as barras sem interpolações (o que acaba unindo elas se não não usarmos shrink)
    # shrink=0.8 para dar um pequeno espaçamento entre uma barra e outras



def plot_columns_percent_hue_cluster(
        dataframe,
        columns,
        column_cluster='cluster',
        rows_cols=(2,3),
        figsize=(15, 8),
        palette='tab10'
):
    """Função para plotar o percentual de cada cluster para as variáveis de cada features em análise.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    column_cluster : str, opcional
        Coluna utilizada para cluster, por padrão 'cluster'
    rows_cols : Tuple[int, int], opcional
        Tupla com o número de linhas e colunas do grid de subplots, por padrão (2, 3)
    figsize : Tuple[int, int], opcional
        Tamanho da figura, por padrão (15, 8)
    palette : str, opcional
        Paleta a ser utilizada, por padrão 'tab10'
    """
    
    fig, axs = plt.subplots(nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True)

    if axs is not isinstance(axs, np.ndarray):  # Verifica se axs é um array numpy ---> método para ser usado caso queiramos gerar apenas 1 gráfico (1,1)
        axs = np.array(axs)                     # Se não for, converte para um array numpy de um único elemento 

    for ax, coluna in zip(axs.flatten(), columns):
        h = sns.histplot(x=coluna, hue=column_cluster, data=dataframe, ax=ax, multiple='fill', stat='percent', discrete=True, shrink=0.8, palette=palette)

        if dataframe[coluna].dtype != 'object':
            h.set_xticks(range(dataframe[coluna].nunique()))  # Define os ticks do eixo X conforme as entradas unicas da coluna

        h.yaxis.set_major_formatter(PercentFormatter(1))         # Formata o eixo Y para mostrar porcentagens de 0 a 1
        h.set_ylabel("")                                         # Remove o rótulo do eixo Y, pois já está formatado como porcentagem
        h.tick_params(axis='both', which='both', length=0)       # Remove os ticks dos eixos X e Y para deixar o gráfico mais limpo

        for bars in h.containers:
            h.bar_label(bars, label_type='center', labels=[f'{b.get_height():.1%}' for b in bars], color='white', weight='bold', fontsize=10)

        for bar in h.patches:                                   # Remove as bordas das barras para deixar o gráfico mais limpo
            bar.set_linewidth(0)

        legend = h.get_legend()                                 # Pegando a legenda do gráfico
        legend.remove()                                         # Removendo a legenda de cada gráfico

    labels = [text.get_text() for text in legend.get_texts()]      # Para pegar os textos da legenda e atribuindo a variável labels
    fig.legend(handles=legend.legend_handles, labels=labels, loc='upper center', ncol=dataframe[column_cluster].nunique(), title='Clusters')  # Adicionando a legenda no gráfico

    plt.subplots_adjust(wspace=0.25, hspace=0.25)                        # Para controlar o espaçamento entre os gráficos (mas precisa tirar o tight_layout)

    # multiple = 'fill' para mostrar as barras empilhadas,
    # stat='percent' para mostrar a porcentagem de cada categoria dentro de cada barra
    # discrete=True para as barras sem interpolações (o que acaba unindo elas se não não usarmos shrink)
    # shrink=0.8 para dar um pequeno espaçamento entre uma barra e outras



def visualizar_clusters_3d(
    dataframe,                       # Precisamos passar o dataframe preprocessado, pois os centroides foram calculados em cima desse dataframe preprocessado
    colunas,                         # Informar em formato de lista, e o nome delas precisa ter o prefixo do preprocessamento 'one_hot_coluna' ou 'standard_coluna'
    quantidade_cores_clusters,       # Vai ser sempre igual a quantidade de clusters (e não das colunas)
    centroids,                       # Esse parametro deve ser fornecido, e pode ter apenas os centroides das colunas que serão exibidas no gráfico
    mostrar_centroids=True, 
    mostrar_pontos=False,            # Se for usado o parametro igual a True, precisa ser fornecido a 'coluna_cluster' abaixo
    coluna_clusters=None,            # Esse dataframe['coluna_cluster'] não precisa ser o mesmo df_preprocessado do 1º parametro, pode ser o df_clustered['cluster']
):

    fig = plt.figure()
    
    ax = fig.add_subplot(111, projection="3d")
    
    cores = plt.cm.tab10.colors[:quantidade_cores_clusters]
    cores = ListedColormap(cores)
    
    x = dataframe[colunas[0]]
    y = dataframe[colunas[1]]
    z = dataframe[colunas[2]]
    
    ligar_centroids = mostrar_centroids
    ligar_pontos = mostrar_pontos
    
    for i, centroid in enumerate(centroids):
        if ligar_centroids: 
            ax.scatter(*centroid, s=500, alpha=0.5)
            ax.text(*centroid, f"{i}", fontsize=20, horizontalalignment="center", verticalalignment="center")
    
        if ligar_pontos:
            s = ax.scatter(x, y, z, c=coluna_clusters, cmap=cores)
            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.3, 1))
    
    ax.set_xlabel(colunas[0])
    ax.set_ylabel(colunas[1])
    ax.set_zlabel(colunas[2])
    ax.set_title("Clusters")
    
    plt.show()


def plot_clusters_2D(
    dataframe,
    columns,
    n_colors,
    centroids,
    show_centroids=True,
    show_points=False,
    column_clusters=None,
):
    """Gerar gráfico 2D com os clusters.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    n_colors : int
        Número de cores para o gráfico.
    centroids : np.ndarray
        Array com os centroides.
    show_centroids : bool, opcional
        Se o gráfico irá mostrar os centroides ou não, por padrão True
    show_points : bool, opcional
        Se o gráfico irá mostrar os pontos ou não, por padrão False
    column_clusters : List[int], opcional
        Coluna com os números dos clusters para colorir os pontos
        (caso mostrar_pontos seja True), por padrão None
    """

    fig = plt.figure()

    ax = fig.add_subplot(111)

    cores = plt.cm.tab10.colors[:n_colors]
    cores = ListedColormap(cores)

    x = dataframe[columns[0]]
    y = dataframe[columns[1]]

    ligar_centroids = show_centroids
    ligar_pontos = show_points

    for i, centroid in enumerate(centroids):
        if ligar_centroids:
            ax.scatter(*centroid, s=500, alpha=0.5)
            ax.text(
                *centroid,
                f"{i}",
                fontsize=20,
                horizontalalignment="center",
                verticalalignment="center",
            )

        if ligar_pontos:
            s = ax.scatter(x, y, c=column_clusters, cmap=cores)
            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.3, 1))

    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_title("Clusters")

    plt.show()



def plot_coeficientes(df_coefs, tituto="Coeficientes"):
    df_coefs.plot.barh(figsize=(10, 15))
    plt.title(tituto)
    plt.axvline(x=0, color=".5")
    plt.xlabel("Coeficientes")
    plt.gca().get_legend().remove()
    plt.show()



def plot_comparar_metricas_modelos(df_resultados):
    fig, axs = plt.subplots(4, 2, figsize=(9, 9), sharex=True)

    comparar_metricas = [
        "time_seconds",
        "test_accuracy",
        "test_balanced_accuracy",
        "test_f1",
        "test_precision",
        "test_recall",
        "test_roc_auc",
        "test_average_precision",
    ]

    nomes_metricas = [
        "Tempo (s)",
        "Acurácia",
        "Acurácia balanceada",
        "F1",
        "Precisão",
        "Recall",
        "AUROC",
        "AUPRC",
    ]

    for ax, metrica, nome in zip(axs.flatten(), comparar_metricas, nomes_metricas):
        sns.boxplot(
            x="model",
            y=metrica,
            data=df_resultados,
            ax=ax,
            showmeans=True,
        )
        ax.set_title(nome)
        ax.set_ylabel(nome)
        ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()

    plt.show()
