from gridder import grid_from_image
import tkinter as tk
import random as rnd
import os

app = tk.Tk()
app.attributes("-fullscreen", True)

game_running = False

ovladani = tk.Frame(app, bg="darkgrey", width=130)
ovladani.pack_propagate(False)
ovladani.pack(side="left", fill="y")

shutdown_btn = tk.Button(ovladani, text="✕", font=("Arial", 12), command=app.destroy, bg="red", fg="white", width=2, height=1)
shutdown_btn.pack(pady=5, padx=5, anchor="nw")

nadpis = tk.Label(ovladani, text="Menu", bg="darkgrey", fg="black", font=("Arial", 16))
nadpis.pack(pady=10)


class DialogWindow(tk.Toplevel):
    def __init__(self, master, title, submit_btn_text: str = "OK", on_select = None, *contents):
        super().__init__(master)
        self.title(title)
        self.geometry("300x300")
        self.master = master
        self.transient(master)
        self.grab_set()
        # insert contents
        content_returns = []
        for content in contents:
            content_returns.append(content(self))
        if not on_select:
            btn_ok = tk.Button(self, text=submit_btn_text, command=self.on_destroy)
        else:
            btn_ok = tk.Button(self, text=submit_btn_text, command=lambda:[on_select(content_returns), self.on_destroy()])
        btn_ok.pack(pady=10)
    def on_destroy(self):
        self.grab_release()
        self.destroy()


#region Level filnames
levels: list[list[str, int]] = [] # list of [filename, completed]
og_levels: list[str] = [] # original list of levels [filename]
LEVELS_FOLDER = "levels"
if os.path.exists(LEVELS_FOLDER):
    levels = [f for f in os.listdir(LEVELS_FOLDER) if os.path.isfile(os.path.join(LEVELS_FOLDER, f))]
    # delete all except .png files
    levels = [f for f in levels if f.endswith(".png")]
    og_levels = levels.copy()
    # delete all expept .lvl.png files
    og_levels = [f for f in levels if f.endswith(".lvl.png")]
    og_levels.sort()
else:
    raise FileNotFoundError(f"The folder '{LEVELS_FOLDER}' does not exist.")
#endregion

#region Game variables
current_level_index = 0
current_level_grid = []
exit_open = False


LEVEL_ORDER = og_levels.copy()
# test if all levels in LEVEL_ORDER exist in levels
for lvl in LEVEL_ORDER:
    if lvl not in levels:
        raise FileNotFoundError(f"The level '{lvl}' does not exist in the levels folder.")
    
ENTRANCE_OPEN_THRESHOLD = 0.2
CELL_SIZE = 24
ROW_COUNT = 28
COLUMN_COUNT = 28
PLAYER_SIZE = CELL_SIZE - 4
PLAYER_COLOR = "red"
ENEMY_COLOR = "purple"
ENEMY_SIZE = PLAYER_SIZE

player_abilities = {}
def reset_player_abilities():
    global player_abilities
    player_abilities = {
        "wall_cheap": False, # done
        "slow_enemies": False,
        "wall_destroy": False, # done
        "wall_pass": False, # done
        "exit_80_percent": False, # done
        # "entrance_unlimited": False, (zrušeno)
        "revive": False, # done
        "fast_hp_recovery": False # done
    }
reset_player_abilities()

WALL_MOVE_COST = 5  # coin cost to move through a wall (placing wall somewhere else)
WALL_DESTROY_COST = 10  # coin cost to destroy a wall permanently
HP_COIN_RATIO = 2  # how many HP points per coin spent (when low on money)

COLOR_MAPPING = {
    0: "white",         # empty
    1: "grey",          # wall
    2: "darkgrey",      # perma wall
    # 3: "green",       # spawn
    4: "darkgreen",     # exit
    5: "RoyalBlue4",    # entrance
    # 6: "cyan",          # loot
    # 7: "gold3",          # coin
    8: "lightgreen",    # open exit
    10: "RoyalBlue2",   # open entrance
}
current_level_grid = grid_from_image(os.path.join(LEVELS_FOLDER, LEVEL_ORDER[current_level_index]))
on_start_coins = 20
revive_used = False

#endregion

# region Menu
#Ukazatele
hp_player = tk.Variable(app, value=100)
hp_frame = tk.Frame(ovladani, bg="tomato", width=80, height=70)
hp_frame.pack_propagate(False)
hp_label = tk.Label(hp_frame, text="Životy", bg="tomato", fg="black", font=("Arial", 12))
hp_label.pack(pady=5)
hp_value = tk.Label(hp_frame, textvariable=hp_player, bg="tomato", fg="black", font=("Arial", 12))
hp_value.pack(pady=5)
hp_frame.pack(pady=5)

coins = tk.Variable(app, value=20)
coin_frame = tk.Frame(ovladani, bg="gold", width=80, height=70)
coin_frame.pack_propagate(False)
coin_label = tk.Label(coin_frame, text="Mince", bg="gold", fg="black", font=("Arial", 12))
coin_label.pack(pady=5)
coin_value = tk.Label(coin_frame, textvariable=coins, bg="gold", fg="black", font=("Arial", 12))
coin_value.pack(pady=5)
coin_frame.pack(pady=5)

revive_used_label = tk.Label(ovladani, text="Revive: Neaktivní", bg="darkgrey", fg="black", font=("Arial", 10))
revive_used_label.pack(pady=5)

def update_revive_label():
    if player_abilities["revive"] and not revive_used:
        revive_used_label.config(text="Revive: Aktivní", fg="green", font=("Arial", 10, "bold"))
    else:
        revive_used_label.config(text="Revive: Neaktivní", fg="black", font=("Arial", 10))

update_revive_label()

# ovládací prvky
toggle_buttons = []
class ToggleButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        global toggle_buttons
        toggle_buttons.append(self)
        self.is_on = False
        self.config(bg="red", command=self.toggle)
    def toggle(self):
        if self['state'] == 'disabled':
            return
        if self.is_on:
            self.is_on = False
            self.config(bg="red")
        else:
            self.is_on = True
            self.config(bg="green")
            for btn in toggle_buttons:
                if btn != self:
                    btn.is_on = False
                    btn.config(bg="red")
btn_wall_move = ToggleButton(ovladani, text="Přesouvání zdi")
btn_wall_move.pack(pady=5)
btn_wall_destroy = ToggleButton(ovladani, text="Ničení zdi", state="disabled")
btn_wall_destroy.pack(pady=5)
btn_wall_pass = ToggleButton(ovladani, text="Procházení zdí", state="disabled")
btn_wall_pass.pack(pady=5)

# seznam abilit
class AbilitiesList:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="lightgrey", width=120, height=235)
        self.frame.pack_propagate(False)
        # Hlavička
        self.label = tk.Label(self.frame, text="Schopnosti", bg="lightgrey", fg="black", font=("Arial", 12))
        self.label.pack(pady=5)
        # Seznam schopností
        self.ability_labels = {}
        for ability in player_abilities.keys():
            color = "green" if player_abilities[ability] else "red"
            lbl = tk.Label(self.frame, text=f"{ability.replace('_', ' ').title()}", bg="lightgrey", fg=color, font=("Arial", 10), wraplength=100, justify="left")
            lbl.pack(pady=2)
            self.ability_labels[ability] = lbl
        self.frame.pack(pady=5)
    def update(self):
        for ability, lbl in self.ability_labels.items():
            color = "green" if player_abilities[ability] else "red"
            lbl.config(fg=color)
abilities_list = AbilitiesList(ovladani)


# horizonální oddělovač
separator = tk.Frame(ovladani, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=10)

def load_level():
    global current_level_index, on_start_coins
    current_level_index = -1
    on_start_coins = coins.get()
    # dialog window to select level
    """dialog = tk.Toplevel(app)
    dialog.title("Vyber úroveň")
    dialog.geometry("200x300")
    dialog.transient(app)
    dialog.grab_set()"""
    def generate_level_listbox(parent):
        global game_running
        game_running = False
        listbox = tk.Listbox(parent)
        for lvl in levels:
            listbox.insert(tk.END, lvl)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        return listbox
    def on_select(content_returns):
        listbox = content_returns[0]
        global current_level_grid, player_position, game_running
        game_running = True
        player_position = [-1, -1]
        current_level_grid = grid_from_image(os.path.join(LEVELS_FOLDER, levels[listbox.curselection()[0]]))
        if game_running:
            find_player_start()
            hp_player.set(100)
            global revive_used
            revive_used = False
            # revive_used_label.config(text="Revive: Aktivní", fg="green", font=("Arial", 10, "bold"))
            update_revive_label()
            generate_coins(5)
            update()
            # reset_player_abilities()
        # return focus to main window
        # app.focus_set()
    # btn_select = tk.Button(dialog, text="Načíst", command=lambda:[on_select(), dialog.destroy()])
    # btn_select.pack(pady=5)
    dialog = DialogWindow(app, "Vyber úroveň", "Načíst", on_select, generate_level_listbox)
# game setup
btn_load_level = tk.Button(ovladani, text="Načíst úroveň", command=load_level)
btn_load_level.pack(pady=5)

# endregion

class AbilityLoot:
    def __init__(self, x: int, y: int, loot_type: str = None):
        self.x = x
        self.y = y
        if not loot_type:
            try:
                self.loot_type = rnd.choice(list(filter(lambda k: not player_abilities[k], list(player_abilities.keys()))))
            except IndexError:
                self.loot_type = None  # all abilities already collected
                self.x, self.y = -1, -1  # remove from map
                self.collected = True
        else:
            self.loot_type = loot_type  # type of ability
            if not loot_type in player_abilities.keys():
                raise ValueError(f"Invalid loot type: {loot_type}")
        self.collected = False
    def collect(self):
        global player_abilities
        if not self.collected:
            player_abilities[self.loot_type] = True
            self.collected = True
            abilities_list.update()
            if self.loot_type == "wall_destroy":
                btn_wall_destroy.config(state="normal")
            elif self.loot_type == "wall_pass":
                btn_wall_pass.config(state="normal")
            elif self.loot_type == "revive":
                # revive_used_label.config(text="Revive: Aktivní", fg="green", font=("Arial", 10, "bold"))
                update_revive_label()
            def collected_content(parent):
                lbl = tk.Label(parent, text=f"Získal jsi schopnost: {self.loot_type.replace('_', ' ').title()}", font=("Arial", 12), wraplength=250)
                lbl.pack(pady=10)
                return lbl
            dialog = DialogWindow(app, "Schopnost získána!", "OK", None, collected_content)
        self.x, self.y = -1, -1  # remove from map
ability_loot = AbilityLoot(-1, -1)  # placeholder
def find_ability_loot_start():
    global ability_loot
    for row in current_level_grid:
        for cell in row:
            if cell == 6:  # loot
                ability_loot = AbilityLoot(row.index(cell), current_level_grid.index(row))
                return
    ability_loot = AbilityLoot(-1, -1)  # no loot found
find_ability_loot_start()

canvas = tk.Canvas(app, bg="black", highlightthickness=0)
canvas.place(x=130, y=0, relheight=1, relwidth=1)

player_position = [-1, -1]  # (x, y)
# enemies = []
class Enemy:
    def __init__(self, x: int, y: int, hp: float = 10.0):
        self.x = x
        self.y = y
        self.hp = hp
        self.alive = True if hp > 0 else False
    def take_damage(self, amount: float):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.die()
    def die(self):
        self.x, self.y = -1, -1  # remove from map
        self.alive = False
    def find_path(self):
        pass
enemy = Enemy(-1, -1, 0)  # dead placeholder
def find_enemy_start():
    pass
find_enemy_start()

# find player spawn position (value 5)
## code to find enemy spawn point (3)

class Coin:
    # class wide value of existing coins
    existing_coins: list['Coin'] = []
    def __init__(self, x: int, y: int, value: float = 1.0):
        self.x = x
        self.y = y
        self.value = value
        Coin.existing_coins.append(self)
    def collect(self):
        global coins
        coins.set(coins.get() + self.value)
        Coin.existing_coins.remove(self)
        current_level_grid[self.y][self.x] = 0  # remove coin from grid
        self.x, self.y = -1, -1  # remove from map

def generate_coins(amount: int):
    for _ in range(amount):
        coin_pos = (-1, -1)
        while coin_pos == (-1, -1):
            coin_pos = (rnd.randint(0,COLUMN_COUNT-1), rnd.randint(0,ROW_COUNT-1)) # generate new coin position
            if current_level_grid[coin_pos[1]][coin_pos[0]] != 0 or coin_pos == player_position or coin_pos == (ability_loot.x, ability_loot.y) or enemy.alive and coin_pos == (enemy.x, enemy.y):
                coin_pos = (-1,-1)
        current_level_grid[coin_pos[1]][coin_pos[0]] = 7  # place coin
        Coin(coin_pos[0], coin_pos[1])

# region Functions
def hp_change(amount):
    global hp_player, revive_used
    hp_player.set(round(hp_player.get() + amount, 1))
    if hp_player.get() <= 0:
        if player_abilities["revive"] and not revive_used:
            revive_used = True
            # revive_used_label.config(text="Revive: Neaktivní", fg="black", font=("Arial", 10))
            update_revive_label()
            hp_player.set(50)  # revive with 50 HP
            find_player_start()
            global game_running
            game_running = False
            def content_revive(parent):
                lbl = tk.Label(parent, text="Použil jsi revive!", font=("Arial", 14))
                lbl.pack(pady=10)
                return lbl
            def on_revive_select(content_returns):
                global game_running
                game_running = True
                update()
            dialog = DialogWindow(app, "Revive!", "OK", on_revive_select, content_revive)
            return
        hp_player.set(0)
        def content_game_over(parent):
            global game_running
            game_running = False
            lbl = tk.Label(parent, text="Zemřel jsi!", font=("Arial", 14))
            lbl.pack(pady=10)
            return lbl
        def on_game_over_select(content_returns):
            # resetuje level
            global current_level_grid, player_position, hp_player, coins, game_running
            game_running = True
            player_position = [-1, -1]
            current_level_grid = grid_from_image(os.path.join(LEVELS_FOLDER, LEVEL_ORDER[current_level_index]))
            find_player_start()
            hp_player.set(100)
            coins.set(on_start_coins)
            update()
        dialog = DialogWindow(app, "Konec hry", "OK", on_game_over_select, content_game_over)
    elif hp_player.get() > 100:
        hp_player.set(100)

def load_next_level():
    global current_level_index, current_level_grid, player_position, game_running, on_start_coins, revive_used
    current_level_index += 1
    if current_level_index >= len(LEVEL_ORDER):
        current_level_index = 0  # restart from first level
    current_level_grid = grid_from_image(os.path.join(LEVELS_FOLDER, LEVEL_ORDER[current_level_index]))
    player_position = [-1, -1]
    find_player_start()
    find_ability_loot_start()
    find_enemy_start()
    generate_coins(5)
    hp_player.set(100)
    on_start_coins = coins.get()
    game_running = True
    revive_used = False
    # revive_used_label.config(text="Revive: Aktivní", fg="green", font=("Arial", 10, "bold"))
    update_revive_label()
    update()

def money_change(amount):
    global coins
    coins.set(round(coins.get() + amount, 1))
    if coins.get() < 0:
        coins.set(0)
        hp_player.set(hp_player.get() + HP_COIN_RATIO * amount) # lose HP when no money left


def move_player(direction):
    global player_position
    if not game_running:
        return
    x, y = player_position
    if direction == "Up":
        new_x, new_y = x, y - 1
    elif direction == "Down":
        new_x, new_y = x, y + 1
    elif direction == "Left":
        new_x, new_y = x - 1, y
    elif direction == "Right":
        new_x, new_y = x + 1, y
    else:
        return  # invalid direction

    # check boundaries
    if 0 <= new_x < COLUMN_COUNT and 0 <= new_y < ROW_COUNT:
        next_cell = current_level_grid[new_y][new_x]
        forbidden_cells = [1, 2]  # walls
        if btn_wall_pass.is_on or btn_wall_move.is_on or btn_wall_destroy.is_on:
            forbidden_cells.remove(1)  # allow moving through normal walls
        if next_cell not in forbidden_cells:
            player_position = [new_x, new_y]
            if next_cell == 1:  # wall
                if btn_wall_move.is_on:
                    current_level_grid[new_y][new_x] = 0  # remove wall
                    new_wall_pos = (-1, -1)
                    while new_wall_pos == (-1, -1):
                        new_wall_pos = (rnd.randint(0,COLUMN_COUNT-1), rnd.randint(0,ROW_COUNT-1)) # generate new wall position
                        # print(new_wall_pos)
                        if current_level_grid[new_wall_pos[1]][new_wall_pos[0]] != 0 or new_wall_pos == next_cell:
                            new_wall_pos = (-1,-1)
                        current_level_grid[new_wall_pos[1]][new_wall_pos[0]] = 1  # place wall
                    money_change(-WALL_MOVE_COST*(0.5 if player_abilities["wall_cheap"] else 1))
                elif btn_wall_destroy.is_on:
                    current_level_grid[new_y][new_x] = 0  # remove wall permanently
                    money_change(-WALL_DESTROY_COST)
            elif next_cell == 4 and enemy.alive == False:  # exit
                load_next_level()
            elif next_cell == 6:  # loot
                ability_loot.collect()
            elif next_cell == 4 and enemy.hp <= 0.2 and player_abilities["exit_80_percent"]:
                load_next_level()
            elif next_cell == 7:  # coin
                # print(Coin.existing_coins)
                for coin in Coin.existing_coins:
                    if coin.x == new_x and coin.y == new_y:
                        coin.collect()
                        break
            # elif next_cell == 5:  # entrance (zrušeno, nebudu implementovat)

        draw_grid()

# region Bindings
app.bind("<Up>", lambda event: move_player("Up"))
app.bind("<Down>", lambda event: move_player("Down"))
app.bind("<Left>", lambda event: move_player("Left"))
app.bind("<Right>", lambda event: move_player("Right"))

app.bind("q", lambda event: btn_wall_move.toggle())
app.bind("w", lambda event: btn_wall_destroy.toggle())
app.bind("e", lambda event: btn_wall_pass.toggle())

# endregion

def find_player_start():
    global player_position
    for row in current_level_grid:
        for cell in row:
            if cell == 5:  # entrance
                player_position = [row.index(cell), current_level_grid.index(row)]  # (x, y)
                break
    if player_position == [-1, -1]:
        raise ValueError("No entrance point found in the level.")
find_player_start()



def draw_grid():
    canvas.delete("all")
    for r_ind, row in enumerate(current_level_grid):
        for c_ind, cell in enumerate(row):
            # center into the middle of canvas space
            centered_offset_x = canvas.winfo_width()//2 - (COLUMN_COUNT * CELL_SIZE)//2
            centered_offset_y = canvas.winfo_height()//2 - (ROW_COUNT * CELL_SIZE)//2
            # debug
            # print(f"Canvas size: {canvas.winfo_width()}x{canvas.winfo_height()}, Offset: {centered_offset_x},{centered_offset_y}")

            x1 = c_ind * CELL_SIZE + centered_offset_x
            y1 = r_ind * CELL_SIZE + centered_offset_y
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if cell not in COLOR_MAPPING.keys():
                color = "white"
            else:
                color = COLOR_MAPPING[cell]
            canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="")
            
            # special draw system for player, coins, loot and enemies
            if [c_ind, r_ind] == player_position:
                x1 = c_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_x
                y1 = r_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_y
                x2 = x1 + PLAYER_SIZE
                y2 = y1 + PLAYER_SIZE
                canvas.create_rectangle(x1,y1,x2,y2, fill=PLAYER_COLOR, outline="")
            elif cell == 7:  # coin
                x1 = c_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_x
                y1 = r_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_y
                x2 = x1 + PLAYER_SIZE
                y2 = y1 + PLAYER_SIZE
                canvas.create_oval(x1,y1,x2,y2, fill="gold3", outline="")
            elif cell == 6:  # loot
                if not ability_loot.collected:
                    x1 = c_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_x
                    y1 = r_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2 + centered_offset_y
                    x2 = x1 + PLAYER_SIZE
                    y2 = y1 + PLAYER_SIZE
                    canvas.create_oval(x1,y1,x2,y2, fill="cyan", outline="")
    app.update_idletasks()

def update():
    draw_grid()
    hp_change(0.1 + 0.1*player_abilities["fast_hp_recovery"])  # slowly recover HP + boost if ability is active
    if game_running:
        app.after(100, update)

# endregion
generate_coins(5)
game_running = True
app.after(100, update)
app.mainloop()