# Uvoz modula 'os' koji omogućava interakciju s operativnim sustavom, npr. za rad s datotečnim sustavom
import os

# Uvoz modula 'json' koji omogućava rad s JSON datotekama, uključujući učitavanje i pisanje
import json

# Uvoz modula 'tkinter' koji omogućava stvaranje grafičkog korisničkog sučelja (GUI)
import tkinter as tk

# Uvoz modula 'secrets' koji se koristi za generiranje sigurnih nasumičnih brojeva, npr. za simulaciju lootanja
import secrets

# Uvoz modula 're' koji omogućava rad s regularnim izrazima, npr. za pretragu teksta
import re

# Uvoz modula 'numpy' koji omogućava rad s nizovima i matricama, te brojne matematičke operacije
import numpy as np

# Uvoz funkcije 'copy' iz modula 'copy' koja omogućava stvaranje dubokih kopija objekata
from copy import copy

# Uvoz modula 'ttk' iz 'tkinter' biblioteke koji omogućava korištenje poboljšanih grafičkih komponenata
from tkinter import ttk

# Uvoz klase 'Fraction' iz modula 'fractions' koja omogućava rad s razlomcima
from fractions import Fraction

# Uvoz modula 'matplotlib.pyplot' koji omogućava crtanje grafova i vizualizaciju podataka
import matplotlib.pyplot as plt

# Uvoz modula 'poisson' iz 'scipy.stats' koji omogućava rad s Poissonovom distribucijom
from scipy.stats import poisson

# Uvoz klase 'FuncFormatter' iz 'matplotlib.ticker' koja omogućava prilagođavanje formata oznaka na osima grafova
from matplotlib.ticker import FuncFormatter

# Uvoz modula 'mplcursors' koji omogućava interaktivnost s grafovima, npr. prikaz informacija o točkama na grafu
import mplcursors

# Blok 'try' pokušava izvršiti kod unutar sebe, a 'except' hvata iznimke (greške) koje se mogu pojaviti
try:
    # Otvaramo JSON datoteku s podacima o čudovištima za čitanje
    with open('monsters-complete.json') as file:
        # Učitavamo podatke iz JSON datoteke
        monsters_data = json.load(file)
        # Filtriramo podatke tako da zadržimo samo čudovišta koja imaju 'drops' (padajuće predmete)
        monsters_data = {monster['name']: monster for monster_id, monster in monsters_data.items() if monster['drops'] != []}
        # Prolazimo kroz svako čudovište i njegove 'drops'
        for id, monster in monsters_data.items():
            for drop in monster['drops']:
                # Ako čudovište ima više od jednog 'rolla' za padajući predmet, prilagođavamo rijetkost
                if drop['rolls'] > 1:
                    drop['rarity'] = drop['rarity'] * drop['rolls']
                    drop['rolls'] = 1
# Ako se dogodi greška prilikom otvaranja ili obrade datoteke, ispisujemo poruku o grešci
except:
    print("Could not find monsters-complete.json")

# Definicija funkcije 'search_monster' koja se poziva prilikom pretrage čudovišta
def search_monster(event=None):
    # Dohvaćamo upit za pretragu iz korisničkog sučelja
    search_query = search_var.get().lower()
    # Filtriramo čudovišta koja odgovaraju upitu za pretragu
    filtered_monsters = [monster_data['name'] for monster_data in monsters_data.values() if
                         re.search(search_query, monster_data['name'], re.IGNORECASE)]
    # Ažuriramo padajući izbornik s filtriranim čudovištima
    monster_dropdown['values'] = filtered_monsters

# Definicija funkcije 'convert_rarity' koja pretvara rijetkost u razlomak i postotak
def convert_rarity(rarity):
    # Pretvaramo rijetkost u razlomak s ograničenim brojem u nazivniku
    fraction = Fraction(rarity).limit_denominator(10000)
    # Pretvaramo rijetkost u postotak
    percentage = rarity * 100
    # Vraćamo razlomak i postotak
    return fraction, percentage

# Definicija funkcije 'percentage_formatter' koja formatira postotke za prikaz na grafu
def percentage_formatter(x, pos):
    # Vraćamo formatirani postotak s jednom decimalom
    return f"{x:.1%}"

# Definicija funkcije 'show_loot_items' koja prikazuje padajuće predmete u korisničkom sučelju
def show_loot_items():
    # Prolazimo kroz svaki padajući predmet u simuliranom plijenu
    for id, item in simulated_loot.items():
        # Stvaramo okvir za svaki predmet
        item_frame = tk.Frame(loot_results_frame)
        item_frame.pack(pady=5)
        # Dohvaćamo ID predmeta
        item_id = item['id']
        # Stvaramo putanju do ikone predmeta
        item_icon_path = f"items-icons/{item_id}.png"
        # Provjeravamo postoji li datoteka s ikonom predmeta
        if os.path.isfile(item_icon_path):
            # Učitavamo ikonu predmeta
            item_icon = tk.PhotoImage(file=item_icon_path)
            # Stvaramo oznaku s ikonom predmeta
            item_label = tk.Label(item_frame, image=item_icon)
            # Pohranjujemo referencu na sliku kako bi se spriječilo njezino uništavanje
            item_label.image = item_icon
            # Pakiramo oznaku s ikonom predmeta
            item_label.pack(side=tk.TOP)
        else:
            # Ako ikona predmeta ne postoji, koristimo zamjensku sliku
            item_icon_placeholder = tk.PhotoImage(file='placeholder.png')
            item_label = tk.Label(item_frame, image=item_icon_placeholder)
            item_label.image = item_icon_placeholder
            item_label.pack(side=tk.TOP)
        # Stvaramo oznaku s imenom predmeta
        item_name_label = tk.Label(item_frame, text=item['name'])
        item_name_label.pack(side=tk.TOP)
        # Stvaramo oznaku s količinom predmeta
        item_quantity_label = tk.Label(item_frame, text=f"Quantity: {item['quantity']}")
        item_quantity_label.pack(side=tk.TOP)
        # Dohvaćamo rijetkost predmeta
        rarity = item['rarity']
        # Pretvaramo rijetkost u razlomak i postotak
        rarity_fraction, rarity_percentage = convert_rarity(rarity)
        # Stvaramo oznaku s rijetkošću predmeta
        item_rarity_label = tk.Label(item_frame, text=f"Rarity: {rarity_fraction} ({rarity_percentage}%)")
        item_rarity_label.pack(side=tk.TOP)

    # Prolazimo kroz svaki ID predmeta u simuliranom plijenu
    for id in simulated_loot:
        # Otvaramo JSON datoteku s podacima o predmetu za čitanje
        with open('items-json\\{}.json'.format(id)) as file:
            # Učitavamo podatke iz JSON datoteke
            data = json.load(file)
            # Ažuriramo vrijednost 'highalch' za predmet, ako postoji
            simulated_loot[id]['highalch'] = 0 if data['highalch'] in [None, '', ' '] else data['highalch']

    # Blok 'try' pokušava izvršiti kod unutar sebe, a 'except' hvata iznimke (greške) koje se mogu pojaviti
    try:
        # Pronalazimo predmet s najvećom vrijednošću 'highalch'
        most_valueable_item = max(simulated_loot, key=lambda item: simulated_loot[item].get('highalch', 0))
        most_valueable_item = simulated_loot[most_valueable_item]
    # Ako se dogodi greška prilikom pronalaska predmeta, postavljamo vrijednost na None i prikazujemo poruku o grešci
    except ValueError:
        most_valueable_item = None
        error_label = tk.Label(loot_results_frame, text="Please select a monster.")
        error_label.pack()

    # Prolazimo kroz svako dijete okvira s rezultatima plijena
    for child in loot_results_frame.winfo_children():
        # Provjeravamo je li dijete okvir
        if isinstance(child, tk.Frame):
            # Dohvaćamo oznake s imenom i količinom predmeta
            child_name_label = child.winfo_children()[1]
            child_quantity_label = child.winfo_children()[2]
            # Provjeravamo odgovara li ime i količina predmeta najvrijednijem predmetu
            if child_name_label.cget("text") == most_valueable_item['name'] and \
                    child_quantity_label.cget("text") == f"Quantity: {most_valueable_item.get('quantity', 0)}":
                # Ako odgovara, mijenjamo font i boju teksta
                child_name_label.config(font=("TkDefaultFont", 12, "bold"), fg="#a18b3f")
                child_quantity_label.config(font=("TkDefaultFont", 12, "bold"), fg="#a18b3f")
                break

# Definicija funkcije 'simulate_loot' koja simulira plijen za odabrano čudovište
def simulate_loot(times=1):
    # Globalna varijabla koja sadrži podatke o odabranom čudovištu
    global selected_monster_data
    # Dohvaćamo ime odabranog čudovišta iz korisničkog sučelja
    selected_monster_name = selected_monster.get()
    # Tražimo podatke o odabranom čudovištu
    selected_monster_data = next((monster_data for monster_data in monsters_data.values() if monster_data['name'] == selected_monster_name), None)
    # Provjeravamo postoje li podaci o odabranom čudovištu
    if selected_monster_data:
        # Dohvaćamo padajuće predmete odabranog čudovišta
        loot = selected_monster_data['drops']
        # Simuliramo plijen određeni broj puta
        for i in range(times):
            print(f'simulating loot for {i + 1} time(s)')
            # Prolazimo kroz svaki padajući predmet
            for item in loot:
                # Provjeravamo sadrži li količina predmeta raspon
                if '-' in item['quantity']:
                    # Ako sadrži, generiramo nasumičnu količinu unutar raspona
                    item_quantity = item_quantity = int(secrets.randbelow(int(item['quantity'].split('-')[1])) + int(item['quantity'].split('-')[0]))
                else:
                    # Ako ne sadrži, količina je fiksna
                    item_quantity = int(item['quantity'])
                # Provjeravamo je li rijetkost predmeta 1 (zagarantirani pad)
                if item['rarity'] == 1:
                    # Ako je, dodajemo predmet u simulirani plijen ili ažuriramo količinu
                    if item['id'] in simulated_loot:
                        simulated_loot[item['id']]['quantity'] += int(item_quantity)
                        continue
                    simulated_loot[item['id']] = copy(item)
                    simulated_loot[item['id']]['quantity'] = item_quantity
                    continue
                else:
                    # Ako rijetkost nije 1, izračunavamo vjerojatnost pada
                    decimal_value = item['rarity']
                    fraction = Fraction(decimal_value)
                    drop_rate = Fraction(1, round((fraction.denominator / fraction.numerator)))
                    n = int(secrets.randbelow(drop_rate.denominator) + 1)
                    # Ako je nasumični broj jednak nazivniku razlomka, predmet pada
                    if n == drop_rate.denominator:
                        show_loot = True
                        # Dodajemo predmet u simulirani plijen ili ažuriramo količinu
                        if item['id'] in simulated_loot:
                            simulated_loot[item['id']]['quantity'] += int(item_quantity)
                            continue
                        simulated_loot[item['id']] = copy(item)
                        simulated_loot[item['id']]['quantity'] = item_quantity
        # Uništavamo sve dječje komponente okvira s rezultatima plijena
        for child in loot_results_frame.winfo_children():
            child.destroy()
    # Prikazujemo padajuće predmete u korisničkom sučelju
    show_loot_items()
    
# Definicija funkcije 'simulate_xloot' koja se poziva prilikom simulacije plijena za prilagođeni broj pokušaja
def simulate_xloot():
    # Blok 'try' pokušava izvršiti kod unutar sebe, a 'except' hvata iznimke (greške) koje se mogu pojaviti
    try:
        # Dohvaćamo broj pokušaja iz korisničkog sučelja
        num_kills = int(user_input_kills_var.get())
        # Provjeravamo je li broj pokušaja unutar dopuštenog raspona
        if not (0 < num_kills <= 100000):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Please simulate loot for no more than 100 000 kills (events), you can graph up to 1 million.")
    # Ako se dogodi greška, prikazujemo poruku o grešci
    except:
        error_label = tk.Label(loot_results_frame, text="Input a valid number of kills (events) to simulate loot.")
        error_label.pack()
    # Simuliramo plijen za uneseni broj pokušaja
    simulate_loot(num_kills)
            
# Definicija funkcije 'simulate_100xloot' koja simulira plijen 100 puta
def simulate_100xloot():
    simulate_loot(100)
    
# Definicija funkcije 'simulate_1000xloot' koja simulira plijen 1000 puta
def simulate_1000xloot():
    simulate_loot(1000)

# Definicija funkcije 'simulate_poisson_distribution' koja simulira Poissonovu distribuciju za padajuće predmete
def simulate_poisson_distribution(num_kills, drop_probability, num_drops, time_per_kill_minutes, time_per_kill_seconds, show_calculated_poisson=True, calculated_poisson_opacity=0.21):

    # Stvaramo tekstualni zapis s rezultatima simulacije
    luck_results = f"Simulated kills: {num_kills}\n"
    
    # Izračunavamo lambda vrijednost za Poissonovu distribuciju
    lambda_val = num_kills * drop_probability

    # Provjeravamo je li lambda veća od 1
    if lambda_val > 1:
        # Izračunavamo vjerojatnost za točno N padova
        chance_of_exactly_n_drops = poisson.pmf(num_drops, lambda_val)
        luck_results += f"Chance to receive exactly {num_drops} drop(s): {chance_of_exactly_n_drops * 100:.4f}%\n"
        
        # Izračunavamo kumulativnu vjerojatnost za N ili manje padova
        chance_of_at_least_n_drops = poisson.cdf(num_drops, lambda_val)
        luck_results += f"Chance to receive {num_drops} drop(s) or fewer: {chance_of_at_least_n_drops * 100:.4f}%\n"    
    
        # Izračunavamo vjerojatnost za više od N padova
        chance_more_than_n = poisson.sf(num_drops, lambda_val)
        luck_results += f"Chance to receive more than {num_drops} drop(s): {chance_more_than_n * 100:.4f}%\n"
    
    # Izračunavamo vjerojatnost za barem jedan pad
    chance_of_at_least_one_drop = 1 - np.exp(-lambda_val)
    luck_results += f"Chance to receive at least one drop: {chance_of_at_least_one_drop * 100:.4f}%\n"
    
    # Izračunavamo vjerojatnost da neće biti nijednog pada
    chance_no_drops = np.exp(-lambda_val)
    luck_results += f"Chance to not receive any drops: {chance_no_drops * 100:.4f}%\n"
    
    # Dodajemo očekivani broj padova (lambda) u rezultate
    luck_results += f"Expected drops (lambda): {lambda_val:.4f}\n"
    
    # Simuliramo Poissonovu distribuciju
    poisson_samples = np.array([secrets.choice(np.random.poisson(lambda_val, num_drops)) for i in range(int(num_kills))])

    # Stvaramo podgraf sa stupcima za Poissonovu distribuciju
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Izračunavamo prosječan broj padova
    average_drops = np.mean(poisson_samples)
    luck_results += f"Average drops (simulated): {average_drops:.4f}\n"

    # Crtamo Poissonovu distribuciju
    poisson_data = np.histogram(poisson_samples, bins=np.arange(0, max(poisson_samples) + 1, 1), density=True)
    cumulative_percentage = np.cumsum(poisson_data[0]) * np.diff(poisson_data[1])
    ax.bar(poisson_data[1][:-1], poisson_data[0], alpha=0.7, color='skyblue', edgecolor='black', label='Poisson Simulation')
    mplcursors.cursor(hover=False).connect("add", lambda sel: sel.annotation.set_text(f"{sel.index} or fewer drops: {cumulative_percentage[int(sel.index)] * 100:.1f}%"))

    # Ako je omogućeno prikazivanje izračunate Poissonove distribucije
    if show_calculated_poisson:
        # Izračunavamo Poissonovu distribuciju
        calculated_poisson = poisson.pmf(np.arange(0, max(poisson_samples) + 1), lambda_val)
        # Crtamo izračunatu Poissonovu distribuciju
        ax.bar(np.arange(0, max(poisson_samples) + 1), calculated_poisson, alpha=calculated_poisson_opacity, color='red', edgecolor='black', label='Probability Mass Function (calculated)')  
    
    # Dohvaćamo razlomak i postotak rijetkosti za prikaz na grafu
    input_rarity_fraction, input_rarity_percentage = convert_rarity(drop_probability)

    # Postavljamo oznake na osima grafa
    ax.set_xlabel(f"Number of drops \n in {num_kills} tries with Rarity: {input_rarity_fraction} ({input_rarity_percentage:.4f}%) chance on each try; lambda (calculated): {lambda_val:0.4f}")
    ax.set_ylabel('Probability * 100, Chance for exactly N drops [%]')
    # Uključujemo mrežu na grafu
    ax.grid(True)
    # Dodajemo legendu na graf
    ax.legend(loc='best', frameon=False)
    # Formatiramo oznake na y-osi kao postotke
    ax.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))

    # Dodajemo graf u listu otvorenih grafova
    open_graphs.append(fig)

    # Ako imamo više od 5 otvorenih grafova, zatvaramo najstariji
    if len(open_graphs) > 5:
        oldest_figure = open_graphs.pop(0)
        plt.close(oldest_figure)

    # Ako postoje uzorci u Poissonovoj distribuciji
    if any(poisson_samples):
        # Izračunavamo vrijeme potrebno za završetak simulacije
        time_to_finish = (float(time_per_kill_minutes) * 60 + float(time_per_kill_seconds)) * num_kills
        # Ako je vrijeme izračunato
        if time_to_finish is not None:
            # Pretvaramo vrijeme u godine, mjesece, dane, sate, minute i sekunde
            years, remainder = divmod(time_to_finish, 31556952)  # 365.25 dana u godini u prosjeku
            months, remainder = divmod(remainder, 2629746)  # 30.44 dana u mjesecu u prosjeku
            days, remainder = divmod(remainder, 86400)  # 24 sata u danu
            hours, remainder = divmod(remainder, 3600)  # 60 minuta u satu
            minutes, seconds = divmod(remainder, 60)
            # Stvaramo formatirani zapis vremena
            time_format = ""
            if years:
                time_format += f"{int(years)} {'year' if int(years) == 1 else 'years'}, "
            if months:
                time_format += f"{int(months)} {'month' if int(months) == 1 else 'months'}, "
            if days:
                time_format += f"{int(days)} {'day' if int(days) == 1 else 'days'}, "
            if hours:
                time_format += f"{int(hours)} {'hour' if int(hours) == 1 else 'hours'}, "
            if minutes:
                time_format += f"{int(minutes)} {'minute' if int(minutes) == 1 else 'minutes'}, "
            if seconds:
                time_format += f"{seconds:.2f} seconds"
                
            # Uklanjamo zarez i razmak s kraja zapisa
            time_format = time_format.rstrip(', ')
            # Dodajemo zapis o vremenu u rezultate
            luck_results += f"Time for {num_kills} tries: {time_format}\n"  
        # Ažuriramo oznaku s rezultatima sreće
        luck_label.config(text=luck_results)
    # Prikazujemo graf
    plt.show()

# Definicija funkcije 'simulate_drop_probability' koja se poziva prilikom simulacije vjerojatnosti pada
def simulate_drop_probability():
    # Blok 'try' pokušava izvršiti kod unutar sebe, a 'except' hvata iznimke (greške) koje se mogu pojaviti
    try:
        # Dohvaćamo broj pokušaja iz korisničkog sučelja
        num_kills = int(user_input_kills_var.get())
        # Provjeravamo je li broj pokušaja unutar dopuštenog raspona
        if not (0 < num_kills <= 1000000):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Please simulate between 1 and 1 million kills.")
        
        # Dohvaćamo vjerojatnost pada iz korisničkog sučelja
        drop_probability = float(chance_input_var.get())
        # Provjeravamo je li vjerojatnost pada unutar dopuštenog raspona
        if not (0 < drop_probability < 1):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Drop probability must be between 0 (impossible) and 1 (guaranteed).")

        # Dohvaćamo broj padova iz korisničkog sučelja
        num_drops = int(num_drops_entry.get())
        # Provjeravamo je li broj padova valjan
        if not (0 <= num_drops):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Please input a valid number of drops.")

        # Dohvaćamo prosječno vrijeme po pokušaju u minutama iz korisničkog sučelja
        time_per_kill_minutes = int(average_time_minutes.get())
        # Provjeravamo je li vrijeme unutar dopuštenog raspona
        if not (0 <= time_per_kill_minutes < 1440):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Time in minutes needs to be between 0 and 1439 minutes (<24 hours).")
        
        # Dohvaćamo prosječno vrijeme po pokušaju u sekundama iz korisničkog sučelja
        time_per_kill_seconds = int(average_time_seconds.get())
        # Provjeravamo je li vrijeme unutar dopuštenog raspona
        if not (0 <= time_per_kill_seconds < 60):
            # Ako nije, prikazujemo iznimku s porukom o grešci
            raise ValueError("Time in seconds needs to be between 0 and 59 seconds.")

        # Dohvaćamo informaciju o prikazu izračunate Poissonove distribucije iz korisničkog sučelja
        show_calculated_poisson = calculated_poisson_var.get()
        # Dohvaćamo prozirnost izračunate Poissonove distribucije iz korisničkog sučelja
        calculated_poisson_opacity = calculated_poisson_opacity_slider.get() / 100.0

    # Ako se dogodi greška, prikazujemo poruku o grešci
    except:
        error_label = tk.Label(loot_results_frame, text=str("Please check the given parameters."))
        error_label.pack()
        return
    
    # Pozivamo funkciju za simulaciju Poissonove distribucije s unesenim parametrima
    simulate_poisson_distribution(num_kills, drop_probability, num_drops, time_per_kill_minutes, time_per_kill_seconds, show_calculated_poisson, calculated_poisson_opacity)

# Definicija funkcije 'on_canvas_configure' koja se poziva prilikom promjene konfiguracije platna
def on_canvas_configure(event):
    # Ažuriramo područje pomicanja za platno
    loot_canvas.configure(scrollregion=loot_canvas.bbox("all"))

# Definicija funkcije 'on_mousewheel' koja omogućava pomicanje sadržaja platna kotačićem miša
def on_mousewheel(event):
    # Pomičemo sadržaj platna vertikalno
    loot_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
# Definicija funkcije 'update_fraction_field' koja ažurira polje s razlomkom kada se promijeni vjerojatnost pada
def update_fraction_field(*args):
    try:
        # Dohvaćamo vjerojatnost pada iz korisničkog sučelja
        drop_probability = float(chance_input_var.get())
        # Omogućavamo uređivanje polja s razlomkom
        drop_fraction_entry.config(state=tk.NORMAL)
        # Brišemo trenutni sadržaj polja s razlomkom
        drop_fraction_entry.delete(0, tk.END)
        # Unosimo novi razlomak u polje
        drop_fraction_entry.insert(0, str(Fraction(drop_probability).limit_denominator(10000)))
        # Onemogućavamo uređivanje polja s razlomkom
        drop_fraction_entry.config(state=tk.DISABLED)

    # Ako se dogodi greška, onemogućavamo uređivanje polja s razlomkom i brišemo sadržaj
    except ValueError:
        drop_fraction_entry.config(state=tk.NORMAL)
        drop_fraction_entry.delete(0, tk.END)
        drop_fraction_entry.config(state=tk.DISABLED)

# Lista koja sadrži otvorene grafove
open_graphs = []

# Stvaramo glavni prozor aplikacije
window = tk.Tk()
# Postavljamo naslov prozora
window.title("Monster Loot Simulator")
# Definiramo širinu i visinu prozora
window_width = 320
window_height = 700
# Dohvaćamo širinu i visinu ekrana
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Izračunavamo poziciju prozora na ekranu
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
# Postavljamo geometriju prozora
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Stvaramo varijablu za odabrano čudovište
selected_monster = tk.StringVar()
# Postavljamo početnu vrijednost varijable
selected_monster.set("Select a monster")
# Stvaramo padajući izbornik za odabir čudovišta
monster_dropdown = ttk.Combobox(window, textvariable=selected_monster, state="readonly")
# Postavljamo vrijednosti padajućeg izbornika na sortiranu listu imena čudovišta
monster_dropdown['values'] = sorted(list(set([monster_data['name'] for monster_data in monsters_data.values()])))
# Pakiramo padajući izbornik
monster_dropdown.pack()

# Stvaramo varijablu za pretragu
search_var = tk.StringVar()
# Postavljamo početnu vrijednost varijable
search_var.set("Search...")
# Stvaramo unosno polje za pretragu
search_entry = ttk.Entry(window, textvariable=search_var)
# Pakiramo unosno polje
search_entry.pack()

# Povezujemo događaj otpuštanja tipke s funkcijom za pretragu
search_entry.bind("<KeyRelease>", search_monster)

# Stvaramo gumb za simulaciju plijena
loot_button = ttk.Button(window, text="Simulate  1x     Loot")
# Pakiramo gumb
loot_button.pack()

# Stvaramo gumb za simulaciju plijena 100 puta
simulate_100x = ttk.Button(window, text="Simulate 100x  Loot")
# Pakiramo gumb
simulate_100x.pack()

# Stvaramo gumb za simulaciju plijena 1000 puta
simulate_1000x = ttk.Button(window, text="Simulate 1000x Loot")
# Pakiramo gumb
simulate_1000x.pack()

# Stvaramo gumb za simulaciju plijena za prilagođeni broj pokušaja
simulate_x = ttk.Button(window, text="Simulate X (Custom) Loot")
# Pakiramo gumb
simulate_x.pack()

# Stvaramo oznaku za unos broja pokušaja
user_input_kills_label = ttk.Label(window, text="Number of kills / tries to simulate:")
# Pakiramo oznaku
user_input_kills_label.pack()
# Stvaramo varijablu za unos broja pokušaja
user_input_kills_var = tk.StringVar(value="1000")
# Stvaramo unosno polje za broj pokušaja
num_kills = ttk.Entry(window, textvariable=user_input_kills_var)
# Pakiramo unosno polje
num_kills.pack()

# Stvaramo oznaku za unos broja padova
num_drops_label = ttk.Label(window, text="Number of Drops / Occurances:")
# Pakiramo oznaku
num_drops_label.pack()
# Stvaramo varijablu za unos broja padova
num_drops = tk.StringVar(value="10")
# Stvaramo unosno polje za broj padova
num_drops_entry = ttk.Entry(window, textvariable=num_drops)
# Pakiramo unosno polje
num_drops_entry.pack()

# Stvaramo oznaku za unos vjerojatnosti pada u decimalnom obliku
chance_input_label = ttk.Label(window, text="Drop probability (Decimal):")
# Pakiramo oznaku
chance_input_label.pack()
# Stvaramo varijablu za unos vjerojatnosti pada
chance_input_var = tk.StringVar(value="0.001")
# Povezujemo promjenu varijable s funkcijom za ažuriranje polja s razlomkom
chance_input_var.trace_add("write", update_fraction_field)
# Stvaramo unosno polje za vjerojatnost pada
drop_probability_entry = ttk.Entry(window, textvariable=chance_input_var)
# Pakiramo unosno polje
drop_probability_entry.pack()

# Stvaramo oznaku za unos vjerojatnosti pada u obliku razlomka
chance_fraction_label = ttk.Label(window, text="Drop probability (Fraction):")
# Pakiramo oznaku
chance_fraction_label.pack()
# Stvaramo varijablu za unos vjerojatnosti pada u obliku razlomka
chance_fraction_var = tk.StringVar(value="1/1000")
# Stvaramo unosno polje za vjerojatnost pada u obliku razlomka, koje je onemogućeno za uređivanje
drop_fraction_entry = ttk.Entry(window, textvariable=chance_fraction_var, state=tk.DISABLED)
# Pakiramo unosno polje
drop_fraction_entry.pack()
# Stvaramo oznaku za unos prosječnog vremena po pokušaju u minutama
time_per_kill_minutes_label = ttk.Label(window, text="Average Time per kill / roll (minutes):")
# Pakiramo oznaku
time_per_kill_minutes_label.pack()

# Stvaramo varijablu za unos prosječnog vremena po pokušaju u minutama
average_time_minutes = tk.StringVar(value="1")
# Stvaramo unosno polje za prosječno vrijeme po pokušaju u minutama
time_per_kill_minutes = ttk.Entry(window, textvariable=average_time_minutes)
# Pakiramo unosno polje
time_per_kill_minutes.pack()

# Stvaramo oznaku za unos prosječnog vremena po pokušaju u sekundama
time_per_kill_seconds_label = ttk.Label(window, text="Average Time per kill / roll (seconds):")
# Pakiramo oznaku
time_per_kill_seconds_label.pack()

# Stvaramo varijablu za unos prosječnog vremena po pokušaju u sekundama
average_time_seconds = tk.StringVar(value="30")
# Stvaramo unosno polje za prosječno vrijeme po pokušaju u sekundama
time_per_kill_seconds = ttk.Entry(window, textvariable=average_time_seconds)
# Pakiramo unosno polje
time_per_kill_seconds.pack()

# Stvaramo oznaku za prikaz rezultata sreće
luck_label = tk.Label(window, text="", font=("TkDefaultFont", 8, "italic"))
# Pakiramo oznaku
luck_label.pack()

# Stvaramo gumb za grafički prikaz vjerojatnosti pada
simulate_button = ttk.Button(window, text="Graph Drop Probability", command=simulate_drop_probability)
# Pakiramo gumb
simulate_button.pack()

# Stvaramo varijablu za kontrolu prikaza izračunate Poissonove distribucije
calculated_poisson_var = tk.BooleanVar(value=False)
# Stvaramo kontrolni okvir za odabir prikaza izračunate Poissonove distribucije
calculated_poisson = ttk.Checkbutton(window, text="Show Probability Mass Function (Calculated)", variable=calculated_poisson_var, command=simulate_drop_probability)
# Pakiramo kontrolni okvir
calculated_poisson.pack()

# Stvaramo oznaku za unos prozirnosti izračunate Poissonove distribucije
calculated_poisson_opacity_label = ttk.Label(window, text="Calculation Opacity:")
# Pakiramo oznaku
calculated_poisson_opacity_label.pack()
# Stvaramo klizač za odabir prozirnosti izračunate Poissonove distribucije
calculated_poisson_opacity_slider = ttk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
# Postavljamo početnu vrijednost klizača
calculated_poisson_opacity_slider.set(21)
# Pakiramo klizač
calculated_poisson_opacity_slider.pack()

# Stvaramo oznaku za prikaz rezultata plijena
loot_results_label = ttk.Label(window, text="Loot Results:")
# Pakiramo oznaku
loot_results_label.pack()

# Stvaramo platno za prikaz rezultata plijena
loot_canvas = tk.Canvas(window)
# Pakiramo platno
loot_canvas.pack(fill=tk.BOTH, expand=True)

# Stvaramo okvir unutar platna za prikaz rezultata plijena
loot_results_frame = tk.Frame(loot_canvas)
# Pakiramo okvir
loot_results_frame.pack(side=None,fill=tk.BOTH, expand=True)

# Stvaramo klizač za pomicanje sadržaja platna
loot_scrollbar = tk.Scrollbar(loot_canvas, orient=tk.VERTICAL, command=loot_canvas.yview)
# Pakiramo klizač
loot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Povezujemo klizač s platnom
loot_canvas.configure(yscrollcommand=loot_scrollbar.set)
# Stvaramo prozor unutar platna koji sadrži okvir s rezultatima plijena
loot_canvas.create_window((0,0) , window=loot_results_frame, anchor=tk.NW)

# Povezujemo promjenu konfiguracije okvira s funkcijom za ažuriranje platna
loot_results_frame.bind("<Configure>", on_canvas_configure)
# Povezujemo događaj kotačića miša s funkcijom za pomicanje sadržaja platna
loot_results_frame.bind_all("<MouseWheel>", on_mousewheel)

# Povezujemo gumb za simulaciju plijena s odgovarajućom funkcijom
loot_button.configure(command=simulate_loot)
# Povezujemo gumb za simulaciju plijena za prilagođeni broj pokušaja s odgovarajućom funkcijom
simulate_x.configure(command=simulate_xloot)
# Povezujemo gumb za simulaciju plijena 100 puta s odgovarajućom funkcijom
simulate_100x.configure(command=simulate_100xloot)
# Povezujemo gumb za simulaciju plijena 1000 puta s odgovarajućom funkcijom
simulate_1000x.configure(command=simulate_1000xloot)

# Stvaramo rječnik za pohranu simuliranog plijena
simulated_loot = {}

# Pokrećemo glavnu petlju prozora
window.mainloop()