# !/usr/bin/env python3
# Authors: AnalogMan, SwayStation
# Modified Date: 2025-09-14
# Version: DIM Name Gen DS v1.4.0
# Purpose: Generates Bandai Vital Bracelet Name Sprites for DIM modifications
# Requirements: Pillow (pip install Pillow)
#               tkinterdnd2 (pip install tkinterdnd2)


# ---------- Imports & Global Setup ----------

import os
import sys
from functools import partial
from tkinter import PhotoImage, StringVar, Label, Entry, Button, Canvas, Frame, Toplevel
from PIL import Image, ImageTk
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
root = TkinterDnD.Tk()
DEBUG_MODE = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller/py2app """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Overlay definitions
overlay_active = False

# Font mapping
FONT_MAP = {
    "DigiScript": "VB_Alphabet_ENG_DigiScript",
    "Official Bandai": "VB_Alphabet_ENG_Official_Bandai",
    "Agero": "VB_Alphabet_Eng_Agero"}

# Font Menu Definitions
font_groups = {
    "DigiScript": [("DigiScript", "DigiScript.png", "DigiScript_hover.png"), 
                   ("Official Bandai", "Official Bandai.png", "Official Bandai_hover.png"),
                   ("Agero", "Agero.png", "Agero_hover.png")]}

default_font = font_groups["DigiScript"][0][0]
font_var = StringVar(value=default_font)
font_var.set("DigiScript")  # or whatever your default font is
active_font_group = "DigiScript"
alternate_buttons = []
related_buttons = []
current_preview = None

font_images = {}


default_button_map = {
    "Agero": "Agero.png",
    "DigiScript": "DigiScript.png",
    "Official Bandai": "Official Bandai.png"
}

for group, entries in font_groups.items():
    for font_name, _, hover_img in entries:
        default_img = default_button_map.get(font_name, "DigiScript.png")

        try:
            default_path = resource_path(f"assets/GUI/{default_img}")
            default = Image.open(default_path).resize((156, 24))
        except Exception as e:
            print(f"Failed to load default image: {default_img}")
            print(e)
            default = Image.new("RGBA", (156, 24), (255, 0, 0, 255))  # Red placeholder

        try:
            hover_path = resource_path(f"assets/GUI/{hover_img}")
            hover = Image.open(hover_path).resize((156, 24))
        except Exception as e:
            print(f"Failed to load hover image: {hover_img}")
            print(e)
            hover = default.copy()

        font_images[font_name] = {
            "default": ImageTk.PhotoImage(default),
            "hover": ImageTk.PhotoImage(hover)
        }




# Color definitions
white = (255, 255, 255)
green = (0, 255, 0)
serif = ["A", "M", "S", "V", "W"]


from sys import version_info, exit
if version_info <= (3,2,0):
    hidden_label.config(text="Python version 3.2.0+ needed to run this app.", font=("Courier New", 14))

try: 
    from PIL import Image, ImageOps # pip3 import Pillow
except:
    print('\nDependancies missing:\npip3 install Pillow\n')
    hidden_label.config(text="Dependancies missing: pip3 install Pillow.", font=("Courier New", 14))
    exit(1)

import os





# ---------- Setup UI & Functions Definitions ----------

# --- Setup UI ---
def setup_ui():
    global drop_canvas, overlay_label, output_button, overlay_img
    global my_entry, my_label, generate_button, hidden_label, font_var

    button_width = 8  # Adjust as needed
    button_height = 1

    # Overlay and text
    overlay_img_path = resource_path("assets/GUI/overlay_dragdrop.png")  # Update path as needed
    overlay_img_raw = Image.open(overlay_img_path).convert("RGBA")
    overlay_img = ImageTk.PhotoImage(overlay_img_raw)

    overlay_label = Label(root, image=overlay_img, borderwidth=0)
    overlay_label.image = overlay_img  # Prevent garbage collection
    overlay_label.place(x=0, y=0)
    overlay_label.lower()  # Start hidden

    # Drop canvas
    drop_canvas = Canvas(root, width=700, height=275, bg="#313131", highlightthickness=0)
    drop_canvas.place(x=0, y=0)

    # Drag bindings
    drop_canvas.drop_target_register(DND_FILES)
    drop_canvas.dnd_bind('<<DropEnter>>', on_drag_enter)
    drop_canvas.dnd_bind('<<DropLeave>>', on_drag_leave)
    drop_canvas.dnd_bind('<<Drop>>', handle_drop)

    overlay_label.drop_target_register(DND_FILES)
    overlay_label.dnd_bind('<<DropEnter>>', on_drag_enter)
    overlay_label.dnd_bind('<<DropLeave>>', on_drag_leave)
    overlay_label.dnd_bind('<<Drop>>', handle_drop)

    # Entry and labels
    my_label = Label(root, text="Type Name:", fg="white", font=("Courier New", 20), justify="center", bg="#313131")
    my_label.place(x=350, y=80, anchor="center")
    debug_print("Label exists:", my_label.winfo_exists())

    my_entry = Entry(root, width=50, font=("Courier New", 14))
    my_entry.place(x=350, y=130, anchor="center")
    debug_print("Entry exists:", my_entry.winfo_exists())

    generate_button = Button(root, text="Generate", font=("Courier New", 14), 
                             width=button_width, height=button_height, command=lambda: change())
    generate_button.place(x=425, y=175, anchor="center")
    debug_print("Button exists:", generate_button.winfo_exists())

    preview_button = Button(root, text="Preview", font=("Courier New", 14), 
                            width=button_width, height=button_height, command=open_preview_window)
    preview_button.place(x=275, y=175, anchor="center")  # Adjust position as needed

    hidden_label = Label(root, text="", fg="white", font=("Courier New", 20), bg="#313131")
    hidden_label.place(x=350, y=230, anchor="center")
    debug_print("Widget created:", my_label.winfo_exists())


    # Output folder button (hidden initially)
    output_button = Button(root, text="Show Output Folder", font=("Courier New", 12), command=open_output_folder)
    output_button.place_forget()

    # Font selector
    show_font_preview()

    # Bind Enter key
    root.bind('<Return>', handle_enter_key)

    # Icon Loading
    icon_path = resource_path("assets/App Icons/DIMNameGenDS.png")
    img = Image.open(icon_path)
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(True, icon)
       
    # Load Fonts
    digi_font_path = resource_path("assets/Fonts/VB_Alphabet_ENG_DigiScript.png")
    bandai_font_path = resource_path("assets/Fonts/VB_Alphabet_ENG_Official_Bandai.png")
    agero_font_path = resource_path("assets/Fonts/VB_Alphabet_ENG_Agero.png")

    try:
        digi_font_img = PhotoImage(file=digi_font_path)
        bandai_font_img = PhotoImage(file=bandai_font_path)
        agero_font_img = PhotoImage(file=agero_font_path)
    except Exception as e:
        print(f"Font image load failed: {e}")
    
    debug_print("Type of overlay_label:", type(overlay_label))
    debug_print("Scheduling overlay lower")
    debug_print(font_images[font_var.get()]["default"].height())
    root.after(10, lambda: overlay_label.master.tk.call('lower', overlay_label._w))





# --- Definitions ---

dropdown_open = False
alternate_buttons = []
preview_button = Button(root, text="Preview", command=lambda: open_preview_window(my_entry.get()))

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)


def toggle_font_menu():
    global dropdown_open

    if not dropdown_open:
        preview_frame.lower()  # Push behind menu
        show_font_menu()
        dropdown_open = True
    else:
        hide_font_menu()
        preview_frame.lift()   # Bring back to front
        dropdown_open = False


def on_hover(button, font_name, is_enter, event=None):
    debug_print(f"{'Enter' if is_enter else 'Leave'}: {font_name}")
    state = "hover" if is_enter else "default"
    button.config(image=font_images[font_name][state])


def show_font_menu():
    global alternate_buttons
    menu_frame = Frame(root, width=160, height=81)
    menu_frame.place(x=520, y=20)

    group_fonts = font_groups[active_font_group]
    current_font = font_var.get()
    
    # Reorder so current font appears first
    sorted_fonts = sorted(group_fonts, key=lambda f: f[0] != current_font)

    debug_print(f"Current font: {font_var.get()}")
    
    y_offset = 0
    for font_name, default_img, hover_img in sorted_fonts:
        create_font_button(menu_frame, font_name, y_offset)
        y_offset += 26

    alternate_buttons.append(menu_frame)


def show_related_fonts():
    global related_buttons, active_font_group

    # Clear old buttons
    for btn in related_buttons:
        btn.destroy()
    related_buttons.clear()

    # Show related fonts from base group
    y_offset = 0
    for font_name, img in font_images[active_font_group][1:]: # Skip first preview
        btn = Button(root, image=img, borderwidth=0,
                     command=lambda i=img, f=font_name: select_font(i, f))
        btn.image = img
        btn.place(x=520, y=y_offset)
        btn.lift()
        related_buttons.append(btn)
        y_offset += 26


def hide_font_menu():
    global alternate_buttons
    for btn in alternate_buttons:
        btn.destroy()
    alternate_buttons.clear()


def show_font_preview():
    global current_preview, preview_frame

    img = font_images[font_var.get()]["default"]

    preview_frame = Frame(root, width=160, height=27)
    preview_frame.place(x=520, y=20)

    current_preview = Button(preview_frame, image=img, borderwidth=0,
                            command=toggle_font_menu)
    current_preview.image = img
    current_preview.place(x=0, y=0)
    

def select_font(font_name):
    global font_var, active_font_group, current_preview, dropdown_open

    font_var.set(font_name)
    debug_print(f"Font selected: {font_name}")

    # Update active group
    for group, entries in font_groups.items():
        if any(font_name == name for name, *_ in entries):
            active_font_group = group
            break

    # Update preview image
    img = font_images[font_name]["default"]
    current_preview.config(image=img)
    current_preview.image = img  # Prevent garbage collection

    # Restore the preview frame and button
    preview_frame.lift()
    current_preview.place(x=0, y=0)

    # Clear dropdown
    hide_font_menu()
    dropdown_open = False # ✅ Reset toggle state


def show_alternate_fonts():
    global alternate_buttons

    # Clear old buttons
    for btn in alternate_buttons:
        btn.destroy()
    alternate_buttons.clear()

    group_fonts = font_groups[active_font_group]
    current_font = font_var.get()

    y_offset = 0
    for font_name, _ in group_fonts:
        if font_name != current_font:
            img = font_images[font_name]
            btn = Button(root, image=img, borderwidth=0,
                         command=lambda f=font_name: select_font(f))
            btn.image = img
            btn.place(x=520, y=y_offset)
            btn.lift()
            alternate_buttons.append(btn)
            y_offset += 26


def create_font_button(parent, font_name, y_offset):
    img_default = font_images[font_name]["default"]
    img_hover = font_images[font_name]["hover"]

    btn = Button(parent, image=img_default, borderwidth=0,
                 command=lambda f=font_name: select_font(f),
                 takefocus=True)
    btn.image = img_default
    btn.place(x=0, y=y_offset)

    def on_enter(event):
        debug_print(f"ENTER: {font_name}")
        btn.config(image=img_hover)

    def on_leave(event):
        debug_print(f"LEAVE: {font_name}")
        btn.config(image=img_default)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    alternate_buttons.append(btn)


def crop_green_edges(img, green=(0, 255, 0)):
    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size

    left = width
    right = 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (r, g, b) != green and a != 0:
                left = min(left, x)
                right = max(right, x)

    if right < left:
        return img.crop((0, 0, 1, height))  # Empty fallback

    return img.crop((left, 0, right + 1, height))


def open_preview_window(animated=True):
    name = my_entry.get().strip()
    font = font_var.get()
    
    sprite_data = render_name_sprite(name, font)
    if not sprite_data:
        hidden_label.config(text="Invalid or empty name.", font=("Courier New", 14))
        return
    
    # Generate transparent name sprite for scrolling
    name_sprite_transparent, _ = sprite_data

    # Generate green-background version for static preview
    green_bg = Image.new("RGBA", name_sprite_transparent.size, (0, 255, 0, 255))
    name_sprite_green = green_bg.copy()
    name_sprite_green.paste(name_sprite_transparent, (0, 0), name_sprite_transparent)

    preview_win = Toplevel(root)
    preview_win.title("Sprite Preview")
    preview_win.geometry("500x500")
    preview_win.configure(bg="#313131")

    canvas = Canvas(preview_win, width=500, height=500, bg="#313131", highlightthickness=0)
    canvas.pack()

    # Crop name sprite and add border
    cropped_static = crop_green_edges(name_sprite_green)
    border_size = 3  # You can set this to 1 or 2

    # Create a new canvas with extra width, same height
    bordered_static = Image.new("RGBA",
        (cropped_static.width + border_size * 2, cropped_static.height),
        (0, 255, 0, 255)  # Solid green background
    )

    # Paste the cropped image into the center horizontally
    bordered_static.paste(cropped_static, (border_size, 0), cropped_static)

    # Place static name preview
    static_img = ImageTk.PhotoImage(bordered_static.resize(
        (bordered_static.width * 2, bordered_static.height * 2), Image.NEAREST))

    canvas.create_image((500 - static_img.width()) // 2, 30, anchor="nw", image=static_img)
    canvas.static_img = static_img  # Prevent garbage collection
    
    # Load background frames
    bg_paths = [
        resource_path("assets/Backgrounds/preview_bg_1.png"),
        resource_path("assets/Backgrounds/preview_bg_2.png")
    ]
    bg_frames = []

    for path in bg_paths:
        raw = Image.open(path).convert("RGB")
        upscaled_bg = raw.resize((raw.width * 2, raw.height * 2), Image.NEAREST)
        bg_frames.append(ImageTk.PhotoImage(upscaled_bg))

    bg_x = (500 - bg_frames[0].width()) // 2
    bg_y = (500 - bg_frames[0].height()) // 2
    bg_id = canvas.create_image(bg_x, bg_y, anchor="nw", image=bg_frames[0])
    bg_width = bg_frames[0].width()
    bg_height = bg_frames[0].height()
    
    def animate_bg(index=0):
        canvas.itemconfig(bg_id, image=bg_frames[index])
        next_index = (index + 1) % len(bg_frames)
        preview_win.after(750, animate_bg, next_index)

    animate_bg()

    left_mask = canvas.create_rectangle(0, bg_y, bg_x, bg_y + bg_height, fill="#313131", outline="")
    right_mask = canvas.create_rectangle(bg_x + bg_width, bg_y, 500, bg_y + bg_height, fill="#313131", outline="")

    # Generate and upscale name sprite
    name = my_entry.get()
    font = font_var.get()
    
    upscaled = name_sprite_transparent.resize((name_sprite_transparent.width * 2, name_sprite_transparent.height * 2), Image.NEAREST)
    name_img = ImageTk.PhotoImage(upscaled)

    # Srolling name sprite
    scroll_img = ImageTk.PhotoImage(name_sprite_transparent.resize(
        (name_sprite_transparent.width * 2, name_sprite_transparent.height * 2), Image.NEAREST))
    canvas.scroll_img = scroll_img  # Prevent garbage collection

    scroll_left_bound = bg_x
    scroll_right_start = bg_x + bg_frames[0].width()

    canvas.name_img = name_img
    name_id = canvas.create_image(scroll_right_start, bg_y, anchor="nw", image=scroll_img)

    canvas.tag_raise(left_mask)
    canvas.tag_raise(right_mask)

    def scroll_name():
        canvas.move(name_id, -2, 0)
        x = canvas.coords(name_id)[0]

        if x + scroll_img.width() <= scroll_left_bound:
            canvas.coords(name_id, scroll_right_start, bg_y)

        preview_win.after(50, scroll_name)
    
    scroll_name()

    debug_print("Scroll bounds:", scroll_left_bound, scroll_right_start)
    debug_print("Name width:", scroll_img.width())
    debug_print("Current X:", canvas.coords(name_id)[0])

    close_btn = Button(preview_win, text="Close Preview", command=preview_win.destroy,
                   font=("Courier New", 14), relief="flat")
    close_btn.place(x=250, y= 450, anchor="center")



def extract_plain_text_from_rtf(path):
    with open(path, 'r') as f:
        raw = f.read()
    import re
    text = re.sub(r'{\\[^}]+}|\\[a-z]+\d*|{|}', '', raw)
    lines = [line.strip().rstrip('\\') for line in text.splitlines() if line.strip()]
    return lines


def on_drag_enter(event):
    debug_print("Drag entered")
    debug_print("Type of overlay_label:", type(overlay_label))
    global overlay_active
    if overlay_active:
        return
    overlay_active = True
    overlay_label.lift()


def on_drag_leave(event):
    # Delay hiding to prevent flicker
    root.after(2000, hide_overlay)


def hide_overlay():
    global overlay_active
    if not overlay_active:
        return
    overlay_active = False
    overlay_label.lower()


def show_output_button():
    output_button.place(x=20, y=20)  # Or .grid(), depending on layout


def open_output_folder():
    print("Opening output folder...")
    output_path = os.path.expanduser("~/Desktop/DIMNameGenDS_Output")
    if sys.platform == "win32":
        os.startfile(output_path)
    elif sys.platform == "darwin":
        subprocess.call(["open", output_path])
    elif sys.platform.startswith("linux"):
        subprocess.call(["xdg-open", output_path])


def render_name_sprite(name, font_name):
    # All your existing logic that builds namesprite2
    charsheet = load_font_sheet(font_name)
    if not charsheet:
        hidden_label.config(text=f"Font sheet '{font_name}' not found.", font=("Courier New", 14))
        return
    
    letters = map_characters(charsheet, font_name)
    if not letters:
        hidden_label.config(text=f"Font '{font_name}' has no character map.", font=("Courier New", 14))
        return
    
    display_name = name.strip()  # Keep original for rendering
    safe_filename = cleanFilename(display_name) or "default_name" # Used only for saving
    cleaned_name = cleanFilename(name)

    if not cleaned_name:
        hidden_label.config(text="Invalid or empty name.", font=("Courier New", 14))
        return
    
    if font_name in ("Official Bandai", "Agero"):
        cleaned_name = cleaned_name.upper()

    # ✅ Use cleaned_name for character validation
    unsupported = [c for c in cleaned_name if c not in letters]
    if unsupported:
        chars = ' '.join(unsupported)
        hidden_label.config(
            text=f"Nothing generated. Unsupported characters: {chars}",
            font=("Courier New", 14)
        )
        print("Unsupported characters:", unsupported)
        return

    print("Checking for unsupported characters in:", name)
    print("Available characters:", list(letters.keys()))

    if font_name in ("Official Bandai", "Agero"):
        display_name = display_name.upper()

    # Set X position padding
    x = 1

    # Create starter name sprite
    canvas_w = 80
    namesprite = Image.new("RGBA", (canvas_w, 15), (0, 0, 0, 0))

    # Rendering Loop
    # Iterate through each letter, check how close the two adjoining letters are and add space if too close.
    prev_char = None
    space_after_g = {"J", "T", "a", "c", "d", "e", "f", "j", "-", ".", ":", ")", "1", "7"}  # Add more as needed: {"T", "Y", "V", "W"}
    
    def remove_green(img, threshold=10):
        img = img.convert("RGBA")
        datas = img.getdata()
        new_data = []

        for r, g, b, a in datas:
            if abs(r - 0) < threshold and abs(g - 255) < threshold and abs(b - 0) < threshold:
                new_data.append((0, 0, 0, 0))  # Transparent
            else:
                new_data.append((r, g, b, a))

        img.putdata(new_data)
        return img

    for elem in display_name:
        x += 1
        y = 3

        # Special kerning tweak for MON endings in Agero
        if font_name == "Agero" and prev_char == "O" and elem == "N" and cleaned_name.endswith("MON"):
            x += 0  # or x += 1 if spacing is too tight
            print(f"Rendering '{elem}' after '{prev_char}' at x={x}")

        # If the current X position for the next letter would go beyond the sprites current width, increase width another 80px
        if x + letters[elem].width > canvas_w:
            namesprite = ImageOps.expand(namesprite, (0, 0, 80, 0), (0, 0, 0, 0)) # Fully Transparent
            canvas_w += 80

        # This simulates the kerning style from the officially released Vital Hero name sprites
        while y <= 12:
            if letters[elem].getpixel((0, y)) != white:
                y+=1
                continue

            if (
                namesprite.getpixel((x-2, y)) == white or
                namesprite.getpixel((x-2, y-1)) == white or
                namesprite.getpixel((x-2, y-2)) == white or
                namesprite.getpixel((x-2, y+1)) == white or
                namesprite.getpixel((x-2, y+2)) == white
            ):

                x += 1

            else:
                y += 1

        # Special kerning rule for DigiScript: g followed by another letter
        if font_name == "DigiScript" and prev_char == "g" and elem in space_after_g:
            print(f"Kerning tweak applied between 'g' and '{elem}'")
            x -= 1

    
        # Add letter into name sprite canvas
        letter = remove_green(letters[elem])
        namesprite.paste(letter, (x, 0), letter)
        x += letters[elem].width
        prev_char = elem
         
    # Get width of actual text
    text_w = canvas_w - 1
    y = 3
    while text_w > 0:
        if namesprite.getpixel((text_w, y)) == white:
            break
        elif y < 12:
            y = y + 1
        else:
            text_w = text_w - 1
            y = 3
    # Remove two pixel border on left side
    text_w = text_w - 2
    
    # Determine left padding based on canvas width
    lmargin = 0
    if canvas_w == 80:
        # Center sprite with a left margin of at least 2px
        x = (80 - text_w) // 80
        lmargin = x - 2
    elif canvas_w == 160:
        # Add a 3px or 4px left margin based on wether the first letter is serif
        x = 3 if (cleaned_name[0] in serif) else 4
        if text_w + x > 160:
            lmargin = 0
        else:
            lmargin = 0
    else:
        # Add a 5px or 6px left margin based on wether the first letter is serif
        x = 5 if (cleaned_name[0] in serif) else 6
        if text_w + x > 240:
            lmargin = 0
        else:
            lmargin = 0
    if lmargin < 0:
        lmargin = 0

    # TODO: Check if right margin is at least 2x. If not, use alternate MON kerning
    if cleaned_name[-3::1] == "MON" and font_name != "Agero":
        if (text_w + 2 + lmargin) > (canvas_w - 3):
            if (text_w + 2 + lmargin) == (canvas_w - 1):
                x = canvas_w - 36
            else:
                x = canvas_w - 37
            namesprite.paste(remove_green(letters["M"]), (x, 0), remove_green(letters["M"]))
            x += letters["M"].width
            namesprite.paste(remove_green(letters[" "]), (x+12, 0), remove_green(letters[" "]))
            x += letters["M"].width
            namesprite.paste(remove_green(letters["O"]), (x+13, 0), remove_green(letters["O"]))
            x += letters["M"].width
            namesprite.paste(remove_green(letters[" "]), (x+23, 0), remove_green(letters[" "]))
            x += letters["M"].width
            namesprite.paste(remove_green(letters["N"]), (x+24, 0), remove_green(letters["N"]))
            x += letters["M"].width
            namesprite.paste(remove_green(letters[" "]), (x+34, 0), remove_green(letters[" "]))
            x += letters["M"].width

    # Debug
    if font_name == "Agero" and elem == "M":
        debug_print(f"Placing 'M' after '{prev_char}' at x={x}")


    # Create new canvas to paste into
    namesprite2 = Image.new("RGBA", namesprite.size, (0, 0, 0, 0)) # Fully Transparent
    namesprite2.paste(namesprite, (0, 0), namesprite)  # Use letter as its own mask

    return namesprite2, safe_filename


def export_sprite(name: str, font_name: str = "DigiScript", use_official_sprite=False):
    sprite_data = render_name_sprite(name, font_name)
    if not sprite_data:
        hidden_label.config(text="Invalid or empty name.", font=("Courier New", 14))
        return

    sprite, safe_filename = sprite_data

    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "DIMNameGenDS_Output")
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir,
        f"{safe_filename.upper()}.png" if font_name in ("Official Bandai", "Agero") else f"{safe_filename}.png")
    
    bandai_used = False
    if use_official_sprite and font_name == "Official Bandai":
        bandai_path = f"assets/Official Bandai Sprites/{name.strip().upper()}.png"
        if os.path.exists(bandai_path):
            sprite = Image.open(bandai_path).convert("RGBA")  # Override with Bandai sprite
            bandai_used = True

    if bandai_used:
        sprite.save(filename)  # Already has green background
    else:
        green_bg = Image.new("RGBA", sprite.size, (0, 255, 0, 255))
        sprite_with_green = green_bg.copy()
        sprite_with_green.paste(sprite, (0, 0), sprite)
        sprite_with_green.save(filename)

    print(f"Exported to: {filename}")

    # Conditional message
    if bandai_used:
        message = f"Saved official Bandai sprite as {os.path.basename(filename)} to output folder"
    else:
        message = f"{os.path.basename(filename)} generated with {font_name} font to output folder"
    
    hidden_label.config(
        text=message,
        font=("Courier New", 14),
        wraplength=625,
        justify="center"
    )

    show_output_button()
    

def main(name: str, font_name: str = "DigiScript", preview_label=None):
    global output_dir
    namesprite2, safe_filename = render_name_sprite(name, font_name)

    # Update preview if label is provided
    if preview_label:
        preview_image = ImageTk.PhotoImage(namesprite2)
        preview_label.config(image=preview_image)
        preview_label.image = preview_image

    charsheet = load_font_sheet(font_name)
    if not charsheet:
        hidden_label.config(text=f"Font sheet '{font_name}' not found.", font=("Courier New", 14))
        return
    
    letters = map_characters(charsheet, font_name)
    if not letters:
        hidden_label.config(text=f"Font '{font_name}' has no character map.", font=("Courier New", 14))
        return
    
    display_name = name.strip()  # Keep original for rendering
    safe_filename = cleanFilename(display_name) or "default_name" # Used only for saving
    cleaned_name = cleanFilename(name)

    if not cleaned_name:
        hidden_label.config(text="Invalid or empty name.", font=("Courier New", 14))
        return
    
    if font_name in ("Official Bandai", "Agero"):
        cleaned_name = cleaned_name.upper()

    if font_name == "Agero":
        safe_filename = safe_filename.upper()


    # ✅ Use cleaned_name for character validation
    unsupported = [c for c in cleaned_name if c not in letters]
    if unsupported:
        chars = ' '.join(unsupported)
        hidden_label.config(
            text=f"Nothing generated. Unsupported characters: {chars}",
            font=("Courier New", 14)
        )
        print("Unsupported characters:", unsupported)
        return

    print("Checking for unsupported characters in:", name)
    print("Available characters:", list(letters.keys()))

    if font_name in ("Official Bandai", "Agero"):
        display_name = display_name.upper()
    
    # Show fallback message if Bandai font selected but sprite not found
    elif font_name == "Official Bandai":
        hidden_label.config(
            text=f"No official Bandai sprite found for '{cleaned_name}'. Generating from Bandai font sheet...",
            font=("Courier New", 14),
            wraplength=625,
            justify="center"
        )
        print("Fallback rendering triggered for:", cleaned_name)
        show_output_button()

    # Set X position padding
    x = 1

    # Create starter name sprite
    canvas_w = 80
    namesprite = Image.new("RGB", (canvas_w, 15), green)

    # Rendering Loop
    # Iterate through each letter, check how close the two adjoining letters are and add space if too close.
    prev_char = None
    space_after_g = {"J", "T", "a", "c", "d", "e", "f", "j", "-", ".", ":", ")", "1", "7"}  # Add more as needed: {"T", "Y", "V", "W"}
    
    for elem in display_name:
        x += 1
        y = 3

        # Special kerning tweak for MON endings in Agero
        if font_name == "Agero" and prev_char == "O" and elem == "N" and cleaned_name.endswith("MON"):
            x -= 1  # or x += 1 if spacing is too tight
            print(f"Rendering '{elem}' after '{prev_char}' at x={x}")

        # If the current X position for the next letter would go beyond the sprites current width, increase width another 80px
        if x + letters[elem].width > canvas_w:
            namesprite = ImageOps.expand(namesprite, (0, 0, 80, 0), green)
            canvas_w += 80

        # This simulates the kerning style from the officially released Vital Hero name sprites
        while y <= 12:
            if letters[elem].getpixel((0, y)) != white:
                y+=1
                continue

            if (
                namesprite.getpixel((x-2, y)) == white or
                namesprite.getpixel((x-2, y-1)) == white or
                namesprite.getpixel((x-2, y-2)) == white or
                namesprite.getpixel((x-2, y+1)) == white or
                namesprite.getpixel((x-2, y+2)) == white
            ):

                x += 1

            else:
                y += 1

        # Special kerning rule for DigiScript: g followed by another letter
        if font_name == "DigiScript" and prev_char == "g" and elem in space_after_g:
            print(f"Kerning tweak applied between 'g' and '{elem}'")
            x -= 1

        # Add letter into name sprite canvas
        namesprite.paste(letters[elem], (x, 0))
        x += letters[elem].width
        prev_char = elem
         
    # Get width of actual text
    text_w = canvas_w - 1
    y = 3
    while text_w > 0:
        if namesprite.getpixel((text_w, y)) == white:
            break
        elif y < 12:
            y = y + 1
        else:
            text_w = text_w - 1
            y = 3
    # Remove two pixel border on left side
    text_w = text_w - 2
    
    # Determine left padding based on canvas width
    lmargin = 0
    if canvas_w == 80:
        # Center sprite with a left margin of at least 2px
        x = (80 - text_w) // 80
        lmargin = x - 2
    elif canvas_w == 160:
        # Add a 3px or 4px left margin based on wether the first letter is serif
        x = 3 if (cleaned_name[0] in serif) else 4
        if text_w + x > 160:
            lmargin = 0
        else:
            lmargin = 0
    else:
        # Add a 5px or 6px left margin based on wether the first letter is serif
        x = 5 if (cleaned_name[0] in serif) else 6
        if text_w + x > 240:
            lmargin = 0
        else:
            lmargin = 0
    if lmargin < 0:
        lmargin = 0

    # TODO: Check if right margin is at least 2x. If not, use alternate MON kerning
    if cleaned_name[-3::1] == "MON" and font_name != "Agero":
        if (text_w + 2 + lmargin) > (canvas_w - 3):
            if (text_w + 2 + lmargin) == (canvas_w - 1):
                x = canvas_w - 36
            else:
                x = canvas_w - 37
            namesprite.paste(letters["M"], (x, 0))
            x += letters["M"].width
            namesprite.paste(letters[" "], (x+12, 0))
            x += letters["M"].width
            namesprite.paste(letters["O"], (x+13, 0))
            x += letters["M"].width
            namesprite.paste(letters[" "], (x+23, 0))
            x += letters["M"].width
            namesprite.paste(letters["N"], (x+24, 0))
            x += letters["M"].width
            namesprite.paste(letters[" "], (x+34, 0))
            x += letters["M"].width

    # Debug
    if font_name == "Agero" and elem == "M":
        debug_print(f"Placing 'M' after '{prev_char}' at x={x}")


    # Create new canvas to paste into
    namesprite2 = Image.new("RGB", (canvas_w, 15), green)
    namesprite2.paste(namesprite)


    if preview_label is not None:
        preview_image = ImageTk.PhotoImage(namesprite2)
        preview_label.config(image=preview_image)
        preview_label.image = preview_image  # Prevent garbage collection


def handle_drop(event):
    file_path = event.data.strip('{}')
    selected_font = font_var.get()

    # Parse file
    if file_path.lower().endswith(".rtf"):
        names = extract_plain_text_from_rtf(file_path)
    elif file_path.lower().endswith(".txt"):
        with open(file_path, 'r') as f:
            names = [line.strip() for line in f if line.strip()]
    else:
        hidden_label.config(text="Unsupported file type. Please drop a .txt or .rtf file.",
                            font=("Courier New", 14),
                            wraplength=625,
                            justify="center")
        return

    # ✅ Define cleaned_names before using it
    allowed_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -:.()1234567890")
    
    cleaned_names = []
    for raw_name in names:
        display_name = raw_name.strip()
        unsupported = [c for c in display_name if c not in allowed_chars]
        if unsupported:
            print(f"Unsupported characters in '{display_name}': {unsupported}")
        cleaned = ''.join(c for c in display_name if c in allowed_chars)
        if cleaned:
            cleaned_names.append(cleaned)

    # ✅ Now it's safe to loop
    for name in cleaned_names:
        export_sprite(name, selected_font)

    
    show_output_button()
    # ✅ Hide overlay and border after drop
    root.after(2000, hide_overlay)


def map_characters(charsheet, font_name):
    font_name = font_name.strip().lower()
    letters = {} # Initialize the dictionary

    if font_name == "digiscript":
        # Original cropping logic - Dictionary map letters to alphabet sprite sheet
        letters["A"] = charsheet.crop((0, 0, 8, 15))
        letters["B"] = charsheet.crop((9, 0, 16, 15))
        letters["C"] = charsheet.crop((17, 0, 24, 15))
        letters["D"] = charsheet.crop((25, 0, 32, 15))
        letters["E"] = charsheet.crop((33, 0, 39, 15))
        letters["F"] = charsheet.crop((40, 0, 46, 15))
        letters["G"] = charsheet.crop((47, 0, 54, 15))
        letters["H"] = charsheet.crop((55, 0, 63, 15))
        letters["I"] = charsheet.crop((64, 0, 67, 15))
        letters["J"] = charsheet.crop((68, 0, 75, 15))
        letters["K"] = charsheet.crop((76, 0, 83, 15))
        letters["L"] = charsheet.crop((84, 0, 90, 15))
        letters["M"] = charsheet.crop((91, 0, 102, 15))

        letters["N"] = charsheet.crop((103, 0, 114, 15))
        letters["O"] = charsheet.crop((115, 0, 123, 15))
        letters["P"] = charsheet.crop((124, 0, 131, 15))
        letters["Q"] = charsheet.crop((132, 0, 140, 15))
        letters["R"] = charsheet.crop((141, 0, 148, 15))
        letters["S"] = charsheet.crop((149, 0, 157, 15))
        letters["T"] = charsheet.crop((158, 0, 165, 15))
        letters["U"] = charsheet.crop((166, 0, 174, 15))
        letters["V"] = charsheet.crop((175, 0, 183, 15))
        letters["W"] = charsheet.crop((184, 0, 195, 15))
        letters["X"] = charsheet.crop((196, 0, 203, 15))
        letters["Y"] = charsheet.crop((204, 0, 211, 15))
        letters["Z"] = charsheet.crop((212, 0, 219, 15))

        letters["a"] = charsheet.crop((220, 0, 226, 15))
        letters["b"] = charsheet.crop((227, 0, 233, 15))
        letters["c"] = charsheet.crop((234, 0, 240, 15))
        letters["d"] = charsheet.crop((241, 0, 247, 15))
        letters["e"] = charsheet.crop((248, 0, 254, 15))
        letters["f"] = charsheet.crop((255, 0, 260, 15))
        letters["g"] = charsheet.crop((261, 0, 268, 15))
        letters["h"] = charsheet.crop((269, 0, 276, 15))
        letters["i"] = charsheet.crop((277, 0, 279, 15))
        letters["j"] = charsheet.crop((280, 0, 284, 15))
        letters["k"] = charsheet.crop((285, 0, 291, 15))
        letters["l"] = charsheet.crop((292, 0, 294, 15))
        letters["m"] = charsheet.crop((295, 0, 305, 15))

        letters["n"] = charsheet.crop((306, 0, 313, 15))
        letters["o"] = charsheet.crop((314, 0, 320, 15))
        letters["p"] = charsheet.crop((321, 0, 327, 15))
        letters["q"] = charsheet.crop((328, 0, 334, 15))
        letters["r"] = charsheet.crop((335, 0, 341, 15))
        letters["s"] = charsheet.crop((342, 0, 348, 15))
        letters["t"] = charsheet.crop((349, 0, 354, 15))
        letters["u"] = charsheet.crop((355, 0, 361, 15))
        letters["v"] = charsheet.crop((362, 0, 368, 15))
        letters["w"] = charsheet.crop((369, 0, 379, 15))
        letters["x"] = charsheet.crop((380, 0, 387, 15))
        letters["y"] = charsheet.crop((388, 0, 396, 15))
        letters["z"] = charsheet.crop((397, 0, 403, 15))

        letters[" "] = charsheet.crop((404, 0, 407, 15))
        letters["-"] = charsheet.crop((408, 0, 411, 15))
        letters[":"] = charsheet.crop((412, 0, 414, 15))
        letters["."] = charsheet.crop((415, 0, 417, 15))
        letters["("] = charsheet.crop((418, 0, 422, 15))
        letters[")"] = charsheet.crop((423, 0, 427, 15))
        
        letters["1"] = charsheet.crop((428, 0, 433, 15))
        letters["2"] = charsheet.crop((434, 0, 441, 15))
        letters["3"] = charsheet.crop((442, 0, 448, 15))
        letters["4"] = charsheet.crop((449, 0, 455, 15))
        letters["5"] = charsheet.crop((456, 0, 463, 15))
        letters["6"] = charsheet.crop((464, 0, 471, 15))
        letters["7"] = charsheet.crop((472, 0, 479, 15))
        letters["8"] = charsheet.crop((480, 0, 486, 15))
        letters["9"] = charsheet.crop((487, 0, 493, 15))
        letters["0"] = charsheet.crop((494, 0, 501, 15))
        
    elif font_name == "official bandai":
        # Alternate cropping logic - Dictionary map letters to alphabet sprite sheet
        letters["A"] = charsheet.crop((0, 0, 9, 15))
        letters["B"] = charsheet.crop((10, 0, 17, 15))
        letters["C"] = charsheet.crop((18, 0, 26, 15))
        letters["D"] = charsheet.crop((27, 0, 35, 15))
        letters["E"] = charsheet.crop((36, 0, 41, 15))
        letters["F"] = charsheet.crop((42, 0, 47, 15))
        letters["G"] = charsheet.crop((48, 0, 58, 15))
        letters["H"] = charsheet.crop((59, 0, 67, 15))
        letters["I"] = charsheet.crop((68, 0, 70, 15))
        letters["J"] = charsheet.crop((71, 0, 77, 15))
        letters["K"] = charsheet.crop((78, 0, 86, 15))
        letters["L"] = charsheet.crop((87, 0, 92, 15))
        letters["M"] = charsheet.crop((93, 0, 105, 15))

        letters["N"] = charsheet.crop((106, 0, 116, 15))
        letters["O"] = charsheet.crop((117, 0, 127, 15))
        letters["P"] = charsheet.crop((128, 0, 135, 15))
        letters["Q"] = charsheet.crop((136, 0, 146, 15))
        letters["R"] = charsheet.crop((147, 0, 154, 15))
        letters["S"] = charsheet.crop((155, 0, 163, 15))
        letters["T"] = charsheet.crop((164, 0, 170, 15))
        letters["U"] = charsheet.crop((171, 0, 179, 15))
        letters["V"] = charsheet.crop((180, 0, 190, 15))
        letters["W"] = charsheet.crop((191, 0, 204, 15))
        letters["X"] = charsheet.crop((205, 0, 215, 15))
        letters["Y"] = charsheet.crop((216, 0, 224, 15))
        letters["Z"] = charsheet.crop((225, 0, 234, 15))

        letters[" "] = charsheet.crop((235, 0, 239, 15))
        letters["-"] = charsheet.crop((240, 0, 244, 15))
        letters[":"] = charsheet.crop((245, 0, 247, 15))
        letters["."] = charsheet.crop((248, 0, 250, 15))
        letters["("] = charsheet.crop((251, 0, 255, 15))
        letters[")"] = charsheet.crop((256, 0, 260, 15))
        
        letters["1"] = charsheet.crop((261, 0, 264, 15))
        letters["2"] = charsheet.crop((265, 0, 270, 15))
        letters["3"] = charsheet.crop((271, 0, 276, 15))
        letters["4"] = charsheet.crop((277, 0, 283, 15))
        letters["5"] = charsheet.crop((284, 0, 289, 15))
        letters["6"] = charsheet.crop((290, 0, 296, 15))
        letters["7"] = charsheet.crop((297, 0, 302, 15))
        letters["8"] = charsheet.crop((303, 0, 309, 15))
        letters["9"] = charsheet.crop((310, 0, 316, 15))
        letters["0"] = charsheet.crop((317, 0, 323, 15))

    elif font_name == "agero":
        # Alternate cropping logic - Dictionary map letters to alphabet sprite sheet
        letters["A"] = charsheet.crop((0, 0, 10, 15))
        letters["B"] = charsheet.crop((11, 0, 21, 15))
        letters["C"] = charsheet.crop((22, 0, 32, 15))
        letters["D"] = charsheet.crop((33, 0, 44, 15))
        letters["E"] = charsheet.crop((45, 0, 56, 15))
        letters["F"] = charsheet.crop((57, 0, 67, 15))
        letters["G"] = charsheet.crop((68, 0, 78, 15))
        letters["H"] = charsheet.crop((79, 0, 89, 15))
        letters["I"] = charsheet.crop((90, 0, 94, 15))
        letters["J"] = charsheet.crop((95, 0, 105, 15))
        letters["K"] = charsheet.crop((106, 0, 116, 15))
        letters["L"] = charsheet.crop((117, 0, 128, 15))
        letters["M"] = charsheet.crop((129, 0, 144, 15))

        letters["N"] = charsheet.crop((145, 0, 156, 15))
        letters["O"] = charsheet.crop((157, 0, 167, 15))
        letters["P"] = charsheet.crop((168, 0, 179, 15))
        letters["Q"] = charsheet.crop((180, 0, 190, 15))
        letters["R"] = charsheet.crop((191, 0, 201, 15))
        letters["S"] = charsheet.crop((202, 0, 214, 15))
        letters["T"] = charsheet.crop((215, 0, 226, 15))
        letters["U"] = charsheet.crop((227, 0, 238, 15))
        letters["V"] = charsheet.crop((239, 0, 249, 15))
        letters["W"] = charsheet.crop((250, 0, 264, 15))
        letters["X"] = charsheet.crop((265, 0, 276, 15))
        letters["Y"] = charsheet.crop((277, 0, 288, 15))
        letters["Z"] = charsheet.crop((289, 0, 300, 15))

        letters[" "] = charsheet.crop((301, 0, 310, 15))
        letters["-"] = charsheet.crop((311, 0, 321, 15))
        letters[":"] = charsheet.crop((322, 0, 326, 15))
        letters["."] = charsheet.crop((327, 0, 332, 15))
        letters["("] = charsheet.crop((333, 0, 339, 15))
        letters[")"] = charsheet.crop((340, 0, 346, 15))
        
        letters["1"] = charsheet.crop((347, 0, 355, 15))
        letters["2"] = charsheet.crop((356, 0, 369, 15))
        letters["3"] = charsheet.crop((370, 0, 381, 15))
        letters["4"] = charsheet.crop((382, 0, 396, 15))
        letters["5"] = charsheet.crop((397, 0, 410, 15))
        letters["6"] = charsheet.crop((411, 0, 423, 15))
        letters["7"] = charsheet.crop((424, 0, 436, 15))
        letters["8"] = charsheet.crop((437, 0, 448, 15))
        letters["9"] = charsheet.crop((449, 0, 462, 15))
        letters["0"] = charsheet.crop((463, 0, 475, 15))


    else:
        print(f"[Warning] No character map defined for font: '{font_name}'")

    return letters


def load_font_sheet(font_name):
    font_files = {
        "DigiScript": "VB_Alphabet_ENG_DigiScript",
        "Official Bandai": "VB_Alphabet_ENG_Official_Bandai",
        "Agero": "VB_Alphabet_Eng_Agero"}
    try:
        filename = font_files.get(font_name, font_name)
        return Image.open(load_file(f'assets/Fonts/{filename}.png')).convert("RGB")
    except FileNotFoundError:
        hidden_label.config(text=f"Font sheet '{font_name}' not found.", font=("Courier New", 14))
        return None
    

def load_file(file_name: str) -> str:
        return os.path.join(os.path.dirname(__file__), file_name)

def cleanFilename(sourcestring,  removestring = "%/,.\\[]<>*?:|'"):
    """Clean a string by removing selected characters.

    Creates a legal and 'clean' source string from a string by removing some 
    clutter and  characters not allowed in filenames.
    A default set is given but the user can override the default string.

    Args:
        | sourcestring (string): the string to be cleaned.
        | removestring (string): remove all these characters from the string (optional).

    Returns:
        | (string): A cleaned-up string.

    Raises:
        | No exception is raised.
    """
    #remove the undesireable characters
    return ''.join(c for c in sourcestring if c not in removestring)


def change():
    raw_name = my_entry.get().strip()
    selected_font = font_var.get()

    if not raw_name:
        hidden_label.config(text="Invalid entry. Please enter a name.", font=("Courier New", 14))
        return

    print(f"Name submitted: {raw_name} with font: {selected_font}")
    export_sprite(raw_name, selected_font, use_official_sprite=True)  # or False if you want to skip Bandai
    my_entry.delete(0, 'end')


def handle_enter_key(event=None):
    # Function to be called when Enter key is pressed
    change() # Call the same function as the button's command





# ---------- Main Script ----------

# Create root window
root.title("DIM Name Generator DS")
root.geometry('700x275')
root.configure(bg="#313131")

# Call UI setup
setup_ui()

# Start GUI loop
root.mainloop()
