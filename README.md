# Filtrage des données
On supprime les premiers lignes car elles ne servent a rien

<b>GrQc</b>
```
cat CA-GrQc.txt | awk '{if (NR>4)print}' >data1.txt # supprimer 4premieres lignes
```
Apres la creation de data1.txt on execute le code index.py pour créer des index croissant dans un nouveau fichier data.txt

<b>Facebook</b>
```
cat out.facebook-wosn-links | awk '{if (NR>2)print}'>data.txt # supprimer 2 premieres lignes
```
---
```
cat data.txt | awk '{if($1!=$2)print $1" "$2}' | wc -l 

```
--> 28968 <b>GrQc</b>

--> 817035 <b>Facebook</b>
```
cat data.txt | awk '{if($1!=$2)print $1" "$2}' | sort | wc -l
```
--> pas de changement donc ok
```
cat data.txt | awk '{if($1!=$2)print $1" "$2}' | sort | uniq | wc -l # pas deux fois la meme arretes
```
ici on a pas deux fois la meme arrete mais on sais pas si 0 1 et 1 0 existe
```
cat data.txt | awk '{if($1!=$2)print $1" "$2}' |awk '{if($1>$2)print$2" "$1;else print $1" "$2}' > nonOrienteSansBoucle.txt
```
```
cat data.txt | awk '{if($1!=$2)print $1" "$2}' >sansBoucle.txt
```
```
diff sansBoucle.txt nonOrienteSansBoucle.txt # Aucun differences les deux fichiers sont donc identiques
```
```
cat nonOrienteSansBoucle.txt | sort | uniq > prefiletered.txt
wc -l prefiletered.txt 
```
--> 28980<b>GrQc</b>

--> 817035 <b>Facebook</b>

trouver si ya des troues entre les données (des id pas dans le fichier)
```
cat prefiletered.txt | awk '{print $1; print $2}' | wc -l
```
--> 57960 <b>GrQc</b>

--> 1634070 <b>Facebook</b>
```
cat prefiletered.txt | awk '{print $1; print $2}' | sort -n | uniq | tail # dernieres lignes
```
<b>GrQc</b> : il faut 10484 ligne

<b>Facebook</b> : il faut 63731 lignes 
```
cat prefiletered.txt | awk '{print $1; print $2}' | sort -n | uniq | wc -l 
```
<b>GrQc</b> : 10484

<b>Facebook</b> : 63731

donc pas de troue dans les données
```
cat prefiletered.txt | sort -n | uniq > betterFiltered.txt
```
```
cat betterFiltered.txt | awk '{print $1-1" "$2-1}' > almostFitered.txt
head almostFitered.txt
```


le fichier <b>graph.py</b> correspond a tout les traitements et affichages qui on pu etre effectués sur les deux reseaux.