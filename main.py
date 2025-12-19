from gridder import grid_from_image
import tkinter as tk
import random as rnd
import os

app = tk.Tk()
app.attributes("-fullscreen", True)
canvas = tk.Canvas(app, bg="black", highlightthickness=0)
canvas.place(x=0, y=0, relheight=1, relwidth=1)

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
    levels = [f for f in levels if f.endswith(".lvl.png")]
else:
    raise FileNotFoundError(f"The folder '{LEVELS_FOLDER}' does not exist.")
#endregion

#region Game variables
current_level_index = 0
current_level_grid = []
exit_open = False


LEVEL_ORDER = ("test.lvl.png",)
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

COLOR_MAPPING = {
    0: "white",         # empty
    1: "grey",          # wall
    2: "darkgrey",      # perma wall
    # 3: "green",       # spawn
    4: "darkgreen",     # exit
    5: "RoyalBlue4",    # entrance
    # 6: "cyan",          # loot
    7: "gold3",          # coin
    8: "lightgreen",    # open exit
    10: "RoyalBlue2",   # open entrance
}

#endregion

current_level_grid = grid_from_image(os.path.join(LEVELS_FOLDER, LEVEL_ORDER[current_level_index]))
player_position = [-1, -1]  # (x, y)
enemies = []
# find player spawn position (value 5)
## code to find enemy spawn point (3)

for row in current_level_grid:
    for cell in row:
        if cell == 5:  # entrance
            player_position = [row.index(cell), current_level_grid.index(row)]  # (x, y)
            break
if player_position == [-1, -1]:
    raise ValueError("No entrance point found in the level.")

def draw_grid():
    canvas.delete("all")
    for r_ind, row in enumerate(current_level_grid):
        for c_ind, cell in enumerate(row):
            
            x1 = c_ind * CELL_SIZE
            y1 = r_ind * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if cell not in COLOR_MAPPING.keys():
                color = "white"
            else:
                color = COLOR_MAPPING[cell]
            canvas.create_rectangle(x1,y1,x2,y2, fill=color, outline="")
            
            # special draw system for player, coins, loot and enemies
            if [c_ind, r_ind] == player_position:
                x1 = c_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2
                y1 = r_ind * CELL_SIZE + (CELL_SIZE - PLAYER_SIZE) // 2
                x2 = x1 + PLAYER_SIZE
                y2 = y1 + PLAYER_SIZE
                canvas.create_rectangle(x1,y1,x2,y2, fill=PLAYER_COLOR, outline="")
            elif cell == 7:  # coin
                pass # todo later
            elif cell == 6:  # loot
                pass # todo later
    app.update_idletasks()
draw_grid()
app.mainloop()