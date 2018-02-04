"""
VARIABLE DESCRIPTIONS:
survival        Survival
                (0 = No; 1 = Yes)
pclass          Passenger Class
                (1 = 1st; 2 = 2nd; 3 = 3rd)
name            Name
sex             Sex
age             Age
sibsp           Number of Siblings/Spouses Aboard
parch           Number of Parents/Children Aboard
ticket          Ticket Number
fare            Passenger Fare
cabin           Cabin
embarked        Port of Embarkation
                (C = Cherbourg; Q = Queenstown; S = Southampton)

SPECIAL NOTES:
Pclass is a proxy for socio-economic status (SES)
 1st ~ Upper; 2nd ~ Middle; 3rd ~ Lower

Age is in Years; Fractional if Age less than One (1)
 If the Age is Estimated, it is in the form xx.5

With respect to the family relation variables (i.e. sibsp and parch)
some relations were ignored.  The following are the definitions used
for sibsp and parch.

Sibling:  Brother, Sister, Stepbrother, or Stepsister of Passenger Aboard Titanic
Spouse:   Husband or Wife of Passenger Aboard Titanic (Mistresses and Fiances Ignored)
Parent:   Mother or Father of Passenger Aboard Titanic
Child:    Son, Daughter, Stepson, or Stepdaughter of Passenger Aboard Titanic

Other family relatives excluded from this study include cousins,
nephews/nieces, aunts/uncles, and in-laws.  Some children travelled
only with a nanny, therefore parch=0 for them.  As well, some
travelled with very close friends or neighbors in a village, however,
the definitions do not support such relations.
"""
###################### Projekt stworzony w Anaconda3
import pandas as pd

print("--------------------------------------------------------------------------------------------\n"
      "Tragedia Titanica jest chyba najbardziej znanym wypadkiem statku pasażerskiego w dziejach.\n"
      "Ci, którzy go przeżyli, mogli się na pewno nazywać szczęściarzami, zastanówmy się jednak,\n"
      "czy są takie czynniki, które temu szczęściu mogły nieco pomóc.\n\nBędziemy operować na danych pasażerów statku.\n")

try:
    train = pd.read_csv("train.csv")
except:
    print("nie udało się zaimportować niezbędnych plików, sprawdź adres źródłowy")

print("Zobaczmy, jak wyglądają nasze dane:\n")
print(train.head(), "\n")
print("Jak widać, część z danych prawdopodobnie nam się nie przyda - możemy założyć, że ani numer biletu ani port,\n"
      "z którego ktoś wyruszył nie wpłynął na jego możliwość przeżycia tragedii, usuńmy więc niepotrzebne kolumny\n")
train = train.drop(["PassengerId", "Name", "Ticket", "Embarked", "Cabin"], axis=1)
print("Zobaczmy nasze dane raz jeszcze:\n")
print(train.head(), "\n")

print("Aby stworzyć model przewidujący zdolność przeżycia pasażera (w końcu nigdy nie wiadomo, co może się nam przydać !)\n"
      "zobaczmy najpierw, jakie cechy mogą ją dobrze przewidywać. Usunęliśmy już te, które na zdrowy rozsądek wydawały nam\n"
      "się bez znaczenia. Policzmy teraz dla pozostałych cech korelację, aby zobaczyć, jakie ostatecznie weźmiemy pod uwagę.\n")

from scipy.stats import pearsonr
correlation_for_Pclass = pearsonr(train["Pclass"], train["Survived"])
print("Zależność przeżywalności od klasy, w której podróżował pasażer wynosi {}".format(round(correlation_for_Pclass[0],3)))
train["Sex"] = pd.get_dummies(train["Sex"]) # zamieniamy zmienną jakosciową na ilościową
correlation_for_Sex = pearsonr(train["Sex"], train["Survived"])
print("Zależność przeżywalności od płci {}".format(round(correlation_for_Sex[0],3)))
train["Age"] = train["Age"].replace("nan", train["Age"].median()) # z uwagi na brakujące wartości
correlation_for_Age = pearsonr(train["Age"], train["Survived"])
print("Zależność przeżywalności od wieku {}".format(round(correlation_for_Age[0],3)))
correlation_for_SibSp = pearsonr(train["SibSp"], train["Survived"])
print("Zależność przeżywalności od obecności rodzeństwa lub małżonka, z którymi się podróżowało {}".format(round(correlation_for_SibSp[0],3)))
correlation_for_Parch = pearsonr(train["Parch"], train["Survived"])
print("Zależność przeżywalności od obecności rodziców lub dzieci, z którymi się podróżowało {}".format(round(correlation_for_Parch[0],3)))
correlation_for_Fare = pearsonr(train["Fare"], train["Survived"])
print("Zależność przeżywalności od ceny biletu {}\n".format(round(correlation_for_Fare[0],3)))

print("Ok, widzimy, że szansa przeżycia jest najbardziej skorelowana z płcią, klasą oraz ceną biletu.\n"
      "Cena biletu wydaje się być jednak mocno zależna od klasy podróżowania, zobaczmy więc związek między tymi dwoma cechami:\n")

correlation_for_FP = pearsonr(train["Fare"], train["Pclass"])
print("Zależność przeżywalności od ceny biletu {}\n".format(round(correlation_for_FP[0],3)))

print("Korelacja nie jest jednak aż tak duża, jakby się mogło wydawać - jedynie 55%, cechy te nie są więc ze sobą tożsame -\n"
      "zostawmy obydwie w naszej tabeli danych.\n"
      "Zanim zabierzemy się dalej do działania policzmy ile ogólnie pasażerów przeżyło katastrofę - \n"
      "będziemy mogli odnosić się do tej liczby w dalszych rozważaniach\n")

all_alive = (train["Survived"].where(train["Survived"] == 1)).count()
all_died = (train["Survived"].where(train["Survived"] == 0)).count()
all = all_alive + all_died

print("Katastrofę przeżyło {} % pasażerów.\n".format(round((all_alive/all)*100,3)))

print("Przyjrzyjmy się poszczególnym zmiennym - na warsztat weźmy najpierw płeć, która była najbardziej skorelowana z przeżywalnością.\n"
      "Zobaczmy jak rozkłada się liczba pasażerów obu płci i ile przeżyło kobiet a ile mężczyzn\n")

men = len(train.loc[train["Sex"] == 0])
women = len(train.loc[train["Sex"] == 1])
print("Podróż statkiem odbywało {0} kobiet i {1} mężczyzn.\n".format(women, men))
sex_survival = train.groupby(["Sex"]).sum()
print(sex_survival, "\n")
print("0 to mężczyźni, 1 to oznaczenie kobiet. Z tabeli widzimy, że kobiet przeżyło ponad dwa razy więcej niz mężczyzn,\n"
      "chociaż było ich prawie dwa razy mniej niż mężczyzn - w sumie przeżyło {0}% kobiet i {1}% mężczyzn.\n"
      "Mężczyźni w sumie byli dwa razy starsi od kobiet - średnio mężczyzna miał {2}, a kobieta {3} lat.\n"
      "Jednak być może o przeżywalności kobiet mogła bardziej decydować klasa, którą podróżowały niż ich płeć - tu na\n"
      "średnio mężczyzna podróżował w klasie {4}, a kobieta - {5}.\n"
      .format(round((233/women)*100), round((109/men)*100), round(17391/men), round(8770/women), round(1379/men), round(678/women)))

print("Zobaczmy zatem kto podróżował jaką klasą:\n")
pclass_survival = train.groupby(["Pclass"]).sum()
print(pclass_survival, "\n")

print("Biorąc pod uwagę poprzednie obliczenia, sama klasa nie decydowała tu chyba o pierwszeństwie w byciu ratowanym -\n"
      "Jak widać, osoby podróżujące klasą 3 przeżyły w prawie takim samym stopniu jak podróżujący klasą 1.\n"
      "Czy w takim razie jest to czynnik zupełnie bez znaczenia? Nie koniecznie, dlatego, że widzimy, że spośród 136 uratowanych\n"
      "pasażerów klasy 1 'tylko' 94 to kobiety, zatem na szalupy ratunkowe musiało zmieścić się nieco mężczyzn podróżujących klasą\n"
      "pierwszą, natomiast nie wszystkie kobiety z klasy 3 udało się uratować. A jak wiek mógł wpłynąć na szansę przeżycia?\n")

bins = [0, 10, 20, 30, 40 ,50, 60, 70, 80, 90, 100]
age_survival = train.groupby(pd.cut(train["Age"], bins)).mean()
print(age_survival.sort_values(by="Survived", ascending=False),"\n")
print("W tabeli widzimy średnie wartości każdej zmiennej, natomiast wyniki uszeregowane są od wieku, w który najbardziej sprzyjał\n"
      "byciu uratowanym. Jak widać, na pierwszym miejscu ratowano dzieci do lat 10, następnie największe szczęście mieli pasażerowie w wieku 50-60\n"
      "a tuż za nimi 40-50-latkowie i nastolatkowie. Najgorsze szanse miały osoby po 60 roku życia, chociaż wśród nich są osoby, \n"
      "które zapłaciły za bilet średnio 25 jak i 45 oraz podróżowały przeważnie 1 lub 2 klasą- wydaje się zatem, że w przypadku \n"
      "osób starszych nie miało to żadnego znaczenia ile ktoś zapłacił za podróż - dzieci wszak średnio podróżowały klasą najgorszą.\n"
      "A jak na na szanse przeżycia wpływała obecność rodziny? Możemy podejrzewać, że dzieci do 10 roku życia podróżowały na pewno z \n"
      "rodzicami, usuńmy ich więc z listy pasażerów, których będziemy teraz brać pod uwagę:\n")

only_adults = train.loc[train["Age"]>10]
parch_survival = only_adults.groupby(["Parch"]).mean()
print(parch_survival, "\n")
print("Największą szansę przeżycia miały osoby, które miały na pokładzie 3 bliskie osoby - rodziców lub dzieci.\n"
      "Być może w większości są to po prostu matki, które były ratowane wraz ze swoimi dziećmi, co możemy wyczytać z kolumny\n"
      "dotyczącej płci - w 8 na 10 przypadków osobami uratowanymi, które miały 3 bliskie osoby były kobiety, średnio 33 letnie.\n")

sibsp_survival = train.groupby(["SibSp"]).mean()
print(sibsp_survival, "\n")
print("Jak widać w powyższej tabeli, najlepiej było mieć 1 bliską osobę na pokładzie - kogoś z rodzeństwa lub męża/żonę. Najlepszy wskaźnik\n"
      "mają jednak osoby, które miały tylko 1 taką osobę, przy większej ich liczbie możliwość przeżycia spada. Być może byli to mężowie/żony\n"
      "z dziećmi, którzy ze względu na swoje pociechy byli ratowani w pierwszej kolejności - może to potwierdzać średnia wieku takich osób - \n"
      "29 lat, co jest bardzo zbliżone do średniej wieku kobiet z poprzednej tabeli.\n\n"
      "Podsumowując nasze dotychczasowe analizy możemy postawić hipotezę, że najlepiej było być dzieckiem do lat 10, jeśli jednak było się starszym,\n"
      "lepiej było być kobietą (najlepiej z tym dzieckiem do lat 10), kto nie miał tyle szczęścia, mógł jeszcze uratować się będąc mężem kobiety\n"
      "(z tym dzieckiem), jeśli jednak był kawalerem, to najlepiej, aby podróżował pierwszą klasą. To taka mała ściągawka dla wszystkich, którzy\n"
      "w najbliższym czasie wybierają się na rejs statkiem w okolice koła podbiegunowego;-).\n\n"
      "Ok, poznaliśmy nieco bliżej nasze zmienne, stwórzmy teraz model, który będzie nam mógł przewidzieć zdolność przeżycia katastrofy.\n"
      "Na początku skorzystamy z drzewa decyzyjnego:\n")

# dzielimy dane na testowe i treningowe
train_data = train[:500]
test_data = train[:500]
x_train = train_data.drop(["Survived"], axis=1)
y_train = train_data["Survived"]
x_test = test_data.drop(["Survived"], axis=1)
y_test = test_data["Survived"]

from sklearn import preprocessing
x_train = preprocessing.scale(x_train)
x_test = preprocessing.scale(x_test)

from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier()
forest = forest.fit(x_train, y_train)
prediction = forest.predict(x_test)
accuracy = forest.score(x_test, y_test)
print("Dokładność naszego modelu przewidywania jest równa: {}\nSprawdźmy teraz metodę Knajbliższych sąsiadów:\n"
      .format(accuracy))

from sklearn.neighbors import KNeighborsClassifier
knc = KNeighborsClassifier(n_neighbors=5)
knc = knc.fit(x_train, y_train)
prediction = knc.predict(x_test)
accuracy = knc.score(x_train, y_train)
print("Dokładność modelu k najbliższych sąsiadów to: {}. Dużo gorzej niż w poprzednim modelu. \n"
      "Na koniec sprawdźmy jeszcze regresję liniową:\n"
      .format(accuracy))

from sklearn.linear_model import LinearRegression
regression = LinearRegression()
regression = regression.fit(x_train, y_train)
prediction = regression.predict(x_test)
accuracy = regression.score(x_train, y_train)
print("Dokładność modelu regresji liniowej to: {}. No cóż, nie wiadomo, czy w przypadku regresji bardziej można liczyć na szczęście\n"
      "czy na trafność modelu. Tak czy inaczej, autorka ma nadzieję, że nikt nie znajdzie się w sytuacji, w której będzie\n"
      "potrzebował skorzystać z któregokolwiek z naszych modeli;-) \n".format(accuracy))