import matplotlib.pyplot as plt

def trace_graphique(ign, ban, ghd):
    """
    Permet de tracer les histogrammes représentant les paramètres des résultats des différents géocodages.
    type(ign) = list
    type(ban) = list
    type(ghd) = list
    """
    ign_distance = ign[:3]
    ban_distance = ban[:3]
    ghd_distance = ghd[:3]
    ign_f_score = [ign[3]]
    ban_f_score = [ban[3]]
    ghd_f_score = [ghd[3]]
    ign_temps = [ign[4]]
    ban_temps = [ban[4]]
    ghd_temps = [ghd[4]]
    largeur_barre = 0.3
    
    position_ign_distance = list(range(len(ign_distance)))
    position_ban_distance = [i+largeur_barre for i in position_ign_distance]
    position_ghd_distance = [i+2*largeur_barre for i in position_ign_distance]
    position_ign_f_score = [3]
    position_ban_f_score = [3+largeur_barre]
    position_ghd_f_score = [3+2*largeur_barre]
    position_ign_temps = [4]
    position_ban_temps = [4+largeur_barre]
    position_ghd_temps = [4+2*largeur_barre]

    plt.figure(figsize = (10, 20))

    axe1 = plt.subplot(1,2,1)
    
    trace_ign_distance = plt.bar(position_ign_distance, ign_distance, width=largeur_barre, color='green')
    trace_ban_distance = plt.bar(position_ban_distance, ban_distance, width=largeur_barre, color='red')
    trace_ghd_distance = plt.bar(position_ghd_distance, ghd_distance, width=largeur_barre, color='blue')

    plt.xticks([r + (9/8)*largeur_barre for r in range(len(ign_distance))], ['Moyenne', 'Médiane*10', 'Ecart-type'])

    axes = plt.gca()
    axes.set_ylabel('Distance (m)')

    plt.legend([trace_ign_distance, trace_ban_distance, trace_ghd_distance], ['ign', 'ban', 'ghd'], loc = 'upper left', ncol = 2, scatterpoints = 1, frameon = True, markerscale = 2, title = "Légende", borderpad = 0.5, labelspacing = 0.5)


    plt.subplot(2,2,2)
    trace_ign_f_score = plt.bar(position_ign_f_score, ign_f_score, width=largeur_barre, color='green')
    trace_ban_f_score = plt.bar(position_ban_f_score, ban_f_score, width=largeur_barre, color='red')
    trace_ghd_f_score = plt.bar(position_ghd_f_score, ghd_f_score, width=largeur_barre, color='blue')

    plt.xticks([267/80], ['F-score (%)'])



    plt.subplot(2,2,4)
    trace_ign_temps = plt.bar(position_ign_temps, ign_temps, width=largeur_barre, color='green')
    trace_ban_temps = plt.bar(position_ban_temps, ban_temps, width=largeur_barre, color='red')
    trace_ghd_temps = plt.bar(position_ghd_temps, ghd_temps, width=largeur_barre, color='blue')

    plt.xticks([347/80], ['Temps (s)'])

    
    plt.show()
