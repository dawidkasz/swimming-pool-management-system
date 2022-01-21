# Dokumentacja

## Instalacja
1. Sklonować repozytorium.<br>
    `git clone https://gitlab-stud.elka.pw.edu.pl/dkaszyns/swimming-pool-management-system.git`
2. Zainstalować wymagane zależności z pliku [requirements.txt](../../requirements.txt).<br>
   Przykład:<br>
   - `python3 -m venv venv`
   - `source ./venv/bin/activate`
   - `pip install -r requirements.txt`
3. Utworzyć zmienną środowiskową o nazwie `SWIMMING_POOL_MANAGEMENT_SYSTEM_SECRET_KEY` zawierającą sekretny klucz wykorzystywany przez Django.<br>
    Klucz można wygenerować online [djecrety.ir](https://djecrety.ir/) lub bezpośrednio z poziomu konsoli.<br>
   Przykład generowania sekretnego klucza:
   - `python3 manage.py shell`
   - `from django.core.management.utils import get_random_secret_key`
   - `get_random_secret_key()`

    <br>Wygenerowany klucz należy umieścić w zmiennej środowiskowej:<br>
    `export SWIMMING_POOL_MANAGEMENT_SYSTEM_SECRET_KEY='<wygenerowany_klucz>'`

4. Wykonać migrację w celu utworzenia utworzenia odpowiedniej struktury bazy danych.<br>
   `python3 manage.py migrate`

## Uruchomienie
W celu uruchomienia aplikacji należy wykonać polecenie `python3 manage.py runserver <opcjonalny_adres>`.<br>
Domyślnie serwer będzie działał na `http://127.0.0.1:8000/`.

W momencie uruchomienia produkcyjnego, należy pamiętać o ustawieniu parametru `DEBUG = False`
w pliku [settings.py](../../swimming_pool_management_system/settings.py)


## Testowanie
Aby uruchomić testy należy wykonąc polecenie `python3.9 manage.py test` lub `python3.9 manage.py test <nazwa_aplikacji>`, w momencie gdy <br>
chcemy przetestować tylko i wyłącznie jeden moduł.

Wszystkie developerskie zależności z pliku [requirements-dev.txt](../../requirements-dev.txt)
można zainstalować poprzez `pip install -r requirements-dev.txt`

Domyślnie wykorzystywanym linterem jest [flake8](https://flake8.pycqa.org/en/latest/)
wraz z następującą [konfiguracją](../../.flake8).<br>