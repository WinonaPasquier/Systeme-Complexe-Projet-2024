import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import scipy.stats as stats
from scipy.stats import spearmanr



def loadGraph(file):
    """charger un graphe à partir d'un fichier
    file: nom du fichier contenant le graphe"""
    with open(file, 'r') as f:
        lignes = f.readlines()
        # La première ligne -> nombre de nœuds
        nbNodes = int(lignes[0].strip())
        # Les lignes suivantes -> les arêtes
        edges = [tuple(map(int, ligne.strip().split())) for ligne in lignes[1:]]
    # graphe non orienté
    graphe = nx.Graph()
    # Ajouter les nœuds et les arêtes
    graphe.add_nodes_from(range(nbNodes))
    graphe.add_edges_from(edges)
    return graphe

def getNumberOfNodesAndEdges(graph):
    """Récupérer le nombre de sommets et d'arêtes du graphe
    graph: graphe"""
    nbNodes = len(graph.nodes())
    nbEdges = len(graph.edges())
    return nbNodes, nbEdges

def computeDensity(graphe):
    """Calculer la densité du graphe
    graphe: graphe"""
    return nx.density(graphe)

def degreMoyen(graphe):
    """Calculer le degré moyen du graphe
    graphe: graphe"""
    return sum(dict(graphe.degree()).values()) / len(graphe.nodes())

def numberTriangles(graphe):
    """Calculer le nombre de triangles dans le graphe
    graphe: graphe"""
    return sum(nx.triangles(graphe).values()) // 3

def globalClustering(graph):
    """Calculer le coefficient de clustering global du graphe
    graph: graphe"""
    return nx.average_clustering(graph)

def localCustering(graph):
    """Calculer le coefficient de clustering local de chaque noeud du graphe
    graph: graphe"""
    return nx.clustering(graph)

def averageShortestPathLength(graphe):
    """Calculer la distance moyenne entre deux sommets du graphe
    graphe: graphe"""
    return nx.average_shortest_path_length(graphe)

def graphDiameter(graphe):
    """Calculer le diamètre du graphe
    graphe: graphe"""
    return nx.diameter(graphe)

def approximateDiameter(graphe, nbSamples=1000):
    """Calculer le diamètre approximatif du graphe
    graphe: graphe
    nbSamples: nombre de noeuds à échantillonner"""
    nodes = list(graphe.nodes())
    sampledNodes = random.sample(nodes, nbSamples)

    diameter = 0
    # Pour chaque noeud calculer distance max au autres noeuds
    for node in sampledNodes:
        lengths = nx.single_source_shortest_path_length(graphe, node)
        maxLength = max(lengths.values())
        if maxLength > diameter:
            diameter = maxLength

    return diameter

def approximateAverageDistance(graphe, nbSamples=1000):
    """Calculer la distance moyenne approximative entre deux sommets du graphe
    graphe: graphe
    nbSamples: nombre de noeuds à échantillonner"""
    nodes = list(graphe.nodes())
    sampled_nodes = random.sample(nodes, nbSamples)
    totalDist = 0
    totalPairs = 0
    for node in sampled_nodes:
        lengths = nx.single_source_shortest_path_length(graphe, node)
        totalDist += sum(lengths.values())
        totalPairs += len(lengths)

    return totalDist / totalPairs

def plotDegreeDistribution(graph):
    """afficher la distribution des degrés en lin-lin et log-log
    graph: graphe"""
    degrees = dict(graph.degree())
    degreeVals = sorted(set(degrees.values()))
    hist = [list(degrees.values()).count(value) for value in degreeVals]
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,5))
    fig.suptitle('Distribution des degrés')

    ax1.scatter(degreeVals, hist, marker='o',color = 'green')
    ax1.set_xlabel('Degré(lin)')
    ax1.set_ylabel('Fréquence(lin)')
    ax1.set_title('Echelle lin-lin')

    ax2.scatter(degreeVals, hist, marker='o',color = 'orange')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Degré (log)')
    ax2.set_ylabel('Fréquence (log)')
    ax2.set_title('Echelle log-log')

    plt.tight_layout()
    plt.show()

def plotLocalClutering(graph):
    """afficher la distribution du coefficient de clustering local
    graph: graphe"""
    localClusteringCoef = localCustering(graph)
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(12,5))

    ax1.set_xlim(0,1)
    ax1.hist(list(localClusteringCoef.values()), bins=100, color='green', alpha=0.7,cumulative=True, density=True,histtype="step")
    ax1.set_xlabel('Coefficient de Clustering Local')
    ax1.set_ylabel('Nombre de Noeuds')
    ax1.set_title('Distribution du Coefficient de Clustering Local')

    ax2.set_xlim(0,1)
    ax2.hist(list(localClusteringCoef.values()), bins=100, color='green', alpha=0.7,cumulative=-1, density=True,histtype="step")
    ax2.set_xlabel('Coefficient de Clustering Local')
    ax2.set_ylabel('Nombre de Noeuds')
    ax2.set_title('Distribution du Coefficient de Clustering Local')

    plt.tight_layout()
    plt.show()

def plotCommunity(G,degreMin):
    """afficher la structure de communauté du graphe
    G: graphe
    degreMin: degré minimum des noeuds à garder dans le graphe"""

    # supprimer les noeuds de degré faible
    lowDegree = [n for n, d in G.degree() if d < degreMin]
    G.remove_nodes_from(lowDegree)

    # plus grande composante connexe
    components = nx.connected_components(G)
    pcc = max(components, key=len)
    H = G.subgraph(pcc)
    centrality = nx.betweenness_centrality(H, k=10, endpoints=True)

    # trouver les communautés
    lpc = nx.community.label_propagation_communities(H)
    comId = {n: i for i, com in enumerate(lpc) for n in com}

    # dessiner le graphe
    fig, ax = plt.subplots(figsize=(20, 15))
    pos = nx.spring_layout(H, k=0.15)
    nodeCol = [comId[n] for n in H]
    nodeSize = [v * 20000 for v in centrality.values()]
    nx.draw_networkx(
        H,
        pos=pos,
        with_labels=False,
        node_color=nodeCol,
        node_size=nodeSize,
        edge_color="gainsboro",
        alpha=0.4,
    )
    plt.title("Community structure of the graph")
    plt.axis("off")
    plt.show()

def drawGraphCentrality(title,values,graph,pos):
    """afficher le graphe avec les valeurs de centralité
    title: titre du graphe
    values: valeurs de centralité (betweenness ou closeness centrality)
    graph: graphe"""
    plt.figure()
    plt.title(title)
    nx.draw(graph,pos,node_color=values, with_labels=False,node_size=10, edge_color='lightgray', alpha=0.5)
    plt.show()


def main():

    GrQcfile = 'C:\\Users\\winona\\Documents\\M1\\S1\\SystemeComplexe\\Projet\\ca-GrQc.txt\\extract\\outputGraph.txt'
    facebookFile = 'C:\\Users\\winona\\Documents\\M1\\S1\\SystemeComplexe\\Projet\\facebook-wosn-links\\extract\\outputGraph.txt'
    graphGrQc = loadGraph(GrQcfile)
    graphFacebook = loadGraph(facebookFile)


    print("######### GrQc Graph #########")

    nbSommets, nbAretes = getNumberOfNodesAndEdges(graphGrQc)
    print("Nombre de sommets:", nbSommets)
    print("Nombre d'arêtes:", nbAretes)

    # Afficher le nombre de triangles dans le graphe
    startTime = time.time()
    print("Nombre de triangles:", numberTriangles(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Afficher la distance moyenne entre deux sommets du graphe
    startTime = time.time()
    print("Distance moyenne entre deux sommets:", averageShortestPathLength(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Afficher le diamètre du graphe
    startTime = time.time()
    print("Diamètre du graphe:", graphDiameter(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Afficher la densité et le degré moyen du graphe
    startTime = time.time()
    print("Densité du graphe:", computeDensity(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")
    startTime   = time.time()
    print("Degré moyen du graphe:", degreMoyen(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    startTime = time.time()
    print("Global Custering",globalClustering(graphGrQc))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Afficher la distribution des degrés en lin-lin et log-log
    startTime = time.time()
    print("Distribution des degrés")
    plotDegreeDistribution(graphGrQc)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # afficher la distribution du coefficient de clustering local
    startTime = time.time()
    print("Distribution du Coefficient de Clustering Local")
    plotLocalClutering(graphGrQc)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")


    ###### analyse du reseau ######

    startTime = time.time()
    plotCommunity(graphGrQc,10)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")
    print('\n\n')

    G = graphGrQc
    pos = nx.spring_layout(G)
    bC = nx.betweenness_centrality(G)
    cC = nx.closeness_centrality(G)
    # Convertir les dictionnaires en listes pour le calcul de la corrélation
    betweennessVal = list(bC.values())
    closenessVal = list(cC.values())
    drawGraphCentrality('Betweenness Centrality',betweennessVal,G,pos)
    drawGraphCentrality('Closeness Centrality',closenessVal,G,pos)
    # Calculer la corrélation de Spearman entre chaque paire de mesures de centralité
    correlationBetweennessCloseness, _ = spearmanr(betweennessVal, closenessVal)
    # Afficher les résultats
    print("Corrélation de Spearman :", correlationBetweennessCloseness)

    # Calculer les classements pour chaque mesure de centralité
    betweennessRanks = stats.rankdata(betweennessVal)
    closenessRanks = stats.rankdata(closenessVal)
    # Calculer la corrélation de Spearman entre les classements
    correlationBetweennessCloseness, _ = stats.spearmanr(betweennessRanks, closenessRanks)
    print("Corrélation de Spearman :", correlationBetweennessCloseness)    











    print("######### facebook Graph #########")

    nbSommets, nbAretes = getNumberOfNodesAndEdges(graphFacebook)
    print("Nombre de sommets:", nbSommets)
    print("Nombre d'arêtes:", nbAretes)

    startTime = time.time()
    print("Nombre de triangles:", numberTriangles(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")


    startTime = time.time()
    print("Distance moyenne approximative entre deux sommets:", approximateAverageDistance(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")
    startTime = time.time()
    print("Diamètre approximatif du graphe:", approximateDiameter(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Afficher la densité et le degré moyen du graphe
    startTime = time.time()
    print("Densité du graphe:", computeDensity(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")
    startTime = time.time()
    print("Degré moyen du graphe:", degreMoyen(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    startTime = time.time()
    print("Global Custering",globalClustering(graphFacebook))
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")
    # Afficher la distribution des degrés en lin-lin et log-log
    startTime = time.time()
    print("Distribution des degrés")
    plotDegreeDistribution(graphFacebook)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    # Plot the distribution of local clustering coefficients
    startTime = time.time()
    print("Distribution du Coefficient de Clustering Local")
    plotLocalClutering(graphFacebook)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")


    ###### analyse du reseau ######
    startTime = time.time()
    plotCommunity(graphFacebook,60)
    endTime = time.time()
    print("Temps d'execution", endTime - startTime,"\n")

    G = graphFacebook
    # Calculez une approximation de la betweenness centrality
    bC = nx.approximate_current_flow_betweenness_centrality(G)
    # Triez les noeuds par centralité en ordre décroissant
    sortedNodes = sorted(bC.items(), key=lambda x: x[1], reverse=True)
    # Prenez les n premiers noeuds
    n = 1000
    top_nodes = [node for node, _ in sortedNodes[:n]]
    # Créez un sous-graphe avec ces noeuds
    subgraph = G.subgraph(top_nodes)
    pos = nx.spring_layout(subgraph)
    # calcule betweenness centrality
    bC = nx.betweenness_centrality(subgraph)
    cC = nx.closeness_centrality(subgraph)

    betweennessVal = list(bC.values())
    closenessVal = list(cC.values())
    drawGraphCentrality('Betweenness Centrality',betweennessVal,subgraph,pos)
    drawGraphCentrality('Closeness Centrality',closenessVal,subgraph,pos)
    # Calculer la corrélation de Spearman entre chaque paire de mesures de centralité
    correlationBetweennessCloseness, _ = spearmanr(betweennessVal, closenessVal)
    print("Corrélation de Spearman :", correlationBetweennessCloseness)

    # Calculer les classements pour chaque mesure de centralité
    betweennessRanks = stats.rankdata(betweennessVal)
    closenessRanks = stats.rankdata(closenessVal)
    # Calculer la corrélation de Spearman entre les classements
    correlationBetweennessCloseness, _ = stats.spearmanr(betweennessRanks, closenessRanks)
    print("Corrélation de Spearman :", correlationBetweennessCloseness)  



if __name__ == "__main__":
    main()