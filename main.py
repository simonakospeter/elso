import tkinter as tk
from tkinter import messagebox

import ido_modul_SAP

class Idonyilvantarto:
    def __init__(self, ablak):
        self.ablak = ablak
        self.napok = []
        self.mezok = {}
        self.ablak.title("Szemelyes idonyilvantarto")
        self.ablak.geometry("720x720")
        self.felulet_letrehozasa()
        self.ablak.bind("<Return>", self.nap_rogzitese)

    def felulet_letrehozasa(self):
        tk.Label(
            self.ablak,
            text="Szemelyes idonyilvantarto",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Label(
            self.ablak,
            text=(
                "A teljes nap 100%. Ne szamolja ugyanazt az idot "
                "tobb kategoriaba!\n"
                "A fennmarado resz az Egyeb kategoriaba kerul."
            )
        ).pack(pady=5)

        keret = tk.Frame(self.ablak)
        keret.pack(pady=10)

        tk.Label(
            keret,
            text="Datum (EEEE-HH-NN):"
        ).grid(row=0, column=0, padx=10, pady=4, sticky="w")

        self.datum_mezo = tk.Entry(keret)
        self.datum_mezo.grid(row=0, column=1, padx=10, pady=4)

        for sor, tevekenyseg in enumerate(
            ido_modul_SAP.TEVEKENYSEGEK, start=1
        ):
            tk.Label(
                keret,
                text=f"{tevekenyseg} (%):"
            ).grid(
                row=sor,
                column=0,
                padx=10,
                pady=4,
                sticky="w"
            )

            mezo = tk.Entry(keret)
            mezo.insert(0, "0")
            mezo.grid(row=sor, column=1, padx=10, pady=4)

            self.mezok[tevekenyseg] = mezo

        gombok = tk.Frame(self.ablak)
        gombok.pack(pady=10)

        tk.Button(
            gombok,
            text="Nap rogzitese",
            command=self.nap_rogzitese
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            gombok,
            text="Napok listazasa",
            command=self.napok_megjelenitese
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            gombok,
            text="Statisztika",
            command=self.statisztika_megjelenitese
        ).pack(side=tk.LEFT, padx=5)

        self.kimenet = tk.Text(
            self.ablak,
            width=80,
            height=20,
            state=tk.DISABLED
        )
        self.kimenet.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.datum_mezo.focus_set()

    def nap_rogzitese(self, event=None):
        datum = self.datum_mezo.get()

        szovegek = [
            self.mezok[tevekenyseg].get()
            for tevekenyseg in ido_modul_SAP.TEVEKENYSEGEK
        ]

        try:
            nap = ido_modul_SAP.nap_ellenorzese(
                datum, szovegek, self.napok
            )
        except ValueError as hiba:
            messagebox.showerror("Hibas adat", str(hiba))
            return

        self.napok.append(nap)
        self.napok_megjelenitese()

        messagebox.showinfo(
            "Sikeres rogzites",
            f"A nap rogzitve.\nEgyeb ido: {nap['Egyeb']:.2f}%"
        )

        self.datum_mezo.delete(0, tk.END)

        for mezo in self.mezok.values():
            mezo.delete(0, tk.END)
            mezo.insert(0, "0")

        self.datum_mezo.focus_set()

    def napok_megjelenitese(self):
        szoveg = ido_modul_SAP.napok_listazasa(self.napok)
        self.szoveg_kiirasa(szoveg)

    def statisztika_megjelenitese(self):
        szoveg = ido_modul_SAP.statisztika_keszitese(self.napok)
        self.szoveg_kiirasa(szoveg)

    def szoveg_kiirasa(self, szoveg):
        self.kimenet.config(state=tk.NORMAL)
        self.kimenet.delete("1.0", tk.END)
        self.kimenet.insert(tk.END, szoveg)
        self.kimenet.config(state=tk.DISABLED)

if __name__ == "__main__":
    ablak = tk.Tk()
    program = Idonyilvantarto(ablak)
    ablak.mainloop()