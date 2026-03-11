import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import math, random, networkx as nx

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

NODE_RES    = "#0ea5e9"   # réservoir  — bleu clair
NODE_JUNC   = "#2563eb"   # jonction   — bleu
NODE_HOUSE  = "#6366f1"   # maison     — indigo
NODE_FAULT  = "#ef4444"   # cassé      — rouge
NODE_SURGE  = "#f59e0b"   # surge      — orange
NODE_ZERO   = "#6b7280"   # pression 0 — gris
EDGE_MAIN   = "#1e3a6a"   # conduite principale
EDGE_SEC    = "#0f2a50"   # conduite secondaire (vers maison)


# ══════════════════════════════════════════════════════════════════
#  Application
# ══════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Réseau d'eau")
        self.geometry("1280x720")
        self.minsize(900, 500)
        self.configure(fg_color=BG_DEEP)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=420)
        self.grid_columnconfigure(1, weight=1)
        self.topbar()
        self.main()
        self.canvas_panel()

# ══════════════════════════════════════════════════════════════════
#  METHODES UI
# ══════════════════════════════════════════════════════════════════

    def topbar(self):
        top = ctk.CTkFrame(self, height=56, corner_radius=0, fg_color=BG_DARK)
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        top.grid_propagate(False)
        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(top, text="Réseau d'eau",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TXT_MAIN).grid(row=0, column=0)

    def section(self, parent, row, num, title):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=0, padx=20, pady=(18, 6), sticky="ew")
        f.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(f, text=num, font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ACCENT, width=28, fg_color=BG_CARD,
                     corner_radius=6).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TXT_MAIN, anchor="w").grid(row=0, column=1, sticky="w")
        return row + 1

    def field(self, parent, row, col, label, placeholder):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))
        entry = ctk.CTkEntry(f, height=38, corner_radius=8,
                             fg_color=BG_INPUT, border_color=BORDER, border_width=1,
                             text_color=TXT_MAIN, placeholder_text=placeholder,
                             placeholder_text_color=TXT_DIM, font=ctk.CTkFont(size=12))
        entry.grid(row=1, column=0, sticky="ew")
        return entry

    def _optmenu(self, parent, row, col, label, values):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))
        om = ctk.CTkOptionMenu(f, values=values, height=38, corner_radius=8,
                               fg_color=BG_INPUT, button_color=BORDER, button_hover_color=ACCENT,
                               text_color=TXT_MAIN, font=ctk.CTkFont(size=12),
                               dropdown_fg_color=BG_CARD, dropdown_hover_color=BORDER,
                               dropdown_text_color=TXT_MAIN)
        om.grid(row=1, column=0, sticky="ew")
        return om

    def _switch(self, parent, row, col, label, command=None):
        f = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        f.grid(row=row, column=col, padx=14, pady=10, sticky="ew")
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=11),
                     text_color=TXT_SUB, anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4))
        sw = ctk.CTkSwitch(f, text="", width=48,
                           button_color=ACCENT, button_hover_color=ACCENT_HVR,
                           progress_color=ACCENT, fg_color=BORDER, command=command)
        sw.grid(row=1, column=0, sticky="w")
        return sw

# ══════════════════════════════════════════════════════════════════
#  FORMULAIRE
# ══════════════════════════════════════════════════════════════════

    def main(self):
        left = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_DEEP)
        left.grid(row=1, column=0, sticky="nsew")
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(left, corner_radius=0, fg_color=BG_DEEP,
                                        scrollbar_button_color=BORDER,
                                        scrollbar_button_hover_color=ACCENT)
        scroll.grid(row=0, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)

        row_idx = 0
        self.entries  = {}
        self.optmenus = {}
        self.switches = {}

        row_idx = self.section(scroll, row_idx, "01", "Paramètres")
        f1 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f1.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f1.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        for i, (key, label, ph) in enumerate([
            ("Nombre de maisons",      "Nombre de maisons",      "ex : 10"),
            ("Nombre de ramifications","Nombre de ramifications", "ex : 5"),
            ("Dénivelé",               "Dénivelé",               "en %"),
        ]):
            self.entries[key] = self.field(f1, i // 2, i % 2, label, ph)

        row_idx = self.section(scroll, row_idx, "02", "Zone")
        f2 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f2.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f2.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        self.optmenus["Zone"]   = self._optmenu(f2, 0, 0, "Type de zone", ["Rurale", "Urbaine", "Mix"])
        self.entries["Surface"] = self.field(f2, 0, 1, "Surface", "en km²")

        row_idx = self.section(scroll, row_idx, "03", "Conduites")
        f3 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f3.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f3.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        self.optmenus["Formule pertes"] = self._optmenu(
            f3, 0, 0, "Formule pertes de charge", ["Darcy-Weisbach", "Hazen-Williams", "Chezy-Manning"])
        self.entries["Rugosité"]     = self.field(f3, 0, 1, "Rugosité", "D-W: 0.02 | H-W: 130")
        self.entries["Diamètre min"] = self.field(f3, 1, 0, "Diamètre min (mm)", "ex : 50")
        self.entries["Diamètre max"] = self.field(f3, 1, 1, "Diamètre max (mm)", "ex : 300")

        row_idx = self.section(scroll, row_idx, "04", "Réservoir")
        f4 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f4.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f4.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        self.switches["Charge auto"] = self._switch(f4, 0, 0, "Charge automatique", command=self.toggle_charge)
        self.entries["Charge"]       = self.field(f4, 0, 1, "Charge (m)", "ex : 750")

        row_idx = self.section(scroll, row_idx, "05", "Simulation")
        f5 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f5.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f5.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        self.optmenus["Mode simulation"] = self._optmenu(
            f5, 0, 0, "Mode", ["Statique (0h)", "Dynamique (24h)", "Personnalisé"])
        self.entries["Durée"] = self.field(f5, 0, 1, "Durée (h)", "ex : 12")

        row_idx = self.section(scroll, row_idx, "06", "Capteurs & Bruit")
        f6 = ctk.CTkFrame(scroll, corner_radius=12, fg_color=BG_CARD, border_width=1, border_color=BORDER)
        f6.grid(row=row_idx, column=0, padx=20, pady=(0, 12), sticky="ew")
        f6.grid_columnconfigure((0, 1), weight=1)
        row_idx += 1
        self.switches["Bruit"]     = self._switch(f6, 0, 0, "Activer le bruit gaussien", command=self.toggle_bruit)
        self.entries["Écart-type"] = self.field(f6, 0, 1, "Écart-type bruit", "ex : 0.05")
        self.entries["% cassés"]   = self.field(f6, 1, 0, "% capteurs cassés", "ex : 10")
        self.entries["Écart-type"].configure(state="disabled")

        btn_frame = ctk.CTkFrame(scroll, corner_radius=0, fg_color="transparent")
        btn_frame.grid(row=row_idx, column=0, padx=20, pady=(8, 28), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Générer réseau", height=48, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=ACCENT, hover_color=ACCENT_HVR, text_color="#ffffff",
                      command=self.on_ok).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(btn_frame, text="Aléatoire", height=48, corner_radius=12,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=BG_CARD, hover_color=BORDER, text_color=TXT_SUB,
                      border_width=1, border_color=BORDER,
                      command=self.on_random).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.feedback = ctk.CTkLabel(btn_frame, text="", font=ctk.CTkFont(size=11),
                                     text_color="#3dba6f", wraplength=360)
        self.feedback.grid(row=1, column=0, columnspan=2, pady=(8, 0))

# ══════════════════════════════════════════════════════════════════
#  CANVAS
# ══════════════════════════════════════════════════════════════════

    def canvas_panel(self):
        right = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_DARK)
        right.grid(row=1, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        bar = ctk.CTkFrame(right, height=44, corner_radius=0, fg_color=BG_DEEP)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(0, weight=1)

        self._info_label = ctk.CTkLabel(
            bar, text="Générez un réseau puis cliquez sur un nœud",
            font=ctk.CTkFont(size=11), text_color=TXT_DIM)
        self._info_label.grid(row=0, column=0, sticky="w", padx=16)

        ctk.CTkButton(bar, text="Exporter .inp", width=120, height=30, corner_radius=8,
                      font=ctk.CTkFont(size=11, weight="bold"),
                      fg_color=ACCENT, hover_color=ACCENT_HVR,
                      command=self.export_inp).grid(row=0, column=1, padx=6)

        ctk.CTkButton(bar, text="Reset fautes", width=110, height=30, corner_radius=8,
                      font=ctk.CTkFont(size=11), fg_color=BG_CARD, hover_color=BORDER,
                      border_width=1, border_color=BORDER, text_color=TXT_SUB,
                      command=self.reset_faults).grid(row=0, column=2, padx=(0, 10))

        self.cv = tk.Canvas(right, bg=BG_DEEP, bd=0,
                            highlightthickness=1, highlightbackground=BORDER)
        self.cv.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.cv.bind("<Button-1>",  self._on_click)
        self.cv.bind("<Configure>", lambda e: self._redraw())

        # légende
        leg = ctk.CTkFrame(right, height=36, corner_radius=0, fg_color=BG_DEEP)
        leg.grid(row=2, column=0, sticky="ew")
        leg.grid_propagate(False)
        for col, txt in [
            (NODE_RES,   "Réservoir"),
            (NODE_JUNC,  "Jonction"),
            (NODE_HOUSE, "Maison"),
            (NODE_FAULT, "Capteur cassé"),
            (NODE_SURGE, "Demande ×5"),
            (NODE_ZERO,  "Pression nulle"),
        ]:
            f = ctk.CTkFrame(leg, fg_color="transparent")
            f.pack(side="left", padx=10)
            tk.Canvas(f, width=10, height=10, bg=col, highlightthickness=0).pack(side="left", padx=(0, 3))
            ctk.CTkLabel(f, text=txt, font=ctk.CTkFont(size=9), text_color=TXT_SUB).pack(side="left")

        self._G          = None
        self._pos_px     = {}
        self._node_state = {}
        self._node_items = {}
        self._params     = {}

# ══════════════════════════════════════════════════════════════════
#  CONSTRUCTION DU GRAPHE
# ══════════════════════════════════════════════════════════════════

    def _build_graph(self, params):
        try:    n_maisons = int(params["n_maisons"])
        except: n_maisons = 10
        try:    n_rami = max(1, int(params["n_rami"]))
        except: n_rami = 3

        # cap visuel : au-delà de 60 maisons le canvas devient illisible
        n_maisons = min(n_maisons, 60)

        G = nx.Graph()

        # ── réservoir ──
        G.add_node("R", type="reservoir")

        # ── jonctions (réseau principal) ──
        for i in range(1, n_rami + 1):
            G.add_node(f"J{i}", type="junction")
            G.add_edge("R", f"J{i}", etype="main")

        # boucles entre jonctions
        juncs = [f"J{i}" for i in range(1, n_rami + 1)]
        for _ in range(max(0, n_rami // 3)):
            a, b = random.sample(juncs, 2)
            if not G.has_edge(a, b):
                G.add_edge(a, b, etype="main")

        # ── maisons rattachées aux jonctions ──
        maisons_par_junc = n_maisons // n_rami
        reste = n_maisons % n_rami
        m_idx = 1
        for i, junc in enumerate(juncs):
            nb = maisons_par_junc + (1 if i < reste else 0)
            for _ in range(nb):
                mid = f"M{m_idx}"
                G.add_node(mid, type="house", parent=junc)
                G.add_edge(junc, mid, etype="secondary")
                m_idx += 1

        return G

    def _layout(self, G):
        """
        Layout custom :
        - réservoir à gauche
        - jonctions en arc
        - maisons disposées en étoile autour de leur jonction
        """
        w   = max(self.cv.winfo_width(),  200)
        h   = max(self.cv.winfo_height(), 200)
        pad = 60

        juncs = [n for n, d in G.nodes(data=True) if d.get("type") == "junction"]
        pos   = {}

        # réservoir
        pos["R"] = (pad, h // 2)

        # jonctions en arc vertical centré
        n_j = len(juncs)
        for i, j in enumerate(juncs):
            jx = pad + (w - 2 * pad) * 0.35
            jy = pad + i * (h - 2 * pad) / max(n_j - 1, 1) if n_j > 1 else h // 2
            pos[j] = (jx, jy)

        # maisons en étoile autour de leur jonction
        houses_per_junc = {}
        for n, d in G.nodes(data=True):
            if d.get("type") == "house":
                p = d.get("parent")
                houses_per_junc.setdefault(p, []).append(n)

        house_r = min(70, (h - 2 * pad) / max(n_j * 2, 1))

        for junc, houses in houses_per_junc.items():
            jx, jy = pos[junc]
            n_h    = len(houses)
            for k, mid in enumerate(houses):
                angle  = math.pi / 2 + k * 2 * math.pi / n_h   # tourne autour
                # décale vers la droite pour ne pas chevaucher le réseau principal
                offset = jx + house_r * 1.6
                mx = offset + house_r * math.cos(angle)
                my = jy   + house_r * math.sin(angle)
                # clamp dans le canvas
                mx = max(pad // 2, min(w - pad // 2, mx))
                my = max(pad // 2, min(h - pad // 2, my))
                pos[mid] = (mx, my)

        return pos

# ══════════════════════════════════════════════════════════════════
#  DESSIN
# ══════════════════════════════════════════════════════════════════

    def _redraw(self):
        if self._G is None:
            self._draw_empty(); return
        self.cv.delete("all")
        self._pos_px     = self._layout(self._G)
        self._node_items = {}

        # arêtes secondaires (maisons) — en premier, sous les nœuds
        for u, v, d in self._G.edges(data=True):
            x1, y1 = self._pos_px[u]
            x2, y2 = self._pos_px[v]
            if d.get("etype") == "secondary":
                self.cv.create_line(x1, y1, x2, y2,
                                    fill=EDGE_SEC, width=1, dash=(4, 3))
            else:
                self.cv.create_line(x1, y1, x2, y2,
                                    fill=EDGE_MAIN, width=3)

        # nœuds
        for node in self._G.nodes():
            self._draw_node(node)

    def _draw_node(self, node):
        if node not in self._pos_px: return
        x, y  = self._pos_px[node]
        ntype = self._G.nodes[node].get("type", "junction")
        state = self._node_state.get(node, "normal")

        # couleur selon état ou type
        if state != "normal":
            color = {"broken": NODE_FAULT, "surge": NODE_SURGE, "zero": NODE_ZERO}[state]
        else:
            color = {"reservoir": NODE_RES, "junction": NODE_JUNC, "house": NODE_HOUSE}.get(ntype, NODE_JUNC)

        # taille selon type
        r = {"reservoir": 18, "junction": 12, "house": 7}.get(ntype, 10)

        self.cv.delete(f"node_{node}")
        self.cv.delete(f"label_{node}")

        if ntype == "reservoir":
            self.cv.create_rectangle(x-r, y-r, x+r, y+r,
                                     fill=color, outline=TXT_MAIN, width=2,
                                     tags=(f"node_{node}", "node"))
        elif ntype == "house":
            # petit carré pour les maisons
            self.cv.create_rectangle(x-r, y-r, x+r, y+r,
                                     fill=color, outline=TXT_DIM, width=1,
                                     tags=(f"node_{node}", "node"))
        else:
            self.cv.create_oval(x-r, y-r, x+r, y+r,
                                fill=color, outline=TXT_MAIN, width=2,
                                tags=(f"node_{node}", "node"))

        # label seulement pour réservoir et jonctions (trop chargé pour les maisons)
        if ntype != "house":
            self.cv.create_text(x, y + r + 10, text=node,
                                fill=TXT_SUB, font=("Courier", 8),
                                tags=f"label_{node}")
        else:
            # numéro discret sur la maison
            self.cv.create_text(x, y, text=node.replace("M", ""),
                                fill=TXT_MAIN, font=("Courier", 6),
                                tags=f"label_{node}")

    def _draw_empty(self):
        self.cv.delete("all")
        w = max(self.cv.winfo_width(), 200)
        h = max(self.cv.winfo_height(), 200)
        self.cv.create_text(w // 2, h // 2,
                            text="Générez un réseau\npour l'afficher ici",
                            fill=TXT_DIM, font=("Courier", 13), justify="center")

# ══════════════════════════════════════════════════════════════════
#  CLIC → INJECTION DE FAUTE
# ══════════════════════════════════════════════════════════════════

    def _on_click(self, event):
        if not self._pos_px: return
        closest, min_dist = None, float("inf")
        for node, (nx_, ny_) in self._pos_px.items():
            d = math.hypot(event.x - nx_, event.y - ny_)
            if d < min_dist:
                min_dist, closest = d, node

        # seuil adapté : maisons plus petites → seuil plus tolérant
        thresh = 20 if self._G.nodes[closest].get("type") == "house" else 28
        if min_dist > thresh: return
        self._show_fault_popup(closest)

    def _show_fault_popup(self, node):
        ntype = self._G.nodes[node].get("type", "junction")
        popup = ctk.CTkToplevel(self)
        popup.title(f"{'Maison' if ntype == 'house' else 'Nœud'}  {node}")
        popup.geometry("290x280")
        popup.resizable(False, False)
        popup.configure(fg_color=BG_CARD)
        popup.grab_set()

        ctk.CTkLabel(popup,
                     text=f"{'🏠 Maison' if ntype == 'house' else '● Jonction'}  {node}",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TXT_MAIN).pack(pady=(18, 4))

        if ntype == "house":
            parent = self._G.nodes[node].get("parent", "?")
            ctk.CTkLabel(popup, text=f"Rattachée à la jonction {parent}",
                         font=ctk.CTkFont(size=10), text_color=TXT_DIM).pack(pady=(0, 4))

        ctk.CTkLabel(popup, text=f"État actuel : {self._node_state.get(node, 'normal')}",
                     font=ctk.CTkFont(size=10), text_color=TXT_SUB).pack(pady=(0, 10))

        def apply(new_state):
            self._node_state[node] = new_state
            self._draw_node(node)
            color = NODE_FAULT if new_state != "normal" else "#3dba6f"
            self._info_label.configure(
                text=f"Faute « {new_state} » → {node}", text_color=color)
            popup.destroy()

        for label, state_key, border in [
            ("✓  Normal",          "normal", ACCENT),
            ("💥  Capteur cassé",  "broken", NODE_FAULT),
            ("📈  Demande × 5",    "surge",  NODE_SURGE),
            ("📉  Pression nulle", "zero",   NODE_ZERO),
        ]:
            ctk.CTkButton(popup, text=label, height=36, corner_radius=8,
                          font=ctk.CTkFont(size=12), fg_color=BG_INPUT,
                          hover_color=BORDER, text_color=TXT_MAIN,
                          border_width=1, border_color=border,
                          command=lambda s=state_key: apply(s)).pack(fill="x", padx=20, pady=3)

# ══════════════════════════════════════════════════════════════════
#  CALLBACKS FORMULAIRE
# ══════════════════════════════════════════════════════════════════

    def toggle_charge(self):
        if self.switches["Charge auto"].get():
            self.entries["Charge"].configure(state="disabled", placeholder_text="calculée automatiquement")
        else:
            self.entries["Charge"].configure(state="normal", placeholder_text="ex : 750")

    def toggle_bruit(self):
        self.entries["Écart-type"].configure(
            state="normal" if self.switches["Bruit"].get() else "disabled")

    def _collect(self):
        return {
            "n_maisons":   self.entries["Nombre de maisons"].get(),
            "n_rami":      self.entries["Nombre de ramifications"].get(),
            "denivele":    self.entries["Dénivelé"].get(),
            "zone":        self.optmenus["Zone"].get(),
            "surface":     self.entries["Surface"].get(),
            "formule":     self.optmenus["Formule pertes"].get(),
            "rugosite":    self.entries["Rugosité"].get(),
            "diam_min":    self.entries["Diamètre min"].get(),
            "diam_max":    self.entries["Diamètre max"].get(),
            "charge_auto": self.switches["Charge auto"].get(),
            "charge":      self.entries["Charge"].get(),
            "mode_sim":    self.optmenus["Mode simulation"].get(),
            "duree":       self.entries["Durée"].get(),
            "bruit":       self.switches["Bruit"].get(),
            "ecart_type":  self.entries["Écart-type"].get(),
            "pct_casses":  self.entries["% cassés"].get(),
        }

    def on_ok(self):
        params = self._collect()
        try:    int(params["n_rami"])
        except:
            self.feedback.configure(text="⚠  Nombre de ramifications invalide", text_color=NODE_FAULT)
            return
        self._params     = params
        self._G          = self._build_graph(params)
        self._node_state = {n: "normal" for n in self._G.nodes()}
        self._redraw()

        n_houses = sum(1 for _, d in self._G.nodes(data=True) if d.get("type") == "house")
        self.feedback.configure(
            text=f"✓  {self._G.number_of_nodes()} nœuds "
                 f"({n_houses} maisons · {self._G.number_of_edges()} conduites)",
            text_color="#3dba6f")
        self._info_label.configure(
            text="Cliquez sur une maison ou une jonction pour injecter une faute",
            text_color=TXT_DIM)

    def on_random(self):
        rng = random.Random()
        for key, val in {
            "Nombre de maisons":       str(rng.randint(4, 30)),
            "Nombre de ramifications": str(rng.randint(2, 8)),
            "Dénivelé":                str(round(rng.uniform(0.5, 10), 1)),
            "Surface":                 str(round(rng.uniform(0.5, 10), 1)),
            "Rugosité":                str(round(rng.uniform(0.01, 0.05), 3)),
            "Diamètre min":            str(rng.choice([50, 80, 100])),
            "Diamètre max":            str(rng.choice([200, 250, 300])),
            "Charge":                  str(rng.randint(30, 100)),
            "Durée":                   str(rng.choice([0, 6, 12, 24])),
            "% cassés":                str(rng.randint(0, 20)),
        }.items():
            e = self.entries[key]
            e.configure(state="normal")
            e.delete(0, "end")
            e.insert(0, val)
        self.optmenus["Zone"].set(rng.choice(["Rurale", "Urbaine", "Mix"]))
        self.optmenus["Formule pertes"].set(rng.choice(["Darcy-Weisbach", "Hazen-Williams"]))
        self.optmenus["Mode simulation"].set(rng.choice(["Statique (0h)", "Dynamique (24h)"]))
        self.feedback.configure(text="🎲  Valeurs aléatoires générées", text_color="#3dba6f")
        self.on_ok()

    def reset_faults(self):
        if not self._G: return
        self._node_state = {n: "normal" for n in self._G.nodes()}
        self._redraw()
        self._info_label.configure(text="Fautes réinitialisées", text_color=TXT_DIM)

# ══════════════════════════════════════════════════════════════════
#  EXPORT .INP
# ══════════════════════════════════════════════════════════════════

    def export_inp(self):
        if not self._G:
            self.feedback.configure(text="⚠  Générez d'abord un réseau", text_color=NODE_FAULT)
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".inp",
            filetypes=[("EPANET Input File", "*.inp"), ("Tous", "*.*")])
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._build_inp()))
        self.feedback.configure(text=f"✓  Exporté : {path.split('/')[-1]}", text_color="#3dba6f")

    def _build_inp(self):
        p = self._params
        lines = []
        w = lines.append

        conso = {"Rurale": 0.15, "Urbaine": 0.30, "Mix": 0.22}.get(p.get("zone", "Mix"), 0.22)
        try:    denivele = float(p.get("denivele", 0))
        except: denivele = 0.0
        try:    rug = float(p.get("rugosite", 0.02))
        except: rug = 0.02
        try:    surface = float(p.get("surface", 2.0))
        except: surface = 2.0

        # demande individuelle par maison en L/s
        demande_maison = conso * 1000 / 86400

        fautes = [n for n, s in self._node_state.items() if s != "normal"]

        w("[TITLE]")
        w(f"; Zone={p.get('zone')} | Maisons={p.get('n_maisons')} | Ramifications={p.get('n_rami')}")
        w(f"; Fautes actives : {fautes if fautes else 'aucune'}")
        w("")

        # jonctions + maisons dans [JUNCTIONS]
        w("[JUNCTIONS]")
        w(";ID              \tElev        \tDemand      \tPattern")

        all_juncs  = [(n, d) for n, d in self._G.nodes(data=True) if d.get("type") == "junction"]
        all_houses = [(n, d) for n, d in self._G.nodes(data=True) if d.get("type") == "house"]

        for i, (node, _) in enumerate(all_juncs):
            state  = self._node_state.get(node, "normal")
            elev   = round(i * denivele / 100 * 10, 2)
            demand = 0.0   # jonctions = pas de demande directe, les maisons portent la demande
            w(f" {node:<16}\t{elev:<12}\t{demand:<12}\t                \t;  [{state}]")

        for i, (node, _) in enumerate(all_houses):
            state  = self._node_state.get(node, "normal")
            elev   = round(i * denivele / 100 * 2, 2)
            demand = (0 if state == "zero"
                      else demande_maison * 5 if state == "surge"
                      else round(demande_maison, 5))
            w(f" {node:<16}\t{elev:<12}\t{demand:<12}\t                \t;  [{state}]")
        w("")

        w("[RESERVOIRS]")
        w(";ID              \tHead        \tPattern")
        if not self.switches["Charge auto"].get():
            try:    charge = float(p.get("charge", 70))
            except: charge = 70.0
        else:
            charge = round(denivele * 10 + 50, 1)
        w(f" R               \t{charge:<12}\t                \t;")
        w("")

        w("[TANKS]"); w(";ID  \tElev  \tInitLevel  \tMinLevel  \tMaxLevel  \tDiameter  \tMinVol  \tVolCurve"); w("")

        w("[PIPES]")
        w(";ID              \tNode1           \tNode2           \tLength      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        len_main = round(math.sqrt(surface * 1e6) / max(len(all_juncs), 1), 1)
        len_sec  = round(len_main * 0.1, 1)   # conduites secondaires plus courtes
        try:    diam_max = int(p.get("diam_max", 200))
        except: diam_max = 200
        try:    diam_min = int(p.get("diam_min", 50))
        except: diam_min = 50

        for k, (u, v, ed) in enumerate(self._G.edges(data=True)):
            etype  = ed.get("etype", "main")
            length = len_sec if etype == "secondary" else len_main
            diam   = diam_min if etype == "secondary" else diam_max
            w(f" P{k+1:<15}\t{u:<16}\t{v:<16}\t{length:<12}\t{diam:<12}\t{rug:<12}\t0           \tOpen  \t;")
        w("")

        w("[PUMPS]"); w(";ID  \tNode1  \tNode2  \tParameters"); w("")
        w("[VALVES]"); w(";ID  \tNode1  \tNode2  \tDiameter  \tType  \tSetting  \tMinorLoss"); w("")
        w("[TAGS]"); w("[DEMANDS]"); w("[STATUS]")

        w("[QUALITY]")
        w(";Node            \tInitQual")
        for node, state in self._node_state.items():
            if state == "broken":
                ntype = self._G.nodes[node].get("type", "?")
                w(f"; [CAPTEUR CASSÉ] {node}  (type: {ntype})")
        w("")

        dur_map = {"Statique (0h)": "0:00", "Dynamique (24h)": "24:00"}
        duree = dur_map.get(p.get("mode_sim"), f"{p.get('duree','0')}:00")
        hl    = {"Darcy-Weisbach": "D-W", "Hazen-Williams": "H-W",
                 "Chezy-Manning": "C-M"}.get(p.get("formule", "Darcy-Weisbach"), "D-W")

        w("[PATTERNS]"); w("[CURVES]"); w("[CONTROLS]"); w("[RULES]")
        w("[ENERGY]"); w(" Global Efficiency  \t75"); w(" Global Price  \t0"); w(" Demand Charge  \t0")
        w("[EMITTERS]"); w("[SOURCES]")
        w("[REACTIONS]"); w(" Order Bulk \t1"); w(" Order Tank \t1"); w(" Order Wall \t1")
        w(" Global Bulk \t0"); w(" Global Wall \t0")
        w(" Limiting Potential \t0"); w(" Roughness Correlation \t0")
        w("[MIXING]")
        w("[TIMES]")
        w(f" Duration           \t{duree} ")
        w(" Hydraulic Timestep \t1:00 "); w(" Quality Timestep   \t0:05 ")
        w(" Pattern Timestep   \t1:00 "); w(" Report Timestep    \t1:00 ")
        w(" Start ClockTime    \t12 am"); w(" Statistic          \tNONE")
        w("[REPORT]"); w(" Status \tNo"); w(" Summary \tNo"); w(" Page \t0")
        w("[OPTIONS]")
        w(" Units              \tLPS"); w(f" Headloss           \t{hl}")
        w(" Specific Gravity   \t1"); w(" Viscosity          \t1")
        w(" Trials             \t40"); w(" Accuracy           \t0.001")
        w(" Unbalanced         \tContinue 10"); w(" Demand Multiplier  \t1.0")
        w(" Quality            \tNone mg/L"); w(" Tolerance          \t0.01")

        w("[COORDINATES]"); w(";Node  \tX-Coord  \tY-Coord")
        cw = max(self.cv.winfo_width(), 200)
        ch = max(self.cv.winfo_height(), 200)
        for node, (px, py) in self._pos_px.items():
            w(f" {node:<16}\t{px/cw*10000:<16.2f}\t{(ch-py)/ch*10000:<16.2f}")

        w("[VERTICES]"); w("[LABELS]")
        w("[BACKDROP]")
        w(" DIMENSIONS \t0.00 \t0.00 \t10000.00 \t10000.00")
        w(" UNITS \tNone"); w(" FILE \t"); w(" OFFSET \t0.00 \t0.00")
        w("[END]")
        return lines


app = App()
app.mainloop()