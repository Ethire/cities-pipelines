import customtkinter as ctk

# ══════════════════════════════════════════════════════════════════
# PALETTE
# ══════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════
#  Application
# ══════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Réseau d'eau")
        self.geometry("1000x670")
        self.minsize(700, 500)
        self.configure(fg_color=BG_DEEP)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.topbar()
        self.main()

# ══════════════════════════════════════════════════════════════════
#  METHODES
# ══════════════════════════════════════════════════════════════════

    """frame du titre et label"""
    def topbar(self):
        top = ctk.CTkFrame(self, height=76, corner_radius=0, fg_color=BG_DARK)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(top, text="Réseau d'eau",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TXT_MAIN).grid(row=0, column=1, sticky="")

    """Crée un titre de section"""
    def section(self, parent, row, num, title):
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
    def field(self, parent, row, col, label, placeholder):
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

    """Crée un switch avec label"""
    def _switch(self, parent, row, col, label, command=None):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))

        sw = ctk.CTkSwitch(f, text="", width=48,
                           button_color=ACCENT, button_hover_color=ACCENT_HVR,
                           progress_color=ACCENT, fg_color=BORDER,
                           command=command)
        sw.grid(row=1, column=0, sticky="w")
        return sw

    # ══════════════════════════════════════════════════════════════════
    #  MAIN
    # ══════════════════════════════════════════════════════════════════

    def main(self):
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=BG_DEEP,
                                        scrollbar_button_color=BORDER,
                                        scrollbar_button_hover_color=ACCENT)
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        row_idx = 0
        self.entries  = {}
        self.optmenus = {}
        self.switches = {}

        # ── Section 01 : Paramètres ───────────────────────────────────
        row_idx = self.section(scroll, row_idx, "01", "Paramètres")

        numeric_fields = [
            ("Nombre de maisons",      "Nombre de maisons",      "ex : 10"),
            ("Nombre de ramifications","Nombre de ramifications", "ex : 5"),
            ("Dénivelé",               "Dénivelé",               "en %"),
        ]

        f1 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f1.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f1.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        for i, (key, label, placeholder) in enumerate(numeric_fields):
            self.entries[key] = self.field(f1, i // 2, i % 2, label, placeholder)

        # ── Section 02 : Zone ─────────────────────────────────────────
        row_idx = self.section(scroll, row_idx, "02", "Zone")

        f2 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f2.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f2.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        self.optmenus["Zone"]    = self._optmenu(f2, 0, 0, "Type de zone", ["Rurale", "Urbaine", "Mix"])
        self.entries["Surface"]  = self.field(   f2, 0, 1, "Surface", "en km²")

        # ── Section 03 : Conduites ────────────────────────────────────
        row_idx = self.section(scroll, row_idx, "03", "Conduites")

        f3 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f3.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f3.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        self.optmenus["Formule pertes"] = self._optmenu(
            f3, 0, 0, "Formule pertes de charge", ["Darcy-Weisbach", "Hazen-Williams", "Chezy-Manning"])
        self.entries["Rugosité"]        = self.field(f3, 0, 1, "Rugosité", "D-W: 0.02 | H-W: 130")
        self.entries["Diamètre min"]    = self.field(f3, 1, 0, "Diamètre min (mm)", "ex : 50")
        self.entries["Diamètre max"]    = self.field(f3, 1, 1, "Diamètre max (mm)", "ex : 300")

        # ── Section 04 : Réservoir ────────────────────────────────────
        row_idx = self.section(scroll, row_idx, "04", "Réservoir")

        f4 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f4.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f4.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        self.switches["Charge auto"]   = self._switch(
            f4, 0, 0, "Charge calculée automatiquement",
            command=self.toggle_charge)
        self.entries["Charge"]         = self.field(f4, 0, 1, "Charge (m)", "ex : 750")

        # ── Section 05 : Simulation ───────────────────────────────────
        row_idx = self.section(scroll, row_idx, "05", "Simulation")

        f5 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f5.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f5.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        self.optmenus["Mode simulation"] = self._optmenu(
            f5, 0, 0, "Mode", ["Statique (0h)", "Dynamique (24h)", "Personnalisé"])
        self.entries["Durée"]            = self.field(f5, 0, 1, "Durée personnalisée (h)", "ex : 12")

        # ── Section 06 : Capteurs & Bruit ────────────────────────────
        row_idx = self.section(scroll, row_idx, "06", "Capteurs & Bruit")

        f6 = ctk.CTkFrame(scroll, corner_radius=12,
                          fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f6.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f6.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1

        self.switches["Bruit"]          = self._switch(
            f6, 0, 0, "Activer le bruit gaussien",
            command=self.toggle_bruit)
        self.entries["Écart-type"]      = self.field(f6, 0, 1, "Écart-type bruit", "ex : 0.05")
        self.entries["% cassés"]        = self.field(f6, 1, 0, "% capteurs cassés", "ex : 10")

        # désactivé par défaut
        self.entries["Écart-type"].configure(state="disabled")

        # ── Boutons ───────────────────────────────────────────────────

        btn_frame = ctk.CTkFrame(scroll, corner_radius=0, fg_color="transparent")
        btn_frame.grid(row=row_idx, column=0, padx=20, pady=(0, 28), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="OK", height=48, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HVR, text_color="#ffffff",
            command=self.on_ok,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Aléatoire", height=48, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=BG_CARD, hover_color=BORDER, text_color=TXT_SUB,
            border_width=1, border_color=BORDER,
            command=self.on_random,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.feedback = ctk.CTkLabel(
            btn_frame, text="", font=ctk.CTkFont(size=11),
            text_color="#3dba6f", wraplength=560
        )
        self.feedback.grid(row=1, column=0, columnspan=2, pady=(8, 0))

    # ══════════════════════════════════════════════════════════════════
    #  TOGGLE
    # ══════════════════════════════════════════════════════════════════

    def toggle_charge(self):
        """Désactive le champ charge si calcul automatique activé"""
        if self.switches["Charge auto"].get():
            self.entries["Charge"].configure(state="disabled", placeholder_text="calculée automatiquement")
        else:
            self.entries["Charge"].configure(state="normal", placeholder_text="ex : 750")

    def toggle_bruit(self):
        """Active/désactive le champ écart-type selon le switch bruit"""
        if self.switches["Bruit"].get():
            self.entries["Écart-type"].configure(state="normal")
        else:
            self.entries["Écart-type"].configure(state="disabled")

    # ══════════════════════════════════════════════════════════════════
    #  COLLECTER DONNEES
    # ══════════════════════════════════════════════════════════════════

    def _collect(self):
        """Collecte toutes les valeurs du formulaire"""
        return {
            "n_maisons":    self.entries["Nombre de maisons"].get(),
            "n_rami":       self.entries["Nombre de ramifications"].get(),
            "denivele":     self.entries["Dénivelé"].get(),
            "zone":         self.optmenus["Zone"].get(),
            "surface":      self.entries["Surface"].get(),
            "formule":      self.optmenus["Formule pertes"].get(),
            "rugosite":     self.entries["Rugosité"].get(),
            "diam_min":     self.entries["Diamètre min"].get(),
            "diam_max":     self.entries["Diamètre max"].get(),
            "charge_auto":  self.switches["Charge auto"].get(),
            "charge":       self.entries["Charge"].get(),
            "mode_sim":     self.optmenus["Mode simulation"].get(),
            "duree":        self.entries["Durée"].get(),
            "bruit":        self.switches["Bruit"].get(),
            "ecart_type":   self.entries["Écart-type"].get(),
            "pct_casses":   self.entries["% cassés"].get(),
        }

    def on_ok(self):
        params = self._collect()
        self.feedback.configure(text=f"✓  Paramètres collectés")

    def on_random(self):
        import random
        rng = random.Random()

        fills = {
            "Nombre de maisons":       str(rng.randint(50, 500)),
            "Nombre de ramifications": str(rng.randint(3, 15)),
            "Dénivelé":                str(round(rng.uniform(0.5, 10), 1)),
            "Surface":                 str(round(rng.uniform(0.5, 10), 1)),
            "Rugosité":                str(round(rng.uniform(0.01, 0.05), 3)),
            "Diamètre min":            str(rng.choice([50, 80, 100])),
            "Diamètre max":            str(rng.choice([200, 250, 300])),
            "Charge":                  str(rng.randint(30, 100)),
            "Durée":                   str(rng.choice([0, 6, 12, 24])),
            "% cassés":                str(rng.randint(0, 20)),
           
        }

        for key, val in fills.items():
            e = self.entries[key]
            e.configure(state="normal")
            e.delete(0, "end")
            e.insert(0, val)

        self.optmenus["Zone"].set(rng.choice(["Rurale", "Urbaine", "Mix"]))
        self.optmenus["Formule pertes"].set(rng.choice(["Darcy-Weisbach", "Hazen-Williams"]))
        self.optmenus["Mode simulation"].set(rng.choice(["Statique (0h)", "Dynamique (24h)"]))

        self.feedback.configure(text="🎲  Valeurs aléatoires générées")


app = App()
app.mainloop()