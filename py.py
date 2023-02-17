import requests
import csv
from bs4 import BeautifulSoup

# On définit des constantes qui sont utilisées comme paramètres pour récup les données de la centrale.
brand = "RENAULT"
year_max = 2022
year_min = 2010
mileage_max = 100000
mileage_min = 0
energy = "ess"
price_min = 0
price_max = 28300

# fonction scrap_listing et ses paramètres
def scrap_listing(brand, year_max, year_min, mileage_min, mileage_max, energy, price_min, price_max, page_num):
    # On construit notre url avec nos paramètre définis 
    url = "https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={mileage_max}&mileageMin={mileage_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}&options=&page={page_num}".format(
        energy=energy, brand=brand, mileage_max=mileage_max, mileage_min=mileage_min, price_max=price_max, price_min=price_min, year_max=year_max, year_min=year_min, page_num=page_num)

    # On envoie une requête HTTP GET à notre variable 'url', et on stocke la réponse du serveur dans la variable 'response'.
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    #On Ouvre le fichier "scraped_data.csv" en mode écriture, on le créer s'il n'existe pas. 
    with open("scraped_data.csv", "w", newline="") as f:
        #On créer un objet csv.writer et on écrit la header dans le fichier CSV.
        writer = csv.writer(f)
        writer.writerow(["Brand", "Motorisation", "Boite de vitesse", "Année", "Kilométrage", "Carburant", "Prix"])
        
        #On démarre une boucle qui s'exécute 10 fois (nombre de pages)
        for page_num in range(1, 11):
            #On ppelle la fonction scrap_listing avec les paramètres définis et stocke le contenu HTML retourné dans html_page
            html_page = scrap_listing(brand, year_max, year_min, mileage_min, mileage_max, energy, price_min, price_max, page_num)
            #Ensuite on parse
            soup = BeautifulSoup(html_page, 'html.parser')
            # On trouve toutes les cartes de voitures dans le contenu HTML (avec la classe HTML)
            searchCards = soup.find_all(class_="searchCard")
            # On loop pour chaque cartes
            for searchCard in searchCards:
                # On cherche l'élément dans la carte avec la classe spécifique
                char = searchCard.find_all(class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
                price = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2')
                brand_ = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2')
                motor = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')
                
                # On extrait le texte de l'élément qui nous intéresse dans la liste 'char'
                char_year = char[0].text.strip()
                char_mileage = char[1].text.strip()
                char_gear = char[2].text.strip()
                char_fuel = char[3].text.strip()

                # On écrit dans le fichier CSV en utilisant la méthode writerow de notre objet csv.writer avec toutes les colonnes
                writer.writerow([brand_.text.strip(), motor.text.strip(), char_gear, char_year, char_mileage, char_fuel, price.text.strip()])
