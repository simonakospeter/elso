import statistics
from datetime import date

TEVEKENYSEGEK = [
    "Tanulás",
    "Telefonozás",
    "Közlekedes",
    "Munka",
    "Szabadidő",
    "Alvás"
]


def nap_ellenorzese(datum, szovegek, napok):
    datum = datum.strip()

    try:
        datum = date.fromisoformat(datum).isoformat()
    except ValueError:
        raise ValueError("Hibás dátum! Példa: 2026-11-02")

    for nap in napok:
        if nap["datum"] == datum:
            raise ValueError("Ez a nap már szerepel a nyilvántartásban.")

    ertekek = []

    for szoveg in szovegek:
        try:
            szazalek = float(szoveg.strip().replace(",", "."))
        except ValueError:
            raise ValueError("Minden tevékenységhez számot adjon meg!")

        if not 0 <= szazalek <= 100:
            raise ValueError("A százalék 0 és 100 között legyen!")

        ertekek.append(szazalek)

    osszesen = sum(ertekek)

    if osszesen > 100:
        raise ValueError("Az összes százalék nem lehet több 100-nál!")

    nap = {"datum": datum}

    for tevekenyseg, ertek in zip(TEVEKENYSEGEK, ertekek):
        nap[tevekenyseg] = ertek

    nap["Egyéb"] = round(100 - osszesen, 2)

    return nap


def napok_listazasa(napok):
    if not napok:
        return "Nincs rögzített nap."

    sorok = []

    for nap in sorted(napok, key=lambda adat: adat["datum"]):
        sorok.append(f"Dátum: {nap['datum']}")

        for tevekenyseg in TEVEKENYSEGEK + ["Egyéb"]:
            sorok.append(
                f"  {tevekenyseg}: {nap[tevekenyseg]:.2f}%"
            )

        sorok.append("")

    return "\n".join(sorok)


def statisztika_keszitese(napok):
    if not napok:
        return "Nincs adat a statisztikához."

    sorok = [
        f"Rögzített napok száma: {len(napok)}",
        "",
        "Tevékenységenkénti statisztika:",
        ""
    ]

    for tevekenyseg in TEVEKENYSEGEK + ["Egyéb"]:
        ertekek = [nap[tevekenyseg] for nap in napok]

        atlag = statistics.mean(ertekek)
        median = statistics.median(ertekek)
        szoras = statistics.pstdev(ertekek)

        sorok.append(tevekenyseg)
        sorok.append(f"  Átlag: {atlag:.2f}%")
        sorok.append(f"  Medián: {median:.2f}%")
        sorok.append(f"  Szórás: {szoras:.2f} százalékpont")
        sorok.append("")

    maximum = max(nap["Tanulás"] for nap in napok)

    datumok = [
        nap["datum"]
        for nap in napok
        if nap["Tanulás"] == maximum
    ]

    sorok.append(
        f"Legmagasabb tanulási arány: {maximum:.2f}%"
    )
    sorok.append("Érintett napok: " + ", ".join(datumok))

    return "\n".join(sorok)
