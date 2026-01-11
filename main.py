import os
import tkinter as tk
from tkinter import filedialog as fd, messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

PREVIEW_SIZE = 86
CHECKER_SIZE = 8

def set_image_path(path):
    path = path.strip("{}")  # windows drag fix

    entryImg.delete(0, tk.END)
    entryImg.insert(0, path)

    entryOut.delete(0, tk.END)
    entryOut.insert(0, os.path.dirname(path))

    update_preview(path)

def create_checkerboard(size=PREVIEW_SIZE, square=CHECKER_SIZE):
    img = Image.new("RGBA", (size, size), (196, 196, 196, 255))
    for y in range(0, size, square):
        for x in range(0, size, square):
            if (x // square + y // square) % 2 == 0:
                for i in range(square):
                    for j in range(square):
                        if x+i < size and y+j < size:
                            img.putpixel((x+i, y+j), (128, 128, 128, 255))
    return img

def update_preview(path):
    try:
        # Load the image
        img = Image.open(path).convert("RGBA")
        img.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE), Image.LANCZOS)

        # Create checkerboard
        checker = create_checkerboard()

        # Center the image on the checkerboard
        offset_x = (PREVIEW_SIZE - img.width) // 2
        offset_y = (PREVIEW_SIZE - img.height) // 2
        checker.paste(img, (offset_x, offset_y), mask=img)

        tk_img = ImageTk.PhotoImage(checker)
        previewLabel.config(image=tk_img, text="")
        previewLabel.image = tk_img

    except Exception:
        previewLabel.config(image="", text="No preview")
        previewLabel.image = None

def on_drop(event):
    files = window.tk.splitlist(event.data)
    if files:
        set_image_path(files[0])

def select_image():
    filepath = fd.askopenfilename(
        title='Select an image',
        filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp')]
    )
    if filepath:
        set_image_path(filepath)

def select_output_dir():
    directory = fd.askdirectory(title="Select output directory")
    if directory:
        entryOut.delete(0, tk.END)
        entryOut.insert(0, directory)

def convert_to_ico():
    img_path = entryImg.get()
    out_dir = entryOut.get()

    if not img_path or not out_dir:
        messagebox.showerror("Error", "Missing image or output directory")
        return

    try:
        os.makedirs(out_dir, exist_ok=True)

        img = Image.open(img_path).convert("RGBA")
        name = os.path.splitext(os.path.basename(img_path))[0]
        ico_path = os.path.join(out_dir, name + ".ico")

        img.save(ico_path, format="ICO", sizes=[
            (16, 16),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
            (256, 256),
        ])

        messagebox.showinfo("Success", f"Saved:\n{ico_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# windowswsws

DARK_BG = "#0d0e0f"
FG_COLOR = "white"
ENTRY_FG = "#cfcfcf"
ENTRY_BG = "#28292e"



# ---- main window
window = TkinterDnD.Tk()
window.title("img-to-ico")
window.resizable(False, False)
window.configure(bg=DARK_BG)

# ---- main frame
main = tk.Frame(window, padx=10, pady=10, bg=DARK_BG)
main.grid()

# ---- img
tk.Label(main, text="Image:", bg=DARK_BG, fg=FG_COLOR).grid(row=0, column=0, sticky="w")

entryImg = tk.Entry(main, width=40, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
entryImg.grid(row=0, column=1, padx=5)
entryImg.drop_target_register(DND_FILES)
entryImg.dnd_bind('<<Drop>>', on_drop)

tk.Button(main, text="Browse", command=select_image, bg=DARK_BG, fg=FG_COLOR).grid(row=0, column=2)

# ----outputs
tk.Label(main, text="Output:", bg=DARK_BG, fg=FG_COLOR).grid(row=1, column=0, sticky="w")

entryOut = tk.Entry(main, width=40, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
entryOut.grid(row=1, column=1, padx=5)

tk.Button(main, text="Browse", command=select_output_dir, bg=DARK_BG, fg=FG_COLOR).grid(row=1, column=2)

# ---- preview image
previewFrame = tk.Frame(
    main,
    width=PREVIEW_SIZE,
    height=PREVIEW_SIZE,
    relief="groove",
    bd=1,
    bg=DARK_BG
)
previewFrame.grid(row=0, column=3, rowspan=2, padx=10)
previewFrame.grid_propagate(False)

previewLabel = tk.Label(previewFrame, text="Drop image\nhere", bg=DARK_BG, fg=FG_COLOR)
previewLabel.place(relx=0.5, rely=0.5, anchor="center")

# ---- convert
convButton = tk.Button(
    main,
    text="Convert to ICO",
    command=convert_to_ico,
    bg=DARK_BG,
    fg=FG_COLOR
)
convButton.grid(row=2, column=2, pady=8, sticky="e")


window.mainloop()
