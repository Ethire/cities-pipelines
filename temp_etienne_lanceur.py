import tsnet
from matplotlib import pyplot as plt
from file_export import *
import re
import ast

# --- Compatibility patch: tsnet temporarily assigns pipe.roughness = 0
# during initialization, but wntr >= 1.x rejects non-positive values.
# We relax the validator to allow zero, restoring tsnet's expected behavior.
import wntr.utils.check_values as _wntr_check
import wntr.network.elements as _wntr_elements

_original_check = _wntr_check._check_positive_non_zero_float

def _check_non_negative_float(value, property_name):
    # Allow zero for "Pipe roughness" (tsnet sets it transiently),
    # keep strict validation for everything else.
    if property_name == "Pipe roughness":
        value = float(value)
        if value < 0:
            raise ValueError(f"{property_name} must be greater than or equal to zero")
        return value
    return _original_check(value, property_name)

# Patch the symbol that wntr.network.elements actually imported.
_wntr_elements._check_positive_non_zero_float = _check_non_negative_float
# --- end of compatibility patch

def get_active_faults(inp_path: str) -> list[str]:
    """
    Read an EPANET .inp file and return the junctions listed after
    'Fautes actives :' in the [TITLE] section.
    Returns an empty list if the marker is not found.
    """
    pattern = re.compile(r"Fautes actives\s*:\s*(\[.*?\])")
    with open(inp_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                try:
                    value = ast.literal_eval(match.group(1))
                except (ValueError, SyntaxError):
                    return []
                # Ensure we return a clean list of strings
                return [str(x) for x in value]
    return []


if __name__ == "__main__":
    fichier_inp = "montest.inp"
    fautes = get_active_faults(fichier_inp)
    print("Fautes actives:", fautes)

    tm = tsnet.network.TransientModel(fichier_inp)

    print("Valve names:", tm.junction_name_list)

    tm.set_wavespeed(1200.)
    tm.set_time(30) # secondes
    tm = tsnet.simulation.Initializer(tm, 0.0)
    tm = tsnet.simulation.MOCSimulator(tm)

    t = tm.simulation_timestamps
    for f in fautes:
        node = tm.get_node(f)
        plt.plot(t, node.head)
        plt.title(f"Node {f}")
        plt.show()




