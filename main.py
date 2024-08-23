import os
import tkinter as tk
from tkinter import messagebox, filedialog, Menu
import shutil
import winshell  # Para criar atalhos na área de trabalho e no menu iniciar

def execute_exe(exe_path):
    try:
        os.startfile(exe_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível executar o arquivo: {str(e)}")

def create_shortcut(exe_path, location):
    exe_name = os.path.basename(exe_path)
    shortcut_name = os.path.splitext(exe_name)[0] + ".lnk"
    shortcut_path = os.path.join(location, shortcut_name)

    winshell.CreateShortcut(
        Path=shortcut_path,
        Target=exe_path,
        Icon=(exe_path, 0),
        Description=f"Atalho para {exe_name}"
    )
    messagebox.showinfo("Sucesso", f"Atalho criado: {shortcut_path}")

def create_shortcuts_for_all(exe_paths):
    location_choice = messagebox.askquestion(
        "Escolher Localização",
        "Onde deseja criar os atalhos?\n\n"
        "Área de Trabalho: Escolha 'yes'.\n"
        "Menu Iniciar: Escolha 'no'.\n"
        "Ambos: Escolha 'cancel'."
    )

    if location_choice == "yes":
        locations = [winshell.desktop()]
    elif location_choice == "no":
        locations = [winshell.start_menu()]
    else:
        locations = [winshell.desktop(), winshell.start_menu()]

    for exe_path in exe_paths:
        for location in locations:
            create_shortcut(exe_path, location)

def search_and_create_buttons(root_dir, frame, exe_paths):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        found_exe = False
        for filename in filenames:
            if filename.endswith(".exe"):
                exe_path = os.path.join(dirpath, filename)
                exe_paths.append(exe_path)
                button = tk.Button(frame, text=filename, command=lambda p=exe_path: execute_exe(p))
                button.pack(fill=tk.X, padx=5, pady=5)
                found_exe = True
                break  # Para de procurar na pasta atual assim que encontrar um .exe
        
        if found_exe:
            # Não procurar nas subpastas se um .exe já foi encontrado
            dirnames[:] = []

def create_gui():
    root = tk.Tk()
    root.title("tech tools")
    root.iconbitmap(os.path.abspath("icone.ico"))
    root.configure(bg="black")
    root.geometry("400x600")
    root.minsize(400, 600)

    # Lista para armazenar os caminhos dos arquivos .exe encontrados
    exe_paths = []

    # Criando o menu bar
    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=file_menu)
    file_menu.add_command(label="Criar Ícones", command=lambda: create_shortcuts_for_all(exe_paths))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Adicionando um Canvas para suportar a barra de rolagem
    canvas = tk.Canvas(main_frame, bg="black")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="black")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    search_and_create_buttons("exes", scrollable_frame, exe_paths)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
