import customtkinter as ctk

app = ctk.CTk(fg_color="#a7c6ed")
app.geometry("1000x1000")
app.title("Réseau d'eau")

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

frame_haut = ctk.CTkFrame(app, fg_color="#5a8cc2", height=80)
frame_haut.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

label_titre = ctk.CTkLabel(frame_haut, text="Réseau d'eau", text_color="white", font=("Arial", 24, "bold"))
label_titre.pack(expand=True, pady=20)

frame_gauche = ctk.CTkFrame(app, fg_color="#5a8cc2")
frame_gauche.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

menu1 = ctk.CTkOptionMenu(frame_gauche, values=["Option 1", "Option 2", "Option 3"])
menu1.pack(pady=20, padx=20)

menu2 = ctk.CTkOptionMenu(frame_gauche, values=["Ville A", "Ville B", "Ville C"])
menu2.pack(pady=20, padx=20)

frame_droite = ctk.CTkFrame(app, fg_color="#5a8cc2")
frame_droite.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

menu3 = ctk.CTkOptionMenu(frame_droite, values=["Rouge", "Bleu", "Vert"])
menu3.pack(pady=20, padx=20)

menu4 = ctk.CTkOptionMenu(frame_droite, values=["Petit", "Moyen", "Grand"])
menu4.pack(pady=20, padx=20)

button = ctk.CTkButton(app, text="OK", fg_color="red")
button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

app.mainloop()

#ctk.set_appearance_mode("light")

# label=ctk.CTkLabel(app, fg_color="#3d6ba6", text="Bienvenue les loosers", corner_radius=10,width=600, height=30 )
# label.pack(pady=20, padx=20)

# TextBox=ctk.CTkTextbox(app, width=600, height=30)
# TextBox.pack(pady=20, padx=20)

# button = ctk.CTkButton(app, fg_color="#5a8cc2",hover_color="grey", text_color="blue", border_width=4, border_color="black")  
# button.pack(pady=20, padx=20) #pady : marge verticale de 20pix / pack : positionne le widget

# CheckBox=ctk.CTkCheckBox(app, fg_color="blue")
# CheckBox.pack(pady=20, padx=20)

# ProgressBar=ctk.CTkProgressBar(app)
# ProgressBar.pack(pady=20, padx=20)

# Slider=ctk.CTkSlider(app)
# Slider.pack(pady=20, padx=20)

# OptionMenu=ctk.CTkOptionMenu(app, values=["Bonjour", "Salut", "Ciao"])
# OptionMenu.pack(pady=20, padx=20)

# frame1 = ctk.CTkFrame(app, fg_color="#3d6ba6", corner_radius=10)
# frame1.pack(pady=20, padx=20)

# # Widgets dans le frame
# label = ctk.CTkLabel(frame1, text="Bloc 1")
# label.pack(pady=10)

# button = ctk.CTkButton(frame1, text="Cliquer")
# button.pack(pady=10)


