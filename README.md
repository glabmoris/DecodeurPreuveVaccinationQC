# DecodeurPreuveVaccinationQC
Extrait les informations contenues dans le code QR de la preuve de vaccination générée par le gouvernement du Québec

# Utilisation

## Prérequis
Le script dépend de zxing, pdf2image et du Java Development Kit (JDK).

Par exemple, pour installer les dépendances sous Ubuntu:
```
sudo apt install python3-pip
pip3 install zxing pdf2image
sudo apt install openjdk-11-jdk
```

## Exécution
Éxécuter le script Python3 extraire.py avec en paramètre le chemin vers le fichier PDF généré par le Gouvernement du Québec:
```
python3 extraire.py preuve.pdf
```


## Exemple
![screenshot](https://user-images.githubusercontent.com/9091120/129313758-1194793d-c929-463c-a355-7fa61882c81c.png)
