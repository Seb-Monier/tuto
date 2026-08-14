#!/usr/bin/env python3
"""
Génère, pour une liste de matériaux :
  - un graphique radar (SVG) "profil de résistance" par matériau
  - un comparatif (SVG) façon "faible / moyenne / forte", tous matériaux confondus

Les critères et les matériaux sont définis dans la section CONFIGURATION
ci-dessous : c'est la seule chose à modifier.

Exécution :
    python3 generation_graph_mat.py

Les SVG sont créés dans le même dossier que le script :
    - un radar par matériau, nommé d'après MATERIAL_NAME, ex: pla_radar.svg
    - un seul comparatif : comparatif_matieres.svg
"""

import math
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# CRITÈRES COMMUNS
# Ces labels sont partagés par tous les matériaux, dans cet ordre.
# Modifie cette liste une seule fois si tu veux changer/ajouter des critères.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# CONFIGURATION DES MATÉRIAUX
# Modifie uniquement cette section pour générer plusieurs matériaux.
#
# Chaque matériau doit définir :
# - name   : nom du matériau (ex: "PLA")
# - values : liste de valeurs (1-5), une par critère, dans le même ordre
#            que CRITERIA_LABELS ci-dessus
# - color  : couleur du radar (facultatif)
# - show_title : afficher le titre sur le SVG (facultatif, défaut True)
#
# Exemple :
# MATERIALS = [
#     {"name": "PLA", "values": [4, 4, 3, 2, 3, 4, 2], "color": "#0d7d8f"},
# ]
# ---------------------------------------------------------------------------

CRITERIA_LABELS = [
    "Facilité d'impression",
    "Qualité visuelle",
    "Résistance à la traction",
    "Élongation à la rupture",
    "Résistance aux chocs",
    "Adhérence inter-couches",
    "Résistance à la chaleur",
]

MATERIALS = [
    {"name": "PLA", "values": [5, 4, 4, 1, 1, 4, 1], "color": "#49096e", "temp" : 55},
    {"name": "PET", "values": [4, 3, 3, 1, 3, 3, 3], "color": "#b8aa33", "temp" : 80},
    {"name": "TPU", "values": [1, 2, 2, 5, 5, 3, 3], "color": "#457e34", "temp" : 80},
    {"name": "ABS", "values": [2, 3, 2, 1, 3, 2, 4], "color": "#a06712", "temp" : 85},
    {"name": "PA",  "values": [3, 3, 2, 3, 4, 1, 3], "color": "#2c63ac", "temp" : 70},
    {"name": "PC",  "values": [2, 3, 5, 1, 3, 3, 5], "color": "#5f2f07", "temp" : 110},
    {"name": "ASA", "values": [1, 4, 5, 3, 3, 3, 4], "color": "#3a3a3b", "temp" : 85},

]


def _wrap(label, width=15):
    """Découpe un label trop long sur 2 lignes maximum."""
    lines = textwrap.wrap(label, width=width, break_long_words=False)
    if not lines:
        return [label]
    if len(lines) > 2:
        lines = [" ".join(lines[:-1]), lines[-1]]
    return lines


def _esc(text):
    """Échappe les caractères spéciaux XML (&, <, >) pour un SVG valide.
    Indispensable si un texte contient par exemple '<60' ou 'A&B'."""
    text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_radar(
    material_name,
    criteria,
    output_path,
    show_title= True,
    color="#0d7d8f",
    text_color="#0f3d4a",
    grid_color="#cbd5e1",
    temp=None,
    temp_criterion="Résistance à la chaleur",
):
    """
    material_name : nom affiché en titre (ex: "PLA")
    criteria      : liste de tuples (label, valeur 1-5)
    output_path   : chemin du fichier .svg à écrire
    show_title    : True pour afficher le nom du matériau en haut, False pour le masquer
    temp          : valeur de température max à afficher sous l'axe temp_criterion (facultatif)
    temp_criterion: label du critère sous lequel afficher "temp°" (doit correspondre
                    exactement à un des labels de CRITERIA_LABELS)
    """
    n = len(criteria)
    if n < 3:
        raise ValueError("Il faut au moins 3 critères pour un radar.")

    # --- Géométrie -----------------------------------------------------
    top_offset = 0 if show_title else 0   # place réservée au titre
    cx, cy = 320, 250 + top_offset          # centre du radar
    max_r = 170                             # rayon du niveau 5
    label_gap = 70                   # distance entre le bord du radar et le texte
    line_height = 20

    angles = [-90 + i * (360 / n) for i in range(n)]

    def pt(r, angle_deg):
        a = math.radians(angle_deg)
        return cx + r * math.cos(a), cy + r * math.sin(a)

    # grille (pentagones niveaux 1 à 5) + axes
    grid_polys = []
    for lvl in range(1, 6):
        r = lvl / 5 * max_r
        grid_polys.append([pt(r, a) for a in angles])
    axis_endpoints = [pt(max_r, a) for a in angles]

    # polygone des valeurs
    data_pts = [pt(v / 5 * max_r, a) for (_, v), a in zip(criteria, angles)]

    def poly_str(pts):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    svg = []

    # --- Canvas : on calcule une largeur/hauteur assez grande pour que
    # les labels (jusqu'à 2 lignes) ne sortent jamais du cadre -----------
    canvas_w = cx + max_r + label_gap + 100   # marge droite pour les longs labels
    canvas_h = cy + max_r + label_gap + 50    # marge basse pour la légende
    canvas_left_margin = 10
    view_x0 = -canvas_left_margin

    svg.append(
        f'<svg viewBox="{view_x0} 0 {canvas_w - view_x0} {canvas_h}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif">'
    )

#Fond blanc
    svg.append(
    f'<rect x="{view_x0}" y="0" width="{canvas_w - view_x0}" '
    f'height="{canvas_h}" fill="white"/>'
)

    # titre (optionnel)
    if show_title:
       svg.append(
            f'<text x="60" y="50" font-size="35" font-weight="800" '
            f'fill= "{color}" text-anchor="middle">{_esc(material_name)}</text>'
      )

    # grille
    for pts in grid_polys:
        svg.append(
            f'<polygon points="{poly_str(pts)}" fill="none" '
            f'stroke="{grid_color}" stroke-width="1"/>'
        )
    for x, y in axis_endpoints:
        svg.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="{grid_color}" stroke-width="1"/>'
        )

    # polygone de données
    svg.append(
        f'<polygon points="{poly_str(data_pts)}" fill="{color}" '
        f'fill-opacity="0.22" stroke="{color}" stroke-width="2.5" '
        f'stroke-linejoin="round"/>'
    )

    # points + valeur
    for (label, v), (x, y) in zip(criteria, data_pts):
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{color}"/>')
        svg.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="15" fill="white" '
            f'text-anchor="middle" font-weight="bold">{_esc(v)}</text>'
        )

    # labels des axes, avec retour à la ligne et ancrage adapté à la
    # position (haut / bas / gauche / droite) pour ne jamais sortir du cadre
    for (label, v), a in zip(criteria, angles):
        x, y = pt(max_r + label_gap, a)
        cos_a = math.cos(math.radians(a))
        sin_a = math.sin(math.radians(a))

        anchor = "middle"


        lines = _wrap(label, width=15)

        # si ce critère est celui de la température, on ajoute une ligne
        # supplémentaire "60°" sous le label habituel
        if temp is not None and label == temp_criterion:
            lines = lines + [f"<{temp}°C"]

        # décalage vertical : si le point est franchement en haut ou en bas,
        # on centre le bloc de texte autour du point ; sinon on part du point.
        if sin_a < -0.6:
            start_y = y - (len(lines) - 1) * line_height +45
        elif sin_a > 0.6:
            start_y = y + line_height -50
        else:
            start_y = y - (len(lines) - 1) * line_height / 2 + 4 

        for i, line in enumerate(lines):
            svg.append(
                f'<text x="{x:.1f}" y="{start_y + i * line_height:.1f}" '
                f'font-size="15" fill="{text_color}" text-anchor="{anchor}" '
                f'font-weight="600">{_esc(line)}</text>'
            )

    # légende : deux blocs côte à côte, chacun avec une pastille numérotée
    # et un texte sur 2 lignes, centrés horizontalement sous le radar
    # (même agencement que sur la fiche d'origine).
    legend_center_y = canvas_h - 30
    legend_items = [
        ("1", "Peu résistant", "Difficile d'utilisation"),
        ("5", "Très résistant", "Simple d'utilisation"),
    ]

    # largeur estimée de chaque bloc (pastille + texte) pour les centrer
    block_gap = 60           # espace entre les deux blocs
    block_width = 150       # largeur réservée à chaque bloc (pastille + texte)
    total_width = block_width * 2 + block_gap
    start_x = cx - total_width / 2

    for i, (num, line1, line2) in enumerate(legend_items):
        block_x = start_x + i * (block_width + block_gap)
        circle_x = block_x + 11
        text_x = block_x + 30

        svg.append(f'<circle cx="{circle_x:.1f}" cy="{legend_center_y:.1f}" r="11" fill="{color}"/>')
        svg.append(
            f'<text x="{circle_x:.1f}" y="{legend_center_y + 4:.1f}" font-size="11" '
            f'fill="white" text-anchor="middle" font-weight="bold">{_esc(num)}</text>'
        )
        svg.append(
            f'<text x="{text_x:.1f}" y="{legend_center_y - 3:.1f}" font-size="13" '
            f'fill="{text_color}" font-weight="600">{_esc(line1)}</text>'
        )
        svg.append(
            f'<text x="{text_x:.1f}" y="{legend_center_y + 14:.1f}" font-size="13" '
            f'fill="{text_color}" font-weight="600">{_esc(line2)}</text>'
        )

    svg.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    return output_path


def generate_dotplot(
    criteria_labels,
    materials,
    output_path,
    title=None,
    axis_labels=("Faible", "Moyenne", "Forte"),
    text_color="#333333",
    axis_color="#9aa0a6",
    label_color="#555555",
):
    """
    Comparatif façon "3D Hubs" : pour chaque critère, un axe horizontal
    faible -> moyenne -> forte, avec un point coloré par matériau positionné
    selon sa valeur (1 à 5).

    criteria_labels : liste des noms de critères (lignes du graphique)
    materials       : liste de dicts {"name", "values" (1-5, un par critère), "color"}
    output_path     : chemin du fichier .svg à écrire
    title           : titre optionnel affiché en haut
    axis_labels     : libellés des 3 graduations (faible / moyenne / forte)
    """
    for m in materials:
        if len(m["values"]) != len(criteria_labels):
            raise ValueError(
                f"{m['name']} : {len(m['values'])} valeurs fournies, "
                f"{len(criteria_labels)} attendues."
            )

    # --- Géométrie -------------------------------------------------------
    label_col_width = 250         # largeur réservée aux noms de critères
    axis_x0 = label_col_width + 30  # début de l'axe (sous "faible")
    axis_x1 = axis_x0 + 450         # fin de l'axe (sous "forte")
    arrow_extra = 60                # dépassement de la flèche après "forte"

    header_h = 60 if not title else 60 + 40
    row_h = 105
    dot_r = 16
    stack_dy = 22                   # écart vertical entre points empilés (même valeur)

    n_rows = len(criteria_labels)
    canvas_w = axis_x1 + arrow_extra + 40
    canvas_h = header_h + n_rows * row_h + 90  # + place pour la légende

    def value_to_x(v):
        # v va de 1 (faible) à 5 (forte), interpolation linéaire sur l'axe
        return axis_x0 + (v - 1) / 4 * (axis_x1 - axis_x0)

    svg = []
    svg.append(
        f'<svg viewBox="0 0 {canvas_w} {canvas_h}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="Arial, Helvetica, sans-serif">'
    )
    svg.append(f'<rect x="0" y="0" width="{canvas_w}" height="{canvas_h}" fill="white"/>')

    # titre optionnel
    y_cursor = 40
    if title:
        svg.append(
            f'<text x="330" y="{y_cursor}" font-size="26" '
            f'font-weight="800" fill="#0f274a" text-anchor="middle">{title}</text>'
        )
        y_cursor += 40

    # en-tête des graduations (faible / moyenne / forte)
    header_y = y_cursor + 50 #placement y du debut du graphe
    tick_xs = [value_to_x(1), value_to_x(3), value_to_x(5)]
    for label, tx in zip(axis_labels, tick_xs):
        svg.append(
            f'<text x="{tx:.1f}" y="{header_y}" font-size="20" fill="{label_color}" '
            f'text-anchor="middle">{_esc(label)}</text>'
        )

    grid_top = header_y + 15
    grid_bottom = grid_top + n_rows * row_h
    all_tick_xs = [value_to_x(v) for v in range(1, 6)]
    for tx in all_tick_xs:
        svg.append(
            f'<line x1="{tx:.1f}" y1="{grid_top}" x2="{tx:.1f}" y2="{grid_bottom}" '
            f'stroke="{axis_color}" stroke-width="1" stroke-dasharray="3,4"/>'
        )

    # lignes de critères + points
    for i, label in enumerate(criteria_labels):
        row_center_y = grid_top + i * row_h + row_h / 2

        # libellé du critère (aligné à droite, juste avant l'axe)
        svg.append(
            f'<text x="{label_col_width}" y="{row_center_y + 6:.1f}" font-size="20" '
            f'fill="{text_color}" text-anchor="end">{_esc(label)}</text>'
        )

        # ligne d'axe avec flèche
        arrow_tip_x = axis_x1 + arrow_extra
        svg.append(
            f'<line x1="{axis_x0}" y1="{row_center_y:.1f}" x2="{arrow_tip_x}" '
            f'y2="{row_center_y:.1f}" stroke="{axis_color}" stroke-width="1.5"/>'
        )
        svg.append(
            f'<polygon points="{arrow_tip_x},{row_center_y - 5:.1f} '
            f'{arrow_tip_x + 10},{row_center_y:.1f} {arrow_tip_x},{row_center_y + 5:.1f}" '
            f'fill="{axis_color}"/>'
        )

        # regrouper les matériaux par valeur pour empiler les points identiques
        by_value = {}
        for m in materials:
            v = m["values"][i]
            by_value.setdefault(v, []).append(m)

        for v, mats in by_value.items():
            x = value_to_x(v)
            k = len(mats)
            block_h = (k - 1) * stack_dy
            start_y = row_center_y - block_h / 2
            for j, m in enumerate(mats):
                y = start_y + j * stack_dy
                svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dot_r}" fill="{m["color"]}"/>')

    # légende : une pastille + nom par matériau, centrée en bas, avec retour
    # à la ligne si trop de matériaux pour tenir sur une seule rangée
    approx_char_w = 10
    dot_to_text_gap = 22
    item_gap = 34
    max_row_w = canvas_w - 40

    item_widths = [dot_r * 2 + dot_to_text_gap + len(m["name"]) * approx_char_w for m in materials]

    # découpage en rangées pour ne pas dépasser la largeur du canvas
    rows = []
    current_row, current_w = [], 0
    for m, w in zip(materials, item_widths):
        added_w = w + (item_gap if current_row else 0)
        if current_row and current_w + added_w > max_row_w:
            rows.append(current_row)
            current_row, current_w = [], 0
            added_w = w
        current_row.append((m, w))
        current_w += added_w
    if current_row:
        rows.append(current_row)

    legend_row_h = 34
    #legend_y = grid_bottom + 45
    legend_y = 40
    for row in rows:
        row_w = sum(w for _, w in row) + item_gap * (len(row) - 1)
        x_cursor = (canvas_w - row_w) / 2
        for m, w in row:
            cx = x_cursor + dot_r
            svg.append(f'<circle cx="{cx:.1f}" cy="{legend_y}" r="{dot_r - 2}" fill="{m["color"]}"/>')
            svg.append(
                f'<text x="{cx + dot_r - 2 + 10:.1f}" y="{legend_y + 6}" font-size="17" '
                f'font-weight="700" fill="{text_color}">{_esc(m["name"])}</text>'
            )
            x_cursor += w + item_gap
        legend_y += legend_row_h

    svg.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    return output_path



def main():
    # Les fichiers SVG sont créés dans le même dossier que ce script.
    script_dir = Path(__file__).resolve().parent

    # --- 1) Un radar par matériau ----------------------------------------
    for material in MATERIALS:
        material_name = material["name"]
        values = material["values"]

        if len(values) != len(CRITERIA_LABELS):
            raise ValueError(
                f"{material_name} : {len(values)} valeurs fournies, "
                f"{len(CRITERIA_LABELS)} attendues (une par critère de CRITERIA_LABELS)."
            )

        criteria = list(zip(CRITERIA_LABELS, values))
        color = material.get("color", "#0d7d8f")
        text_color = material.get("text_color", "#0f3d4a")
        grid_color = material.get("grid_color", "#cbd5e1")
        show_title = material.get("show_title", True)
        temp = material.get("temp")

        output_path = script_dir / f"{material_name.lower()}_radar.svg"

        generate_radar(
            material_name,
            criteria,
            str(output_path),
            show_title=show_title,
            color=color,
            text_color=text_color,
            grid_color=grid_color,
            temp=temp,
        )

        print(f"Généré : {output_path}")

    # --- 2) Le comparatif tous matériaux confondus ------------------------
    dotplot_path = script_dir / "comparatif_matieres.svg"
    generate_dotplot(
        CRITERIA_LABELS,
        MATERIALS,
        str(dotplot_path),
        #title="Comparatif des matières",
    )
    print(f"Généré : {dotplot_path}")


if __name__ == "__main__":
    main()
