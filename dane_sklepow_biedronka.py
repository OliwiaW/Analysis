import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

#############################################################################################
# funkcja generująca dane dla każdego sklepu
# plik jest już wygenerowany, z uwagi na to, że długo się tworzy można ominąć czekanie i skorzystać z gotowego w projekcie
# albo odkomentować tą część kodu i utworzyć plik jeszcze raz samemu
"""
def sklep(ID_SKLEPU):
    adres_= ("http://www.biedronka.pl/pl/shop,id,"+str(ID_SKLEPU))
    nasze_dane = requests.get(adres_)
    soup = BeautifulSoup(nasze_dane.content, "html.parser")

    Miasto = soup.find_all("h4")[0].text.split('\n')[1]
    if Miasto=="":
        Miasto="None"
        # w niektórych sklepach nie ma pełnych danych, stąd zabezpieczenie, żeby potem ładnie się nam to załadowało w odpowiednie kolumny
    Adres = soup.find_all("h4")[0].text.split("\n")[2]
    if Adres=="":
        Adres="None"

    Bankomat = soup.find_all("ul", "shop-details")[0].text.split("\n")[2]
    if Bankomat=="":
        Bankomat = "None"
    if Bankomat=="Sklep z wypiekiem":
        Bankomat="None"

    Piekarnia = soup.find_all("ul", "shop-details")[0].text.split("\n")[3]
    if Piekarnia=="":
        Piekarnia="None"
    if (soup.find_all("ul", "shop-details")[0].text.split("\n")[2])=="Sklep z wypiekiem":
        Piekarnia = "Sklep z wypiekiem"

    for link in soup.find_all('a'):
        if "lng" in link.get('href'):
            Latitude =(link.get('href').split(","))[2]
    if Latitude=="":
        Latitude="None"

    for link in soup.find_all('a'):
        if "lng" in link.get('href'):
            Longitude=(link.get('href').split(","))[4]
    if Longitude=="":
        Longitude="None"

    wektor = (str(ID_SKLEPU)+";"+Miasto+";"+Adres+";"+Bankomat+";"+Piekarnia+";"+Latitude+";"+Longitude)
    return wektor

#generowanie danych dla każdego sklepu
tab = []
for i in list(range(2,2776)):#2776 jest chyba maksymalnie
    try:
        tab.append(sklep(i))
    except:
        pass

#zapisywanie danych do pliku
try:
    with open("plik_dodatkowy.txt", "w") as plik:
        plik.write("\n".join(map(str, tab)))
except:
    print("nie ma takiego pliku")

print("\n Plik powinien zostać wygenerowany\n")
"""""
####################################################################################################
print("\nPopracujmy sobie nieco z danymi, na początku wczytujemy dane z pliku i tworzymy macierz danych\n")

dane = []
try:
    plik = open("plik_dodatkowy.txt")
    for line in plik:
        dane.append(line.split(sep=";"))
except:
    print("nie ma takiego pliku")

dane = pd.DataFrame(dane)
print("Ok, dane wczytane, zobaczmy teraz jak one wyglądają:\n")
print(dane.head())
print("\nTo jedynie pierwsze wiersze danych, sprawdźmy zatem jakie wymiary ma cała tablica\n")
print(dane.shape)

print("\nMoże na początku sprawdźmy jak na 'mapie' rozkładają się nasze Biedronki. Skorzystajmy z wykresu punktowego, by zobaczyć ich zagęszczenie")
x=dane.loc[dane[5]!="None"][5]
y=dane.loc[dane[6]!="None"][6]
plt.scatter(x,y)
plt.xlabel("Szerokość geograficzna")
plt.ylabel("Wysokość geograficzna")
plt.title("Wykres 1")
plt.show()

print("\nWykres 1\n")

print("\nCzas pobawić się danymi, wygenerujmy sobie teraz dla każdej biedronki jakieś losowe dane, niech będzie to np. dzienny utarg\n")
print("Żeby było wesoło, załóżmy, że biedronki cieszą się różną popularnością i dzienny utarg może wynosić od 5 tys do 30 tys.\n")
print("Nowe dane umieścimy w dodatkowej, 7. kolumnie\n")

dane.loc[:][7]=None # tworzymy kolumnę, którą zaraz wypełnimy mnóstwem pieniędzy !
i=0
while i<len(dane):
    dane.loc[i][7] =((np.random.random_integers(5000, high=30000)))
    i+=1

print(dane.head())
print("\nOk, mamy już jakieś przykładowe liczby, to może zobaczmy jaki jest średni dzienny utarg\n")
srednia = np.average(dane[7])
print("Dziennie srednio Biedronka zarabia "+str(srednia)+" zł.\n")
print("\nTrochę ciężko pracuje się jednak na danych aż tylu Biedronek. Ograniczmy nasz zbiór do 3 miast: Szczecina, Warszawy i Lublina\n")
kopia_danych = dane.copy() # coby nie zniszczyć naszych poprzednich danych, moze się komuś przydadzą
del kopia_danych[2] # dokładny adres nie będzie już nam potrzebny
Szczecin = kopia_danych[kopia_danych[1] == "Szczecin"]
Szczecin.set_index(1)
del Szczecin[0]

Warszawa = kopia_danych[kopia_danych[1] == "Warszawa"]
Warszawa.set_index(1)
del Warszawa[0]

Lublin = kopia_danych[kopia_danych[1] == "Lublin"]
Lublin.set_index(1)
del Lublin[0]

print("Oto pierwsze wiersze danych ze Szczecina:\n")
print(Szczecin.head())
print("\nTu widzimy Warszawę:\n")
print(Warszawa.head())
print("\nA teraz szybki rzut okiem na Lublin:\n")
print(Lublin.head())

#############################################################################################################

print("\nPorównajmy te 3 miasta na wykresie - w którym mieście Biedronka ma największy zysk?:\n")

srednie = [np.average(Szczecin[7]), np.average(Warszawa[7]), np.average(Lublin[7])]
miasta = [1,2,3]
labels =["Szczecin", "Warszawa", "Lublin"]
plt.bar(miasta, srednie, align="center")
plt.xlabel("Miasta")
plt.ylabel("Średni dzienny dochód wszystkich sklepów w mieście")
plt.title("Wykres 2")
plt.xticks(miasta, labels)
plt.show()

print("\nWykres 2\n")

print("\nZobaczmy teraz, czy dzienny utarg w danym mieście zależy od tego ile sklepów Biedronki możemy w nim odwiedzić\n")

ile = [len(Warszawa), len(Szczecin),len(Lublin)]

plt.plot(ile, srednie)
plt.xlabel("Ilość sklepów w danym mieście")
plt.ylabel("Średni dzienny dochód wszystkich sklepów w mieście")
plt.title("Wykres 3")
plt.show()

print("\nWykres 3\n")
print("Oczywiście nie musiało nic sensownego wyjść - dane są wszakże wygenerowane losowo;-)")

print("\nWróćmy jeszcze na chwile do naszych pierwotnych danych. W końcu mamy je dalej zapisane;-) \n"
      "Sprawdżmy ile w ogóle biedronek w Polsce, które nie mają Bankomatów lub wypiekanych na miejscu świeżych bułeczek")

ile_bez_bankomatu = len((dane.loc[dane[3] == "None"]))
ile_bez_piekarni = len((dane.loc[dane[4] == "None"]))
print("\nMamy "+str(ile_bez_bankomatu)+" sklepów bez bankomatów oraz "+ str(ile_bez_piekarni)+" sklepów bez piekarni.\n")
print("To "+str(int((ile_bez_bankomatu/len(dane))*100))+" % i "+ str(int((ile_bez_piekarni/len(dane))*100)) +" % wszystkich sklepów w całej Polsce. \nLiczby do nas nie przemawiają? Zobaczmy to na wykresie !\n")

cz1=[ile_bez_bankomatu, len(dane)]
cz2=[ile_bez_piekarni, len(dane)]
labels1 = ["Sklepy bez bankomatu", "Sklepy z bankomatem"]
labels2= ["Sklepy bez piekarni","Sklepy z piekarnią"]
plt.pie(cz1, labels=labels1, colors=["r","g"], autopct="%1.1f%%")
plt.title("Wykres 4")
plt.show()
print("\nWykres 4\n")
plt.pie(cz2, labels=labels2, colors=["r","g"], autopct="%1.1f%%")
plt.title("Wykres 5")
plt.show()
print("\nWykres 5\n")

print("To już koniec, życzę miłego dnia i pozdrawiam !\n")



