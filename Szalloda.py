from datetime import datetime, timedelta

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=10000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=15000)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def ellenoriz_datum(self, foglalasok):
        for foglalas in foglalasok:
            if foglalas.szoba == self.szoba and foglalas.datum == self.datum:
                return False
        return True

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def hozzaad_foglalhato_szoba(self, szobaszam, ar, felhasznalo_tipus, jelszo=None):
        if felhasznalo_tipus == "ugyfel":
            print("Nincs jogosultsága új szobát hozzáadni.")
            return

        if felhasznalo_tipus == "alkalmazott" and jelszo != "qwe123":
            print("Hibás jelszó. Nincs jogosultsága új szobát hozzáadni.")
            return

        szoba = Szoba(szobaszam, ar)
        self.szobak.append(szoba)

    def hozzaad_szoba(self, szoba):
        self.szobak.append(szoba)

    def listaz_foglalhato_szobakat(self, felhasznalo_tipus, jelszo=None):
        if felhasznalo_tipus == "alkalmazott" and jelszo != "qwe123":
            print("Hibás jelszó. Nincs jogosultsága foglalható szobákat listázni.")
            return

        print("Foglalható szobák:")
        for szoba in self.szobak:
            print(f"Szoba száma: {szoba.szobaszam}, Ár: {szoba.ar}")

    def foglalas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                print("A szoba már foglalt ebben az időpontban.")
                return None

        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum)
                if not foglalas.ellenoriz_datum(self.foglalasok):
                    print("A szoba már foglalt ebben az időpontban.")
                    return None
                self.foglalasok.append(foglalas)
                return foglalas.szoba.ar

        print("Hibás szobaszám, kérjük, válasszon elérhető szobát.")
        return None

    def lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        return False

    def listaz_foglalasokat(self):
        for foglalas in self.foglalasok:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

# adatok feltöltése
szalloda = Szalloda("Pihenő Hotel")
szalloda.hozzaad_szoba(EgyagyasSzoba(szobaszam=101))
szalloda.hozzaad_szoba(KetagyasSzoba(szobaszam=201))
szalloda.hozzaad_szoba(EgyagyasSzoba(szobaszam=102))
szalloda.hozzaad_szoba(KetagyasSzoba(szobaszam=202))
szalloda.hozzaad_szoba(EgyagyasSzoba(szobaszam=103))

datumok = [datetime(2023, 12, 1), datetime(2023, 12, 5), datetime(2023, 12, 10), datetime(2023, 12, 15), datetime(2023, 12, 20)]

for i in range(5):
    szobaszam = 101 + i
    foglalas = szalloda.foglalas(szobaszam, datumok[i])
    if foglalas is not None:
        print(f"Sikeres foglalás a szobára {szobaszam} dátummal {datumok[i]}")

# kezelés, interfész és adatvalidáció
while True:
    print("\nVálasszon egy műveletet:")
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Foglalható szoba hozzáadása (szállodai alkalmazott)")
    print("5. Foglalható szobák listázása (szállodai alkalmazott)")
    print("6. Kilépés")

    valasztas = input("Választás: ")

    if valasztas == "1":
        szobaszam = int(input("Adja meg a szoba számát: "))
        datum_str = input("Adja meg a foglalás dátumát (YYYY-MM-DD): ")
        datum = datetime.strptime(datum_str, "%Y-%m-%d")

        if datum < datetime.now():
            print("Hibás dátum, kérjük, válasszon jövőbeli dátumot!")
            continue

        foglalas_ar = szalloda.foglalas(szobaszam, datum)
        if foglalas_ar is not None:
            print(f"Sikeres foglalás a szobára {szobaszam} dátummal {datum}. Ár: {foglalas_ar}")
        else:
            print("Hibás szobaszám, kérjük, válasszon elérhető szobát!")

    elif valasztas == "2":
        print("Válassza ki a lemondani kívánt foglalást:")
        for i, foglalas in enumerate(szalloda.foglalasok):
            print(f"{i + 1}. Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

        lemondas_index = int(input("Adja meg a lemondani kívánt foglalás sorszámát: ")) - 1

        if 0 <= lemondas_index < len(szalloda.foglalasok):
            lemondando_foglalas = szalloda.foglalasok[lemondas_index]
            szalloda.lemondas(lemondando_foglalas)
            print("Sikeres lemondás.")
        else:
            print("Hibás sorszám, kérjük, válasszon érvényes sorszámot!")

    elif valasztas == "3":
        szalloda.listaz_foglalasokat()


    elif valasztas == "4":

        felhasznalo_tipus = input("Adja meg a felhasználó típusát ('ugyfel' vagy 'alkalmazott'): ")

        if felhasznalo_tipus == "alkalmazott":

            jelszo = input("Adja meg a jelszót: ")

        else:

            jelszo = None

        szobaszam = int(input("Adja meg a szoba számát: "))

        ar = int(input("Adja meg a szoba árát: "))

        szalloda.hozzaad_foglalhato_szoba(szobaszam, ar, felhasznalo_tipus, jelszo)

        print(f"Foglalható szoba hozzáadva: Szoba száma: {szobaszam}, Ár: {ar}")

    elif valasztas == "5":

        felhasznalo_tipus = input("Adja meg a felhasználó típusát ('ugyfel' vagy 'alkalmazott'): ")

        if felhasznalo_tipus == "alkalmazott":

            jelszo = input("Adja meg a jelszót: ")

            szalloda.listaz_foglalhato_szobakat(felhasznalo_tipus, jelszo)

        else:

            print("Nincs jogosultsága foglalható szobákat listázni.")


    elif valasztas == "6":

        break


    else:

        print("Érvénytelen választás. Kérjük, válasszon újra.")