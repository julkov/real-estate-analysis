### Wytyczne do projektu zaliczeniowego


W ramach projektu zaliczeniowego należy:
- [x] Zebrać dane z jednego serwisu z ofertami nieruchomości.
- [x] Wyciągnąć i oczyścić dane. (im więcej tym lepiej)
- [x] Wyciągnąć z tekstu ogłoszenia conajmniej jedną dodatkową zmienną, która może wpływać na cenę nieruchomości (jak bliskość do morza, bliskość budynków użyteczności publicznej itp., użyć klasycznej metody słowniczkowej, nie llm)
- [ ] Zbudować model regresji liniowej na podstawie zebranych danych do szacowania ceny nieruchomości na podstawie wybranych parametrów (Jeżeli, ktoś chcę dorzucić dodatkowy model np. oparty o lasy losowe to też na plus, aplikacja może wtedy szacować dwa wyniki).
- [ ] Napisać PROSTY i krótki raport, który będzie zawierał (taki analityczny dla osób, które wiedzą co czytają):
- [ ] Opis procesu zbierania danych (ile było ogłoszeń, ile się udało zebrać), 
- [ ] Eksploracyjną analize danych
- [ ] Zastosowane transformacje zmiennych (podstawowe statystyki deskryptywne, rozkłady zmiennych)
- [ ] Historia budowy modelu regresji (+ diagnostyka modelu)
- [ ] Końcowy model regresji, który został użyty w aplikacji
- [ ] Krótki opis taki bardziej popularno-naukowy (też techniczny ale mniej, bardziej przystępny dla osób, które nie siedzą mocno w analizie danych i programowaniu). Może być zaliczone jako .md na Githubie (Najlepiej po ang.)
- [ ] Zbudować proste i ładne GUI (np. w przy użyciu biblioteki flet, na której robiliśmy przykłady na zajęciach), który będzie zawierał:
- [ ] Odpowiednie pola do wprowadzania danych wraz z walidacją tych danych (np. tam gdzie należy wprowadzić liczbę nie powinno być możliwości wprowadzenia tekstu).
- [ ] Miejsce gdzie, będzie się wyświetlał poprawnie oszacowany wynik modelu regresji. Czyli cena nieruchomości 
- [ ]  Dodatkowo należy:
- [ ] Napisać podstawowe testy jednostkowe do skryptów (dorzucenie kilku testów integracyjnych na plus, proszę pilnować odpowiednie nazewnictwa, a gdy używamy parametryzacji to "ids") 
- [ ] Przesłać w osobnym pliku wygenerowaną dokumentacje kodu (.html lub .pdf) - do tego należy konsekwentnie stosować doc-stringi
- [ ] Autor, licencja, ma się pojawić zarówno w kodzie jak i w dokumentacji
- [ ] Kod ma być zgodny z PEP 8 (chyba, że w jakimś miejscu nie ma to sensu). 
- [ ] Kod ma być napisany w stylu obiektowym, nie proceduralnym (funkcje, klasy)
- [ ] EDA w ładnie opisanym notebooku
* do tego miejsca obowiązkowe - takie minimum na zaliczanie.

Dodatkowo: 
- [ ] Projekt wrzucony na GitHuba (bez baz danych i źródeł stron - compliance) z ładnym opisem, instrukcją, gifami itd.
- [ ] Miejsce, gdzie będą wyświetlały się historyczne oszacowania z możliwością ich "wyczyszczenia". (tak aby program pamiętał te wyniki po zresetowaniu, więc należy albo dane zapisywać do csv albo jeszcze lepiej zrobić prostą bazę sql'a (najlepiej taką, która przy odpaleniu programu będzie sprawdzana czy istnieje i jak jej program nie znajdzie to będzie nową tworzyć bazę razem z tabelami)
- [ ] Możliwość szacowania ceny bez wprowadzenia wszystkich informacji przez użytkownika (podpowiedź, np. wiele modeli)
- [ ] Możliwość podania parametrów nieruchomości i ceny, a następnie na tej postawie wskazanie czy cena jest okazyjna, przeciętna czy za wysoka
- [ ] Wykorzystanie prostej inżynierii cech (jak wyciągnięcie długości opisu czy policzenie ilości zdjęć)
- [ ] Podawanie widełek cenowych, oprócz punktowego oszacowania
Dodatkowe elementy, za które można zdobyć dodatkowe punkty: 
- [ ] animacje (np. lottie mile widziane)
- [ ] pełna responsywność (tak, że na telefonie i komputerze aplikacja będzie wyglądać dobrze, niezależnie od wielkości ekranu)
- [ ] wibracje przy klikaniu
- [ ] dodanie do modelu możliwości szacowania na podstawie informacji ze zdjęć (o ile będzie miało to sens, można użyć PCA lub AE (AE wyżej punktowany))
- [ ] tworzenie i zapisywanie logów (kto, jak i kiedy używał tego programu - takie info może być zapisywane w pliku .log lub w osobnej tabeli w sql'u). Użytkownik aplikacji nie powinien tego widzieć, ale może być mała ikonka, żeby był dostęp z poziomu GUI.


- [ ] Kilka dodatkowych protipów:
- [ ] Aplikacja ma być idioto-odporna, użytkownik nie może mieć możwilości jej popsuć z poziomu interfejsu
- [ ] Oszacowania powinny być w sensownym zakresie (np. nie powinno się dać wprowadzić takiej kombinacji parametrów, że użytkownik dostanie ujemne oszacowanie))
- [ ] Aplikacja powinna posiadać intuicyjny layout (warto po skończeniu dać komuś telefon do ręki z uruchomioną aplikacją i zobaczyć w jaki sposób z niej korzysta)
- [ ] Proszę również zadbać o estetykę aplikacji
Kodu aplikacji nie trzeba kompilować!
 
Przy przesyłaniu zadania bardzo proszę wszystkie skrypty, pliki i bazy spakować do archiwum (zip, gzip, rar lub jakikolwiek inny) i w takiej formie przesłać (ale BEZ wirtualnego środowiska). Dodatkowo proszę o plik z opisem poszczególnych plików (w .md).
Bazy, surowe pliki też należy dorzucić (najlepiej w osobnych folderach)
Jeżeli coś z tego jest nie jasne to proszę o informację. 

Przypominam również, że jeżeli ktoś ma jakikolwiek problem związany z zadaniami lub z projektem zaliczeniowym to proszę pisać, zawsze też możemy się umówić na konsultacje.

Zadanie po przesłane po terminie startuje z niższej oceny, we wrześniu, jeszcze z niższej.. (Chyba, że ktoś da znać wcześniej lub będzie miał dobry powód, sytuacje mniej lub bardziej losowe każdemu mogą się zdarzyć).

Myślcie o tym projekcie, jako o własnej wizytówce.

Miłego klikania! 🔥🔥🔥🔥🔥

 