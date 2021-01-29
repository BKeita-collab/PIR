# Auteur : Gabriela Elgarrista
# Auteur : Carmen Brando

import requests
import csv
import json
import annexe as a

def historique():
    base_url = "http://api.geohistoricaldata.org/geocoding?"
    out = open("adresses_geocodees.csv", "w")
    out_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    with open('dataset_1_500_lignes.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        result_count = 0
        no_result_count=0
        seuil=[50,100,200]
        sous_seuil=[0,0,0]
        N=1
        for row in csv_reader:
            if line_count == 0:
                out_writer.writerow(['id','profession','annee_sour','source','Professi_1','localisati','détail','ind_nom','indiv_titre','association','successeur','ancienne_m','nbre_adres','acitivités','annee_expo','nom_boutiq','type_rue','article_rue','nom_rue','num_rue','cplt_num_rue','ville_rue','autre_vill','infos_rue','unnamed1','quart/sec','arrondiss','unnamed2','unnamed3','geocoder_t','geocoder_s','a_corriger','lon','lat','adresse', 'geometry.lng_1', 'geometry.lat_1', 'source_prop', 'url_prop','dist_prop'])
                line_count += 1
            else:
                line_count += 1
                params = {"address": row[19] +" "+row[20]+ " " + row[16] + " " + row[17]+" " + row[18], "date": "1898", "precision": "true", "maxresults": N}
                print("adresse: " + row[19] + " "+row[20]+" " + row[16] + " " + row[17]+" " + row[18])
                print("requete: " + base_url + "address" + "=" + row[1] + " " + row[0] + "&" + "date" + "=" + "1898" + "&precision=true&maxresults="+str(N))
                r = requests.get(base_url, params)
                print("\n")
                print(r.json())
                print("\n")
                if r.status_code == 200:
                    if (len(r.json())==0):
                        print("ADRESSE A VERIFIER:" + row[19] +" "+row[20]+ " " + row[16] + " " + row[17]+" " + row[18])
                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34]])
                        no_result_count+=1
                    else:
                        for k in range (0,N):
                            if (len(r.json())>k):
                                if (r.json()[k]['geometry']['type']=='GeometryCollection'):
                                    if (r.json()):
                                        source_prop = str(r.json()[k]['historical_source'])
                                        print(source_prop)
                                        url_prop = base_url + "address" + "=" + row[1] + " " + row[0] + "&" + "date" + "=" + "1898" + "&precision=true&maxresults=1"
                                        lon_prop = str(r.json()[k]['geography']['geometries'][0]['coordinates'][0][0])
                                        print("lon_prop", lon_prop)
                                        lat_prop = str(r.json()[k]['geography']['geometries'][0]['coordinates'][0][1])
                                        print("lat_prop", lat_prop)
                                        print("")
                                        dist_prop=a.haversine(float(lon_prop),float(lat_prop),float(row[33]),float(row[34]))
                                        print("row[33]", row[33], "row[34]", row[34], "dist_prop", dist_prop)
                                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34], lon_prop, lat_prop, source_prop, url_prop,dist_prop])
                                        result_count+=1
                                        for i in range(len(seuil)):
                                            if (dist_prop<seuil[i]):
                                                sous_seuil[i]+=1
                                        print (r.json)
                                    else:
                                        print("ADRESSE A VERIFIER:" + row[19] +" "+row[20]+ " " + row[16] + " " + row[17]+" " + row[18])
                                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34]])
                                        no_result_count+=1
                                elif (r.json()[k]['geometry']['type']=='MultiPoint'):
                                    if (r.json()):
                                        source_prop = str(r.json()[k]['historical_source'])
                                        print(source_prop)
                                        url_prop = base_url + "address" + "=" + row[1] + " " + row[0] + "&" + "date" + "=" + "1898" + "&precision=true&maxresults=1"
                                        lon_prop = str(r.json()[k]['geography']['coordinates'][0][0])
                                        print(lon_prop)
                                        lat_prop = str(r.json()[k]['geography']['coordinates'][0][1])
                                        print(lat_prop)
                                        print("")
                                        dist_prop=a.haversine(float(lon_prop),float(lat_prop),float(row[33]),float(row[34]))
                                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],lon_prop, lat_prop, source_prop, url_prop,dist_prop])
                                        result_count+=1
                                        for i in range (len(seuil)):
                                            if (dist_prop<seuil[i]):
                                                sous_seuil[i]+=1
                                                print(10*"\n", sous_seuil, 10*"\n")
                                        print (r.json)
                                    else:
                                        print("ADRESSE A VERIFIER:" + row[1] + " " + row[0])
                                        out_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34]])
                                        no_result_count+=1
    out.close()
    tot_result=result_count+no_result_count
    print ("\n\nSur un total de "+str(tot_result)+" entrée, il y a :\n"+str(result_count)+" requêtes abouties\n"+str(no_result_count)+" requêtes sans résultats\n")
    for k in range (len(seuil)):
        print(str(sous_seuil[k])+" requêtes en dessous du seuil de "+str(seuil[k])+"m")
        print("Une précision de "+str(a.precision(sous_seuil[k],result_count))+" %")
        print("Un rappel de "+str(a.rappel(sous_seuil[k],tot_result))+" %")
        print("Un f_score de : "+str(a.f_score(sous_seuil[k],tot_result,result_count))+"\n")

historique()
