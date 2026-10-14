# Cascade Goods data generation

Reference code for regenerating the Cascade Goods companion dataset. This directory contains the generator and `known_plants.csv`, an exercise answer key describing the deliberately planted issues. The generator also reveals how those issues are introduced. Keep this folder out of an analysis agent's blind-exercise workspace.

## Regeneration

The generator requires Python, NumPy, and pandas. From the repository root:

```sh
python data_generation/generate_cascade_goods.py
```

Regardless of the shell's working directory, all six generated CSV files are written under `generated/` beside the script. This directory is ignored by Git. Running the generator does not update the published [CG data](../cascade_goods/data/) or the committed answer key.

Review the generated tables, dictionary, and catalog before deliberately replacing committed artifacts. The generated dictionary contains field descriptions without planted-defect disclosures. Keep the catalog here rather than copying it into CG's analysis data folder.

Package versions are not pinned, so a seed alone should not be treated as a cross-environment byte-for-byte reproducibility guarantee.
