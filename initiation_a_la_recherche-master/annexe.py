import numpy as np
import math

def arctan3(x , y) :
    if x > 0 and y>0 :
        alpha = np.arctan(x/y)
        return alpha
    elif (x > 0 and y<0) or (x<0 and y<0) :
        alpha = np.arctan(x/y) + np.pi
        return alpha
    elif x<0 and y>0 :
        alpha = np.arctan(x/y) + 2*np.pi
        return alpha

def haversine(lon1,lat1,lon2,lat2):
    R=6371 #Rayon de la Terre
    dLat = (lat2-lat1)*np.pi/180 #ecart de latitude en radian
    dLon = (lon2-lon1)*np.pi/180 #ecart de longitude en radian
    a=np.sin(dLat/2)**2 + np.cos(lat1*np.pi/180)*np.cos(lat2*np.pi/180) * np.sin(dLon/2)**2
    c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
    d = R*c*1000 #distance en metres
    return d
    
def precision(sous_seuil,total_reponses):
    precision = (sous_seuil/total_reponses)*100
    print("Précision : ", precision)
    return precision

def rappel(sous_seuil,total):
    rappel = (sous_seuil/total)*100
    print("Rappel : ", rappel)
    return rappel

def f_score(sous_seuil, total, total_reponses):
    p = precision(sous_seuil,total_reponses)
    r = rappel(sous_seuil,total)
    return (2*p*r)/(p+r)
