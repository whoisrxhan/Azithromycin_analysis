from rdkit import Chem

def analyze_azithromycin():
    azithromycin_smiles = "CC[C@H]1OC(=O)[C@H](C)[C@@H](O[C@@H]2O[C@@H](C)[C@@H]([C@](C2)(C)OC)O)[C@H](C)[C@@H](O[C@@H]2O[C@H](C)C[C@@H]([C@H]2O)N(C)C)[C@](C[C@H](CN([C@@H]([C@H]([C@]1(C)O)O)C)C)C)(C)O"
    mol = Chem.MolFromSmiles(azithromycin_smiles)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True, flagPossibleStereoCenters=True)
    chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    print("Molecule: Azithromycin")
    print(f"Total number of chiral centers: {len(chiral_centers)}")
    print("-" * 40)
    print(f"{'Atom Index':<12} | {'Element':<10} | {'Configuration'}")
    print("-" * 40)
    for atom_idx, config in chiral_centers:
        atom = mol.GetAtomWithIdx(atom_idx)
        element = atom.GetSymbol()
        if config == "?":
            config_display = "Error: Unassigned"
        else:
            config_display = config        
        print(f"{atom_idx:<12} | {element:<10} | {config_display}")

if __name__ == "__main__":
    analyze_azithromycin()

print("Register Number: RA2511026050045")
print("Name: Manikandan Rohan R")
print("Department: CSE w/s in AIML , Section: A")