import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

######################################################################

print("\nProgram dodatkowy 2 - Oliwia Wojtkowska\n")

#########################################################################
print("Idą święta, więc część osób na pewno szuka jakichś ciekawych prezentów.\n"
      "Co zrobić, aby kobiety były zadowolone ze znaleziska pod choinką?\n"
      "Zalando podpowiada nam, że w tym sezonie trendem są sztuczne futra.\n"
      "Ok, ale jakie wybrać? I ile musimy na takie cudo wydać?\n"
      "W podjęciu tej jakże trudnej decyzji przychodzi nam na szczęście pomoc w postaci kilku linii kodu w pythonie\n"
      "Przekonajmy się, że wybór prezentu jeszcze nigdy nie był tak prosty !\n"
      "Zaczynamy !\n"
      "\nNa początku ze strony 'zalando.pl/sztuczne-futra' skopiujmy sobie dane wszystkich 73 futer i zapiszmy do pliku 'dodatkowy2.csv'")

############## te linie kodu można odkomentować, jednak by zaoszczędzić czas można korzystać także z gotowego pliku w csv

adres = requests.get("https://www.zalando.pl/sztuczne-futra/")
soup = BeautifulSoup(adres.content, "html.parser")
Marki = soup.find_all("div", 'catalogArticlesList_brandName')
Ceny = soup.find_all("div", "catalogArticlesList_priceBox")
Marka = []
Cena = []
Promocja = []
for i in range(0,len(Marki)):
    Marka.append(Marki[i].text)
    Cena.append((Ceny[i].text).split("\n"))
    Promocja.append(0)
for j in range(0, len(Cena)):
       if len(Cena[j]) ==4:
           # niestety format ceny sprawia, że musimy się tak pobawić
            Cena[j] = float(((((Cena[j][2]))[:-3]).replace(",", ".")).replace("\xa0", ""))
       elif len(Cena[j]) ==5:
            StaraCena=[]
            StaraCena = float(((((Cena[j])[1])[:-3]).replace(",", ".")).replace("\xa0", ""))
            Cena[j] = float(((((Cena[j][3]))[:-3]).replace(",", ".")).replace("\xa0", ""))
            Promocja[j] = StaraCena-Cena[j]

Marka = pd.DataFrame(Marka)
Cena = pd.DataFrame(Cena)
Promocja=pd.DataFrame(Promocja)
dane = pd.merge(Marka, Cena, how='right', left_index=True, right_index=True)
dane = pd.merge(dane, Promocja, how='right', left_index=True, right_index=True)
dane.columns = ["Marka", "Cena", "Promocja"]
dane.to_csv(path_or_buf="dodatkowy2.csv")


print("\nPlik mamy już zapisany, wczytajmy więc z niego dane i zobaczmy jak nasza tabelka wygląda:\n"
      "Kolumna 'Promocja' jest to różnica w cenie między starą ceną, a aktualną, zawartą w kolumnie 'Cena'\n")
dane = pd.read_csv("dodatkowy2.csv")
print(dane.head())
print("\nTa kolumna 'Unnamed' nie jest nam potrzebna, skasujmy ją więc i zobaczmy nasze dane raz jeszcze:\n")
del dane['Unnamed: 0']
print(dane.head())
print("\nNo już lepiej. Zobaczmy zatem jaka jest średnia cena sztucznych futer:\n")
print(dane['Cena'].mean())
print("\nOk, ale czy nie jest tak, że jakieś futra są po prostu bardzo drogie i zawyżają nam średnią?\n"
      "Policzmy zatem medianę i odchylenie standardowe oraz zobaczmy rozkład cen na histogramie:\n")
print("Mediana: {0}, odchylenie standardowe od średniej: {1}".format(dane['Cena'].median(axis=0), dane['Cena'].std(axis=0)))
print("Wykres 1 - histogram Marek\n")
plt.hist(dane["Cena"],bins=50)
plt.title("Wykres 1\nRozkład cen sztucznych futer")
plt.xlabel("Cena futra")
plt.ylabel("Ilość futer w danej cenie")
plt.axvline(dane['Cena'].median(axis=0), color='violet', linewidth=3)
plt.text(dane['Cena'].median(axis=0),10,"Mediana",rotation=90, color = 'violet')
plt.axvline(dane['Cena'].mean(axis=0), color='c', linewidth=3)
plt.text(dane['Cena'].mean(axis=0),10,"Srednia",rotation=90, color = 'c')
plt.show()

print("\nWidać, że jedno futro cenowo bardzo odstaje. Jest również kilka futer powyżej 1000 zł, jednak większość mieści się w przedziale 0-1000 zł.\n"
      "Przez te kilka futer rozrzut cenowy jest prawie tak duży jak sama średnia, odrzućmy więc te futra z najwyżej półki\n"
      "i powiedzmy, że chcemy wydać max 700 zł, czyli nieco więcej niż nasza mediana. Ile jest takich futer?\n")
tansze_futra = (dane[dane['Cena']<=700])
print(len(tansze_futra))
print("\nCzyli zostało nam {}% wszystkich futer...uff...już trochę mniejszy zawrót głowy !".format(len(tansze_futra)/len(dane['Cena'])*100))
print("\nZobaczmy raz jeszcze jak tym razem wygląda:\n")
print("Wykres 2 - histogram futer do 700 zł\n")
plt.hist(tansze_futra["Cena"],bins=5, label="")
plt.title("Wykres 2\nRozkład cen sztucznych futer do 700zł\n")
plt.xlabel("Cena futra")
plt.ylabel("Ilość futer w danej cenie")
plt.axvline(tansze_futra['Cena'].median(axis=0), color='violet', linewidth=3)
plt.text(tansze_futra['Cena'].median(axis=0),10,"Mediana",rotation=90, color = 'violet')
plt.axvline(tansze_futra['Cena'].mean(axis=0), color='c', linewidth=3)
plt.text(tansze_futra['Cena'].mean(axis=0),10,"Srednia",rotation=90, color = 'c')
plt.show()

print("Jak widać średnia i mediana są prawie równe, możemy wybierać więc z futer porównywalnych cenowo.\n"
      "Co jest zatem jeszcze dla nas ważne przy wyborze idealnego prezentu?\n"
      "Nie bez znaczenia jest oczywiście marka futra !\n"
      "Przyjmijmy, że nie chcemy kupować marki, która proponuje nam tylko jeden rodzaj futra,\n"
      "wszak są one w tym sezonie modne, więc musimy wybierać z marek, które podążają za trendami ;-)\n"
      "Zobaczmy najpierw jakie w ogóle marki mamy do wyboru:\n")

zestawienie_marek = pd.DataFrame(tansze_futra.groupby(['Marka'])["Marka"].count())
print(zestawienie_marek)

print("\nNo, trochę ich jest, ale widzimy, że dużo z nich proponuje po 1 sztuce - usuńmy te firmy z naszej listy i pokażmy raz jeszcze:\n")

zestawienie_marek.columns=["Zestawienie"]
zestawienie_marek=(zestawienie_marek.where(zestawienie_marek["Zestawienie"]>1).dropna()).index
tansze_futra = tansze_futra.where(tansze_futra["Marka"].isin(zestawienie_marek)).dropna().sort_values(by="Marka")
print(tansze_futra)

print("\nW sumie dalej w grze jest {} futer.\n"
      "To i tak lepiej niż {}, które mieliśmy na początku\nNo ok, ale jak jeszcze zawęzić sobie wybór?\n"
      "Zobaczmy jakie futra są w promocji, w końcu po co przepłacać:\n".format(len(tansze_futra),(len(dane))))

tansze_futra_w_promocji = tansze_futra.where(tansze_futra["Promocja"]>0).dropna()
print(tansze_futra_w_promocji)

print("\nW promocji mamy dostępne {} futer z naszej puli.\nCiekawe, czy promocja zależy od ceny futra. Jeśli tak, może opłaci nam się kupić droższe, bo więcej zaoszczędzimy;-)\n"
      "Zobaczmy to na wykresie:\nWykres 3 - Zależność upustu od ceny początkowej".format(len(tansze_futra_w_promocji)))
cena_poczatkowa = tansze_futra_w_promocji["Cena"]+tansze_futra_w_promocji["Promocja"]
plt.scatter(cena_poczatkowa,tansze_futra_w_promocji["Promocja"], color = "c")
plt.title("Wykres 3\nZależność upustu od ceny początkowej\n")
plt.xlabel("Cena początkowa futra")
plt.ylabel("Upust ceny")
plt.show()
print("\nCoś tam niby wyszło - ale czy jest to silna zależność? Poprowadźmy linię regresji:\nWykres 4 - Zależność upustu od ceny początkowej wraz z linią regresji")
plt.scatter(cena_poczatkowa,tansze_futra_w_promocji["Promocja"], color = "c")
fit = np.polyfit(cena_poczatkowa, tansze_futra_w_promocji["Promocja"], deg=1)
plt.plot(cena_poczatkowa, fit[0] * cena_poczatkowa + fit[1], color='red')
plt.title("Wykres 4\nZależność upustu od ceny początkowej\n")
plt.xlabel("Cena początkowa futra")
plt.ylabel("Upust ceny")
plt.show()
print("Nie jest źle. Ale wybierzmy może inną strategię - zobaczmy dla których futer obniżka jest największa:\n")
obnizka = (pd.DataFrame(tansze_futra_w_promocji["Promocja"]/cena_poczatkowa)).sort_values(by=[0], ascending=False)

print(obnizka.head())
# na dzień 30.11 faktycznie 1 towar był obniżony o 50%, ale jeśli generuje się dane innego dnia, wynik może być inny !
# w każdym razie kod powinien umożliwić pracę z futrami na bieżąco, mimo że aż taka okazja może nam się nie trafić ;-)
print("\nMamy jedną 50% obniżkę. Takiej okazji nie można przegapić !\n"
      "Nasz wybór jest już raczej przesądzony, zobaczmy zatem co to za artykuł:\n"
      "(jednak, żeby nie było cienia wątpliwości, że wybraliśmy prezent samodzielnie, poniżej jest czas na Twój ruch !)")
numer = int(input("Wpisz numer indeksu finałowego artykułu:\t"))
print("TADADAM ! Oto najlepszy atrykuł, który wybrał dla Ciebie nasz mały programik w pythonie:\n\n{}"
      "\n\nNie wiadomo, czy spodoba się odbiorczyni prezentu, wszak nie ocenialiśmy artykułów pod względem estetycznym, \n"
      "wiadomo jednak, że nikt nie będzie mógł Ci zarzucić, że był to wybór nieprzemyślany ;-D\n\n"
      "Autorka programu dziękuje za uwagę i życzy wszystkim trafionych prezentów !".format(tansze_futra_w_promocji[tansze_futra_w_promocji.index==numer]))


##########################################################################



