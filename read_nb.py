import json

nb_path = r'F:\PyTorch_GPU\AIS_trajectory_forecasting\CEE-Transformer_architecture_driven_trajectory_forecasting\CEE-Replication\Geohashed_traisformer\Notebooks\05_TRAISformer_Q1.ipynb'
out_path = r'F:\PyTorch_GPU\AIS_trajectory_forecasting\nb05_cells.txt'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open(out_path, 'w', encoding='utf-8') as out:
    for i, cell in enumerate(nb['cells']):
        ct = cell['cell_type']
        if ct in ('code', 'markdown'):
            src = ''.join(cell['source'])
            out.write("\n\n=== Cell {} [{}] ===\n".format(i, ct))
            out.write(src)

print("Done, cells written to:", out_path)
print("Total cells:", len(nb['cells']))
