#!/usr/bin/env bash
set -euo pipefail

# Executa as 3 simulações (n=10 e n=100) e gera relatório.

python -m fluxo_redes.simulations --all --sizes 10 100 --density 0.25 --out results --figures figures
python -m fluxo_redes.report --results results --figures figures --out report

echo "Pronto! Veja: results/, figures/, report/"
