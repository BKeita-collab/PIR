import pandas as pd
from random import choice

def choix_ligne():
    """
    Sélectionne aléatoirement 500 numéros entre 1 et 5771 qui seront les numéros des lignes à géocoder.
    :return: list[int, int, ...]
    """
    lignes_supprimees = list(range(1, 5772))
    for i in range(500):
        choix = choice(lignes_supprimees)
        lignes_supprimees.remove(choix)
    return lignes_supprimees

def choix_500_premieres():
    """
    Variante de la fonction précédente utilisée dans le cas où l'on souhaite garder les 500 premières lignes.
    """
    return list(range(501, 5772))

def dataset_1():
    """
    Return data from 'resources/dataset_1.csv' as a Pandas DataFrame with a column 'address'
    containing the full address (number + type + street).
    :return: a Pandas DataFrame holding the data from 'resources/dataset_1.csv'
    """
    #lignes_supprimees = choix_500_premieres()
    lignes_supprimees = choix_ligne()
    csv = pd.read_csv('echantillon_commerce_complet_prop', skiprows = lignes_supprimees) # Pandas loads the CSV file as a DataFrame object
    csv.fillna('', inplace=True) # Pandas fills empty celles with NaN. We replace every Nan value with an emtpy string.
    csv.num_rue = csv.num_rue.apply(str)  # Cast street numbers to strings
    # Create a new column named 'address' which concatenates the columns ['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']
    # csv[['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']]  select a subset of the table 'csv'.
    # .agg(' '.join, axis=1) is equivalent to merge the selected cells of every lines as 'num_rue' + ' ' + 'cpltnum_ru' + ' ' + 'type_rue' + ' ' + 'article_ru' + ' ' + 'nom_rue'
    csv['address'] = csv[['num_rue', 'cpltnum_ru', 'type_rue', 'article_ru', 'nom_rue']].agg(' '.join, axis=1)
    csv.to_csv('dataset_1_500_lignes.csv')
    return csv
