import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.colors import ListedColormap

RANDOM_STATE = 42


# Fórmula para identificar os outliers automaticamente
def inspect_outliers(datataframe, column, whisker_width=1.5):
    """Função para inspecionar outliers.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    column : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    whisker_width : float, opcional
        Valor considerado para detecção de outliers, por padrão 1.5

    Returns
    -------
    pd.DataFrame
        Dataframe com os outliers.
    """
    q1 = datataframe[column].quantile(0.25)
    q3 = datataframe[column].quantile(0.75)

    iqr = q3 - q1                          
    # iqr: intervale inter-quartile
    # whisker_width --> largura do bigode do boxplot (geralmente é 1.5, mas podemos adotar outros valores)
    lower_bound = q1 - whisker_width * iqr           # intervalo inferior
    upper_bound = q3 + whisker_width * iqr           # intervalo superior

    outliers = datataframe[(datataframe[column] < lower_bound) | (datataframe[column] > upper_bound)]
    
    return outliers

# Fórmula para remover os outliers 
def remove_outliers(datataframe, column, whisker_width=1.5):
    q1 = datataframe[column].quantile(0.25)
    q3 = datataframe[column].quantile(0.75)

    iqr = q3 - q1                          

    lower_bound = q1 - whisker_width * iqr           # intervalo inferior
    upper_bound = q3 + whisker_width * iqr           # intervalo superior

    filtered_dataframe = datataframe[(datataframe[column] > lower_bound) &   (datataframe[column] < upper_bound)]
    
    return filtered_dataframe


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