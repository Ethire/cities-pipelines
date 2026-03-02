import customtkinter as ctk

"""app = ctk.CTk(fg_color="#a7c6ed")
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

app.mainloop()"""

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


import customtkinter as ctk

BG_DEEP    = "#070d1a"
BG_DARK    = "#0c1630"
BG_CARD    = "#0f1e3d"
BG_INPUT   = "#132248"
BORDER     = "#1e3a6a"
ACCENT     = "#2563eb"
ACCENT_HVR = "#1d4ed8"
TXT_MAIN   = "#dce9fb"
TXT_SUB    = "#6a93c8"
TXT_DIM    = "#3a5a8a"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Réseau d'eau")
        self.geometry("1000 x 670")
        self.minsize(700, 500)
        self.configure(fg_color=BG_DEEP)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_topbar()
        self._build_main()

        """frame du titre"""
    def _build_topbar(self):
        top = ctk.CTkFrame(self, height=76, corner_radius=0, fg_color=BG_DARK)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.grid_rowconfigure(0,weight=1)
        top.grid_columnconfigure(1,weight=1)

        ctk.CTkLabel(top,text="Réseau d'eau",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TXT_MAIN).grid(row=0, column=1, sticky="")
        
        """Crée un titre de section"""
    def _section_header(self, parent, row, num, title):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=0, padx=20, pady=(18, 6), sticky="ew")
        f.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(f, text=num, font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ACCENT, width=28,
                     fg_color=BG_CARD, corner_radius=6).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TXT_MAIN, anchor="w").grid(row=0, column=1, sticky="w")
        return row + 1

    """Crée un label avec saisie"""
    def _field(self, parent, row, col, label, placeholder):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))

        entry = ctk.CTkEntry(
            f, height=38, corner_radius=8,
            fg_color=BG_INPUT, border_color=BORDER, border_width=1,
            text_color=TXT_MAIN, placeholder_text=placeholder,
            placeholder_text_color=TXT_DIM,
            font=ctk.CTkFont(size=12),
        )
        entry.grid(row=1, column=0, sticky="ew")
        return entry

    """Crée un label avec un menu déroulant"""
    def _optmenu(self, parent, row, col, label, values):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))

        om = ctk.CTkOptionMenu(
            f, values=values, height=38, corner_radius=8,
            fg_color=BG_INPUT, button_color=BORDER, button_hover_color=ACCENT,
            text_color=TXT_MAIN, font=ctk.CTkFont(size=12),
            dropdown_fg_color=BG_CARD, dropdown_hover_color=BORDER,
            dropdown_text_color=TXT_MAIN,
        )
        om.grid(row=1, column=0, sticky="ew")
        return om
       
    # ══════════════════════════════════════════════════════════════════
    #  MAIN
    # ══════════════════════════════════════════════════════════════════
    def _build_main(self):
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=BG_DEEP,
                                        scrollbar_button_color=BORDER,
                                        scrollbar_button_hover_color=ACCENT)
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        row_idx = 0

        # ── Section 1 : Paramètres  ──────────────────────────
        row_idx = self._section_header(scroll, row_idx, "01", "Paramètres ")

        self.entries = {}  # dict qui stockera toutes les CTkEntry

        numeric_fields = [
            ("Nombre de maisons", "Nombre de maisons", "ex : 10"),
            ("Nombre de ramifications", "Nombre de ramifications", "ex : 5"),
            ("Dénivelé", "Dénivelé", "en %"),
        ]

        fields_frame = ctk.CTkFrame(scroll, corner_radius=12,
                                    fg_color=BG_CARD, border_width=1, border_color=BORDER)
        fields_frame.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        fields_frame.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        for i, (key, label, placeholder) in enumerate(numeric_fields):
            self.entries[key] = self._field(fields_frame, i // 2, i % 2, label, placeholder)

        # ── Section 2 : Zone  ─────────────────────────────────
        row_idx = self._section_header(scroll, row_idx, "02", "Zone")

        self.optmenus = {} # dict qui stockera toutes les OptMenu

        options_fields = [
            ("option_1", "Zone", ["Rurale", "Urbaine", "Mix"]),
        ]

        opts_frame = ctk.CTkFrame(scroll, corner_radius=12,
                                  fg_color=BG_CARD, border_width=1, border_color=BORDER)
        opts_frame.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        opts_frame.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        for oi, (key, label, values) in enumerate(options_fields):
            self.optmenus[key] = self._optmenu(opts_frame, oi // 2, oi % 2, label, values)

        btn_frame = ctk.CTkFrame(scroll, corner_radius=0, fg_color="transparent")
        btn_frame.grid(row=row_idx, column=0, padx=20, pady=(8, 28), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)  # 2 colonnes égales

        ctk.CTkButton(
            btn_frame, text="OK", height=48, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HVR, text_color="#ffffff",
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Random", height=48, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HVR, text_color="#ffffff",
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.feedback = ctk.CTkLabel(
            btn_frame, text="", font=ctk.CTkFont(size=11),
            text_color="#3dba6f", wraplength=560
        )
        self.feedback.grid(row=1, column=0, columnspan=2, pady=(8, 0))


app = App()
app.mainloop()