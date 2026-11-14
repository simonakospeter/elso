import statistics
from datetime import date

TEVEKENYSEGEK = [
    "Tanulas",
    "Telefonozas",
    "Kozlekedes",
    "Munka",
    "Szabadido",
    "Alvas"
]


def nap_ellenorzese(datum, szovegek, napok):
    datum = datum.strip()

    try:
        datum = date.fromisoformat(datum).isoformat()
    except ValueError:
        raise ValueError("Hibas datum! Pelda: 2026-11-02")

    for nap in napok:
        if nap["datum"] == datum:
            raise ValueError("Ez a nap mar szerepel a nyilvantartasban.")

    ertekek = []

    for szoveg in szovegek:
        try:
            szazalek = float(szoveg.strip().replace(",", "."))
        except ValueError:
            raise ValueError("Minden tevekenyseghez szamot adjon meg!")

        if not 0 <= szazalek <= 100:
            raise ValueError("A szazalek 0 es 100 kozott legyen!")

        ertekek.append(szazalek)

    osszesen = sum(ertekek)

    if osszesen > 100:
        raise ValueError("Az osszes szazalek nem lehet tobb 100-nal!")

    nap = {"datum": datum}

    for tevekenyseg, ertek in zip(TEVEKENYSEGEK, ertekek):
        nap[tevekenyseg] = ertek

    nap["Egyeb"] = round(100 - osszesen, 2)

    return nap


def napok_listazasa(napok):
    if not napok:
        return "Nincs rogzitett nap."

    sorok = []

    for nap in sorted(napok, key=lambda adat: adat["datum"]):
        sorok.append(f"Datum: {nap['datum']}")

        for tevekenyseg in TEVEKENYSEGEK + ["Egyeb"]:
            sorok.append(
                f"  {tevekenyseg}: {nap[tevekenyseg]:.2f}%"
            )

        sorok.append("")

    return "\n".join(sorok)


def statisztika_keszitese(napok):
    if not napok:
        return "Nincs adat a statisztikahoz."

    sorok = [
        f"Rogzitett napok szama: {len(napok)}",
        "",
        "Tevekenysegenkenti statisztika:",
        ""
    ]

    for tevekenyseg in TEVEKENYSEGEK + ["Egyeb"]:
        ertekek = [nap[tevekenyseg] for nap in napok]

        atlag = statistics.mean(ertekek)
        median = statistics.median(ertekek)
        szoras = statistics.pstdev(ertekek)

        sorok.append(tevekenyseg)
        sorok.append(f"  Atlag: {atlag:.2f}%")
        sorok.append(f"  Median: {median:.2f}%")
        sorok.append(f"  Szoras: {szoras:.2f} szazalekpont")
        sorok.append("")

    maximum = max(nap["Tanulas"] for nap in napok)

    datumok = [
        nap["datum"]
        for nap in napok
        if nap["Tanulas"] == maximum
    ]

    sorok.append(
        f"Legmagasabb tanulasi arany: {maximum:.2f}%"
    )
    sorok.append("Erintett napok: " + ", ".join(datumok))

    return "\n".join(sorok)