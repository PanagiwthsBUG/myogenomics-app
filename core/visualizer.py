import numpy as np
import plotly.graph_objects as go
import py3Dmol

def create_dna_double_helix(dna_seq: str):
    """
    Δημιουργεί μια διαδραστική 3D διπλή έλικα DNA για το επιλεγμένο τμήμα.
    (Περιορίζεται στις πρώτες 60 βάσεις για ομαλή 3D απόδοση).
    """
    seq = dna_seq[:60]
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    color_map = {"A": "#EF553B", "T": "#636EFA", "C": "#00CC96", "G": "#AB63FA"}
    
    n = len(seq)
    t = np.linspace(0, n * 0.6, n)
    
    # Συντεταγμένες 1ης αλυσίδας
    x1, y1, z1 = np.cos(t), np.sin(t), t
    # Συντεταγμένες 2ης συμπληρωματικής αλυσίδας (μετατόπιση κατά π)
    x2, y2, z2 = np.cos(t + np.pi), np.sin(t + np.pi), t

    fig = go.Figure()

    # Σχεδίαση σκελετού (Backbones)
    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z1, mode='lines', line=dict(color='gray', width=5), name='5\' -> 3\' Strand'))
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z2, mode='lines', line=dict(color='darkgray', width=5), name='3\' -> 5\' Strand'))

    # Σχεδίαση ζευγών βάσεων (Γέφυρες)
    for i, base in enumerate(seq):
        comp_base = complement.get(base, "N")
        c1 = color_map.get(base, "white")
        c2 = color_map.get(comp_base, "white")
        
        # Μισή γέφυρα από την αλυσίδα 1 στο κέντρο
        fig.add_trace(go.Scatter3d(
            x=[x1[i], 0], y=[y1[i], 0], z=[z1[i], z1[i]],
            mode='lines+markers',
            marker=dict(size=5, color=c1),
            line=dict(color=c1, width=4),
            text=f"Θέση {i+1}: {base}",
            hoverinfo="text",
            showlegend=False
        ))
        # Άλλη μισή γέφυρα από το κέντρο στην αλυσίδα 2
        fig.add_trace(go.Scatter3d(
            x=[0, x2[i]], y=[0, y2[i]], z=[z2[i], z2[i]],
            mode='lines+markers',
            marker=dict(size=5, color=c2),
            line=dict(color=c2, width=4),
            text=f"Θέση {i+1}: {comp_base}",
            hoverinfo="text",
            showlegend=False
        ))

    fig.update_layout(
        title=f"3D Διπλή Έλικα DNA (Εμφάνιση πρώτων {n} βάσεων επιλογής)",
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_title="Άξονας Έλικας"),
        margin=dict(l=0, r=0, b=0, t=40),
        height=500
    )
    return fig

def create_protein_3d_view(pdb_data: str, style: str = "cartoon"):
    """
    Δημιουργεί τον 3D viewer της πρωτεΐνης μέσω py3Dmol.
    """
    view = py3Dmol.view(width=700, height=500)
    view.addModel(pdb_data, "pdb")
    
    if style == "cartoon":
        view.setStyle({"cartoon": {"color": "spectrum"}})
    elif style == "stick":
        view.setStyle({"stick": {}})
    elif style == "sphere":
        view.setStyle({"sphere": {"scale": 0.3}})
        
    view.zoomTo()
    return view
