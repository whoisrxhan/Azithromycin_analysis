from flask import Flask, jsonify, render_template
from rdkit import Chem
from rdkit.Chem import Draw
import os

app = Flask(__name__)

# Canonical isomeric SMILES for Azithromycin
AZITHROMYCIN_SMILES = "CC[C@H]1[C@@]([C@@H]([C@H](N(C)C)[C@@H]([C@@H](C(=O)[C@H](C[C@@]([C@@H]([C@H]([C@@H]([C@H](C(=O)O1)C)O[C@H]2C[C@@]([C@H]([C@@H](O2)C)O)(C)OC)C)O[C@H]3[C@@H]([C@H](C[C@H](O3)C)N(C)C)O)(C)O)C)C)O)(C)O)C"

# Ensure the static directory exists and generate the molecule image
os.makedirs("static", exist_ok=True)
mol_image_path = os.path.join("static", "molecule.png")
if not os.path.exists(mol_image_path):
    mol = Chem.MolFromSmiles(AZITHROMYCIN_SMILES)
    if mol is not None:
        Draw.MolToFile(mol, mol_image_path, size=(500, 350))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    try:
        mol = Chem.MolFromSmiles(AZITHROMYCIN_SMILES)
        if mol is None:
            raise ValueError("Failed to parse the SMILES string.")

        # Assign stereochemistry to identify chiral centers from the 3D/isomeric structure
        try:
            Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
        except Exception:
            pass # RDKit usually assigns automatically during MolFromSmiles

        # Find all chiral centers
        chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

        centers_data = []
        for index, config in chiral_centers:
            # RDKit will have assigned R/S based on the isomeric SMILES
            atom = mol.GetAtomWithIdx(index)
            element = atom.GetSymbol()
            
            # Formatting '?' configurations nicely
            display_config = config if config != '?' else 'Unassigned'
            
            centers_data.append({
                "atom_index": index,
                "element": element,
                "configuration": display_config
            })

        return jsonify({
            "molecule": "Azithromycin",
            "total_chiral_centers": len(centers_data),
            "centers": centers_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True, port=5000)