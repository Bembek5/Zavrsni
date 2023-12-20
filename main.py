import os
import json
import tkinter as tk
import secrets
import re
import numpy as np
from copy import copy
from tkinter import ttk
from fractions import Fraction
import matplotlib.pyplot as plt
from scipy.stats import poisson
from matplotlib.ticker import FuncFormatter
import mplcursors

try:
    with open('monsters-complete.json') as file:
        monsters_data = json.load(file)
        monsters_data = {monster['name']: monster for monster_id, monster in monsters_data.items() if monster['drops'] != []}
        for id, monster in monsters_data.items():
            for drop in monster['drops']:
                if drop['rolls'] > 1:
                    drop['rarity'] = drop['rarity'] * drop['rolls']
                    drop['rolls'] = 1
except:
    print("Could not find monsters-complete.json")

def search_monster(event=None):
    search_query = search_var.get().lower()
    filtered_monsters = [monster_data['name'] for monster_data in monsters_data.values() if
                         re.search(search_query, monster_data['name'], re.IGNORECASE)]
    monster_dropdown['values'] = filtered_monsters

def convert_rarity(rarity):
    fraction = Fraction(rarity).limit_denominator(1000)
    percentage = rarity * 100
    return fraction, percentage

def percentage_formatter(x, pos):
    return f"{x:.1%}"


def show_loot_items():
    for id, item in simulated_loot.items():
        item_frame = tk.Frame(loot_results_frame)
        item_frame.pack(pady=5)
        item_id = item['id']
        item_icon_path = f"items-icons/{item_id}.png"
        if os.path.isfile(item_icon_path):
            item_icon = tk.PhotoImage(file=item_icon_path)
            item_label = tk.Label(item_frame, image=item_icon)
            item_label.image = item_icon
            item_label.pack(side=tk.TOP)
        else:
            item_icon_placeholder = tk.PhotoImage(file='placeholder.png')
            item_label = tk.Label(item_frame, image=item_icon_placeholder)
            item_label.image = item_icon_placeholder
            item_label.pack(side=tk.TOP)
        item_name_label = tk.Label(item_frame, text=item['name'])
        item_name_label.pack(side=tk.TOP)
        item_quantity_label = tk.Label(item_frame, text=f"Quantity: {item['quantity']}")
        item_quantity_label.pack(side=tk.TOP)
        rarity = item['rarity']
        rarity_fraction, rarity_percentage = convert_rarity(rarity)
        item_rarity_label = tk.Label(item_frame, text=f"Rarity: {rarity_fraction} ({rarity_percentage}%)")
        item_rarity_label.pack(side=tk.TOP)

    for id in simulated_loot:
        with open('items-json\\{}.json'.format(id)) as file:
            data = json.load(file)
            simulated_loot[id]['highalch'] = 0 if data['highalch'] in [None, '', ' '] else data['highalch']

    try:
        most_valueable_item = max(simulated_loot, key=lambda item: simulated_loot[item].get('highalch', 0))
        most_valueable_item = simulated_loot[most_valueable_item]
    except ValueError:
        most_valueable_item = None
        error_label = tk.Label(loot_results_frame, text="Please select a monster.")
        error_label.pack()

    for child in loot_results_frame.winfo_children():
        if isinstance(child, tk.Frame):
            child_name_label = child.winfo_children()[1]
            child_quantity_label = child.winfo_children()[2]
            if child_name_label.cget("text") == most_valueable_item['name'] and \
                    child_quantity_label.cget("text") == f"Quantity: {most_valueable_item.get('quantity', 0)}":
                child_name_label.config(font=("TkDefaultFont", 12, "bold"), fg="#a18b3f")
                child_quantity_label.config(font=("TkDefaultFont", 12, "bold"), fg="#a18b3f")
                break

def simulate_loot(times=1):
    global selected_monster_data
    selected_monster_name = selected_monster.get()
    selected_monster_data = next((monster_data for monster_data in monsters_data.values() if monster_data['name'] == selected_monster_name),None)
    if selected_monster_data:
        loot = selected_monster_data['drops']
        for i in range(times):
            print(f'simulating loot for {i + 1} time(s)')
            for item in loot:
                if '-' in item['quantity']:
                    item_quantity = item_quantity = int(secrets.randbelow(int(item['quantity'].split('-')[1])) + int(item['quantity'].split('-')[0]))
                else:
                    item_quantity = int(item['quantity'])
                if item['rarity'] == 1:
                    if item['id'] in simulated_loot:
                        simulated_loot[item['id']]['quantity'] += int(item_quantity)
                        continue
                    simulated_loot[item['id']] = copy(item)
                    simulated_loot[item['id']]['quantity'] = item_quantity
                    continue
                else:
                    decimal_value = item['rarity']
                    fraction = Fraction(decimal_value)
                    drop_rate = Fraction(1, round((fraction.denominator / fraction.numerator)))
                    n = int(secrets.randbelow(drop_rate.denominator) + 1)
                    if n == drop_rate.denominator:
                        show_loot = True
                        if item['id'] in simulated_loot:
                            simulated_loot[item['id']]['quantity'] += int(item_quantity)
                            continue
                        simulated_loot[item['id']] = copy(item)
                        simulated_loot[item['id']]['quantity'] = item_quantity
        for child in loot_results_frame.winfo_children():
            child.destroy()
    show_loot_items()
    
def simulate_xloot():
    try:
        num_kills = int(user_input_kills_var.get())
        if not (0 < num_kills <= 100000):
            raise ValueError("Please simulate loot for no more than 100 000 kills (events).")
    except:
        error_label = tk.Label(loot_results_frame, text="Error, input a valid number of kills (events) to simulate loot.")
        error_label.pack()
    simulate_loot(num_kills)
            
def simulate_100xloot():
    simulate_loot(100)
    
def simulate_1000xloot():
    simulate_loot(1000)

def simulate_poisson_distribution(num_kills, drop_probability, num_drops, time_per_kill_minutes, time_per_kill_seconds, show_calculated_poisson=True, calculated_poisson_opacity=0.21):

    luck_results = f"Simulated kills: {num_kills}\n"
    
    lambda_val = num_kills * drop_probability

    if lambda_val > 1:
        chance_of_exactly_n_drops = poisson.pmf(num_drops, lambda_val)
        luck_results += f"Chance to receive exactly {num_drops} drop(s): {chance_of_exactly_n_drops * 100:.4f}%\n"
        
        chance_of_at_least_n_drops = poisson.cdf(num_drops, lambda_val)
        luck_results += f"Chance to receive {num_drops} drop(s) or fewer: {chance_of_at_least_n_drops * 100:.4f}%\n"    
    
        chance_more_than_n = poisson.sf(num_drops, lambda_val)
        luck_results += f"Chance to receive more than {num_drops} drop(s): {chance_more_than_n * 100:.4f}%\n"
    
    chance_of_at_least_one_drop = 1 - np.exp(-lambda_val)
    luck_results += f"Chance to receive at least one drop: {chance_of_at_least_one_drop * 100:.4f}%\n"
    
    chance_no_drops = np.exp(-lambda_val)
    luck_results += f"Chance to not receive any drops: {chance_no_drops * 100:.4f}%\n"
    
    luck_results += f"Expected drops (lambda): {lambda_val:.4f}\n"
    
    # Simulate Poisson distribution
    poisson_samples = np.array([secrets.choice(np.random.poisson(lambda_val, num_drops)) for i in range(int(num_kills))])

    # Create subplot with bars for Poisson distribution
    fig, ax = plt.subplots(figsize=(8, 6))
    
    average_drops = np.mean(poisson_samples)
    luck_results += f"Average drops (simulated): {average_drops:.4f}\n"

    # Plot Poisson distribution
    poisson_data = np.histogram(poisson_samples, bins=np.arange(0, max(poisson_samples) + 1, 1), density=True)
    cumulative_percentage = np.cumsum(poisson_data[0]) * np.diff(poisson_data[1])
    ax.bar(poisson_data[1][:-1], poisson_data[0], alpha=0.7, color='skyblue', edgecolor='black', label='Poisson Simulation')
    mplcursors.cursor(hover=False).connect("add", lambda sel: sel.annotation.set_text(f"{sel.index} or fewer drops: {cumulative_percentage[int(sel.index)] * 100:.1f}%"))

    if show_calculated_poisson:
        calculated_poisson = poisson.pmf(np.arange(0, max(poisson_samples) + 1), lambda_val)
        ax.bar(np.arange(0, max(poisson_samples) + 1), calculated_poisson, alpha=calculated_poisson_opacity, color='red', edgecolor='black', label='Probability Mass Function (calculated)')  
    
    input_rarity_fraction, input_rarity_percentage = convert_rarity(drop_probability)

    ax.set_xlabel(f"Number of drops \n in {num_kills} tries with Rarity: {input_rarity_fraction} ({input_rarity_percentage:.4f}%) chance on each try; lambda (calculated): {lambda_val:0.4f}")
    ax.set_ylabel('Probability * 100, Chance for exactly N drops [%]')
    ax.grid(True)
    ax.legend(loc='best', frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))

    luck_label.config(text=luck_results)
    
    open_graphs.append(fig)

    if len(open_graphs) > 5:
        oldest_figure = open_graphs.pop(0)
        plt.close(oldest_figure)

    if any(poisson_samples):
        time_to_finish = (float(time_per_kill_minutes) * 60 + float(time_per_kill_seconds)) * num_kills
        if time_to_finish is not None:
            years, remainder = divmod(time_to_finish, 31556952)  # 365.25 days in a year on average
            months, remainder = divmod(remainder, 2629746)  # 30.44 days in a month on average
            days, remainder = divmod(remainder, 86400)  # 24 hours in a day
            hours, remainder = divmod(remainder, 3600)  # 60 minutes in an hour
            minutes, seconds = divmod(remainder, 60)
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
                
            # Remove trailing comma and space
            time_format = time_format.rstrip(', ')

            luck_results += f"Time needed for {num_kills} tries: {time_format}\n"

    plt.show()

def simulate_drop_probability():
    try:
        num_kills = int(user_input_kills_var.get())
        if not (0 < num_kills <= 1000000):
            raise ValueError("Please simulate between 1 and 1 million kills.")
        
        drop_probability = float(chance_input_var.get())
        if not (0 < drop_probability < 1):
            raise ValueError("Drop probability must be between 0 (impossible) and 1 (guaranteed).")

        num_drops = int(num_drops_entry.get())
        if not (0 <= num_drops):
            raise ValueError("Please input a valid number of drops.")

        time_per_kill_minutes = int(average_time_minutes.get())
        if not (0 <= time_per_kill_minutes < 1440):
            raise ValueError("Time in minutes needs to be between 0 and 1439 minutes (<24 hours).")
        
        time_per_kill_seconds = int(average_time_seconds.get())
        if not (0 <= time_per_kill_seconds < 60):
            raise ValueError("Time in seconds needs to be between 0 and 59 seconds.")

        show_calculated_poisson = calculated_poisson_var.get()
        calculated_poisson_opacity = calculated_poisson_opacity_slider.get() / 100.0

    except:
        error_label = tk.Label(loot_results_frame, text=str("Please check the given parameters."))
        error_label.pack()
        return
    
    simulate_poisson_distribution(num_kills, drop_probability, num_drops, time_per_kill_minutes, time_per_kill_seconds, show_calculated_poisson, calculated_poisson_opacity)

def on_canvas_configure(event):
    loot_canvas.configure(scrollregion=loot_canvas.bbox("all"))

def on_mousewheel(event):
    loot_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
def update_fraction_field(*args):
    try:
        drop_probability = float(chance_input_var.get())
        drop_fraction_entry.config(state=tk.NORMAL)
        drop_fraction_entry.delete(0, tk.END)
        drop_fraction_entry.insert(0, str(Fraction(drop_probability).limit_denominator(10000)))
        drop_fraction_entry.config(state=tk.DISABLED)

    except ValueError:
        drop_fraction_entry.config(state=tk.NORMAL)
        drop_fraction_entry.delete(0, tk.END)
        drop_fraction_entry.config(state=tk.DISABLED)

def update_decimal_field(*args):
    drop_probability_entry.config(state=tk.NORMAL)
    drop_fraction_entry.config(state=tk.NORMAL)
    drop_fraction_entry.delete(0, tk.END)

open_graphs = []

window = tk.Tk()
window.title("Monster Loot Simulator")
window_width = 300
window_height = 700
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

selected_monster = tk.StringVar()
selected_monster.set("Select a monster")
monster_dropdown = ttk.Combobox(window, textvariable=selected_monster, state="readonly")
monster_dropdown['values'] = sorted(list(set([monster_data['name'] for monster_data in monsters_data.values()])))
monster_dropdown.pack()

search_var = tk.StringVar()
search_var.set("Search...")
search_entry = ttk.Entry(window, textvariable=search_var)
search_entry.pack()

search_entry.bind("<KeyRelease>", search_monster)

loot_button = ttk.Button(window, text="Simulate  1x     Loot")
loot_button.pack()

simulate_100x = ttk.Button(window, text="Simulate 100x  Loot")
simulate_100x.pack()

simulate_1000x = ttk.Button(window, text="Simulate 1000x Loot")
simulate_1000x.pack()

simulate_x = ttk.Button(window, text="Simulate X (Custom) Loot")
simulate_x.pack()

user_input_kills_label = ttk.Label(window, text="Number of kills / tries to simulate:")
user_input_kills_label.pack()
user_input_kills_var = tk.StringVar(value="10000")
num_kills = ttk.Entry(window, textvariable=user_input_kills_var)
num_kills.pack()

num_drops_label = ttk.Label(window, text="Number of Drops / Occurances:")
num_drops_label.pack()
num_drops = tk.StringVar(value="10")
num_drops_entry = ttk.Entry(window, textvariable=num_drops)
num_drops_entry.pack()

chance_input_label = ttk.Label(window, text="Drop probability (Decimal):")
chance_input_label.pack()
chance_input_var = tk.StringVar(value="0.001")
chance_input_var.trace_add("write", update_fraction_field)
drop_probability_entry = ttk.Entry(window, textvariable=chance_input_var)
drop_probability_entry.pack()

chance_fraction_label = ttk.Label(window, text="Drop probability (Fraction):")
chance_fraction_label.pack()
chance_fraction_var = tk.StringVar(value="1/10000")
drop_fraction_entry = ttk.Entry(window, textvariable=chance_fraction_var, state=tk.DISABLED)
drop_fraction_entry.pack()

time_per_kill_minutes_label = ttk.Label(window, text="Average Time per kill / roll (minutes):")
time_per_kill_minutes_label.pack()

average_time_minutes = tk.StringVar(value="1")
time_per_kill_minutes = ttk.Entry(window, textvariable=average_time_minutes)
time_per_kill_minutes.pack()

time_per_kill_seconds_label = ttk.Label(window, text="Average Time per kill / roll (seconds):")
time_per_kill_seconds_label.pack()

average_time_seconds = tk.StringVar(value="30")
time_per_kill_seconds = ttk.Entry(window, textvariable=average_time_seconds)
time_per_kill_seconds.pack()

luck_label = tk.Label(window, text="", font=("TkDefaultFont", 8, "italic"))
luck_label.pack()

simulate_button = ttk.Button(window, text="Graph Drop Probability", command=simulate_drop_probability)
simulate_button.pack()

calculated_poisson_var = tk.BooleanVar(value=False)
calculated_poisson = ttk.Checkbutton(window, text="Show Probability Mass Function (Calculated)", variable=calculated_poisson_var, command=simulate_drop_probability)
calculated_poisson.pack()

calculated_poisson_opacity_label = ttk.Label(window, text="Calculation Opacity:")
calculated_poisson_opacity_label.pack()
calculated_poisson_opacity_slider = ttk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
calculated_poisson_opacity_slider.set(21)
calculated_poisson_opacity_slider.pack()

loot_results_label = ttk.Label(window, text="Loot Results:")
loot_results_label.pack()

loot_canvas = tk.Canvas(window)
loot_canvas.pack(fill=tk.BOTH, expand=True)

loot_results_frame = tk.Frame(loot_canvas)
loot_results_frame.pack(side=None,fill=tk.BOTH, expand=True)

loot_scrollbar = tk.Scrollbar(loot_canvas, orient=tk.VERTICAL, command=loot_canvas.yview)
loot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
loot_canvas.configure(yscrollcommand=loot_scrollbar.set)
loot_canvas.create_window((0,0) , window=loot_results_frame, anchor=tk.NW)

loot_results_frame.bind("<Configure>", on_canvas_configure)
loot_results_frame.bind_all("<MouseWheel>", on_mousewheel)

loot_button.configure(command=simulate_loot)
simulate_x.configure(command=simulate_xloot)
simulate_100x.configure(command=simulate_100xloot)
simulate_1000x.configure(command=simulate_1000xloot)

simulated_loot = {}

window.mainloop()