import geocoders.ban as ban
import geocoders.ign as ign
from statistics import median, stdev, mean
from timeit import default_timer as timer
from datasets import annuaires_du_commerce
from geocoders.util import ban_to_dataframe, ign_to_dataframe
import geocodeurHistorique_commerce
import logging
import pandas as pd
import annexe
import numpy
import matplotlib.pyplot as plt
import graphiques

logging.basicConfig(level=logging.INFO, format='%(message)s')


# Méthode principale
def main():
    ds1 = annuaires_du_commerce.dataset_1()  # Charge les données à géocoder
    liste_ign = exec_ign(ds1)  # Géocode avec le service IGN et sauvegarde le résultat
    liste_ban = exec_ban(ds1)  # Géocode avec le service BAN et sauvegarde le résultat
    liste_historique = exec_historique(ds1)
    graphiques.trace_graphique(liste_ign, liste_ban, liste_historique)


def exec_ban(dataset):
    # Définit les options de géocodage
    number_of_results = 1
    ban_opts = {'limit': number_of_results, 'citycode': 75056}  # Force à chercher dans Paris

    # Géocode le contenu de la colonne 'address' dans dataset.
    logging.info(f'Executing BAN geocoder with options {ban_opts}')
    geocoder = ban.geocode
    results, runtimes, global_time = run(dataset['address'], geocoder, opts=ban_opts)

    # Affiche les statistiques de temps d'exécution
    summary(dataset, results, runtimes)

    # Transforme les résultats renvoyés par le géocodeur en tableau Pandas
    all = ban_to_dataframe.transform(results, keep_only=number_of_results)

    # Concatène le tableau des résultats aux données d'entrée et sauvegarde le résultat
    pd.concat([dataset, all], axis=1).to_csv('annuaire_du_commerce_ban.csv')

    #Calcule la moyenne des écarts entre les coordonnées géographiques réelles et les coordonnées géocodées
    csv = pd.read_csv('annuaire_du_commerce_ban.csv')
    distances, avg_distance, mediane, ecart_type, f_score = calcul_ecart(csv, "ban")
    print("Liste des distances : ", distances)
    print(5*"\n")
    print("Ecart moyen des distances : ", avg_distance)
    print(5*"\n")
    print("Médiane des distances : ", mediane)
    print(5*"\n")
    print("Ecart-type : ", ecart_type)
    print(5*"\n")
    print("F-score : ", f_score)
    
    #Donne le temps total
    print("Temps total : ", global_time)

    return [avg_distance, mediane*10, ecart_type, f_score, global_time]


def exec_ign(dataset):
    # Définit les options de géocodage
    number_of_results = 1
    ign_opts = {'maxResp': number_of_results}

    # Géocode le contenu de la colonne 'address' dans dataset.
    logging.info(f'Executing IGN geocoder')
    addresses_plus_paris = dataset['address'] + ' 75'  # Force à chercher dans Paris (75)
    results, runtimes, global_time = run(addresses_plus_paris, ign.geocode, feature_type='address', opts= ign_opts)

    # Affiche les statistiques de temps d'exécution
    summary(dataset, results, runtimes)

    # Transforme les résultats renvoyés par le géocodeur en tableau Pandas
    all = ign_to_dataframe.transform(results, keep_only=number_of_results)

    # Concatène le tableau des résultats aux données d'entrée et sauvegarde le résultat
    pd.concat([dataset, all], axis=1).to_csv('annuaire_du_commerce_ign.csv')

    #Calcule la moyenne des écarts entre les coordonnées géographiques réelles et les coordonnées géocodées
    csv = pd.read_csv('annuaire_du_commerce_ign.csv')
    distances, avg_distance, mediane, ecart_type, f_score = calcul_ecart(csv, "ign")
    print("Liste des distances : ", distances)
    print(5*"\n")
    print("Ecart moyen des distances : ", avg_distance)
    print(5*"\n")
    print("Médiane des distances : ", mediane)
    print(5*"\n")
    print("Ecart-type : ", ecart_type)
    print(5*"\n")
    print("F-score : ", f_score)

    #Donne le temps total
    print("Temps total : ", global_time)

    return [avg_distance, mediane*10, ecart_type, f_score, global_time]

def exec_historique(dataset):
    start = timer()
    geocodeurHistorique_commerce.historique()
    global_time = timer() - start

    #Calcule la moyenne des écarts entre les coordonnées géographiques réelles et les coordonnées géocodées
    distances, avg_distance, mediane, ecart_type, f_score = calcul_ecart(pd.read_csv('adresses_geocodees.csv', encoding = "ISO-8859-1"), "ghd")
    
    print("Liste des distances : ", distances)
    print(5*"\n")
    print("Ecart moyen des distances : ", avg_distance)
    print(5*"\n")
    print("Médiane des distances : ", mediane)
    print(5*"\n")
    print("Ecart-type : ", ecart_type)
    print(5*"\n")
    print("F-score : ", f_score)

    #Donne le temps total
    print("Temps total : ", global_time)

    return [avg_distance, mediane*10, ecart_type, f_score, global_time]


def run(dataset, geocoder, **kwargs):
    """
    Geocode a dataset using a geocoder.
    :param dataset: a dataset to geocode
    :param geocoder: the geocoder to use
    :return:
    """
    results, runtimes = [], []

    data_list = list(dataset)
    data_len = len(data_list)
    for idx, item in enumerate(data_list):
        # Appelle le géocodeur passé en paramètres avec l'item à géocoder et les options passées à la méthode et
        # mesure le temps d'exécution
        start = timer()
        r = next(geocoder(item, **kwargs))
        elapsed_time = timer() - start

        results.append(r)
        runtimes.append(elapsed_time)

        # Affiche le géocodage courant
        log = '\u2713' if r['success'] else '\u2728'
        log += f" {idx + 1}/{data_len} {elapsed_time * 1000}ms: \'{item}\'"
        log += '' if r['success'] else r['error']
        logging.info(log)

    global_time = sum(runtimes)

    return results, runtimes, global_time


def summary(dataset, results, times):
    """
    Print some information about the execution time of a geocoding
    """
    succ, fail = [], []

    [succ.append(r) if r['success'] else fail.append(r) for r in results]

    logging.info(
        f'Geocoding {len(dataset)} addresses took {sum(times)}s'
        f' with {len(succ)} successes and {len(fail)} failures'
        f' (min = {min(times)}s,'
        f' max = {max(times)}s,'
        f' avg = {mean(times)}s,'
        f' stddev = {stdev(times)}s,'
        f' median = {median(times)}s)')

def calcul_ecart(csv, geocodeur):
    csv.fillna(0, inplace=True)
    if geocodeur == "ign" or geocodeur == "ban":
        lon_reel= csv['lon']
        lat_reel = csv['lat']
    else: #Il y a un problème avec le fichier adresses_geocodees.csv : les en-têtes sont décalés par rapport aux données qu'ils représentent. Ainsi, pour le géocodeur ghd, l'en-tête 'lat' correspond à la longitude, l'en-tête 'adresse' correspond à la latitude.
        lon_reel = csv['lat']
        lat_reel = csv['adresse']
    lon_reel_list = list(lon_reel)
    lat_reel_list = list(lat_reel)
    lon_geocode = csv['geometry.lng_1']
    lon_geocode_list = list(lon_geocode)
    lat_geocode = csv['geometry.lat_1']
    lat_geocode_list = list(lat_geocode)
    
    #On enlève des listes les adresses non géocodées
    lon_reel_tableau = []
    lat_reel_tableau = []
    lon_geocode_tableau = []
    lat_geocode_tableau = []
    for i in range(len(lon_geocode_list)):
        if lon_geocode_list[i] != 0:
            lon_reel_tableau.append(lon_reel_list[i])
            lat_reel_tableau.append(lat_reel_list[i])
            lon_geocode_tableau.append(lon_geocode_list[i])
            lat_geocode_tableau.append(lat_geocode_list[i])

    lon_reel_list = numpy.asarray(lon_reel_tableau)
    lat_reel_list = numpy.asarray(lat_reel_tableau)
    lon_geocode_list = numpy.asarray(lon_geocode_tableau)
    lat_geocode_list = numpy.asarray(lat_geocode_tableau)


    print("Longitude réelle ", len(lon_reel_list), "\nLatitude réelle ", len(lat_reel_list), "\nLongitude géocodée ", len(lon_geocode_list), "\nLatitude géocodée ", len(lat_geocode_list))
            

    distances = annexe.haversine(lon_reel_list,lat_reel_list,lon_geocode_list,lat_geocode_list)

    #Calcul moyenne
    longueur = len(distances)
    avg_distance = sum(distances)/longueur

    #Calcul médiane
    distances.sort()
    if longueur%2 == 1:
        mediane = distances[longueur//2]
    else:
        mediane = (distances[longueur//2-1]+distances[longueur//2])/2

    #Calcul écart-type
    carre_ecart_moyenne = [(i-avg_distance)**2 for i in distances]
    ecart_type = numpy.sqrt(sum(carre_ecart_moyenne)/longueur)

    #Calcul f-score
    sous_seuil = 0
    for i in distances:
        if i <= 50:
            sous_seuil += 1
    f_score = annexe.f_score(sous_seuil, 500, longueur)

    return distances, avg_distance, mediane, ecart_type, f_score
    


if __name__ == '__main__':
    main()
