import requests
from bs4 import BeautifulSoup

url = 'https://www.lacentrale.fr/listing?energies=ess&makesModelsCommercialNames=PORSCHE&mileageMax=125000&mileageMin=50000&priceMax=119800&yearMax=2022&yearMin=2015'
r = requests.get(url)

if r.status_code == 200:
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find_all('div', {'class': 'searchCardContainer'})
    values = []
    for row in table:
        value={}
        value['name']=row.find('h3', {'class': 'Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2'}).text
        value['price']=row.find('span', {'class': 'Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2'}).text
        value['year']=row.find('div', {'class': 'Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2'}).text
        value['km']=row.find('div', {'class': 'Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2'}).text
        values.append(value)
    print(values)
else:
    print("Requete échoué avec un status code : ", r.status_code)
