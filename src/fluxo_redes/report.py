"""Geração de relatório (Markdown + PDF) a partir de `results/summary.csv`.

Uso:
    python -m fluxo_redes.report --results results --figures figures --out report

Gera:
- report/relatorio.md
- report/relatorio.pdf
"""

from __future__ import annotations

import argparse
import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any

import numpy as np
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors

from .visualize import draw_graph


def _safe_markdown_table(df: pd.DataFrame, max_rows: int = 20, max_col_width: int = 48) -> str:
    if len(df) > max_rows:
        df = df.head(max_rows)

    def _float_precision(col: str) -> int:
        name = col.lower()
        if "runtime" in name:
            return 6
        return 2

    def _fmt(v: object, col: str) -> str:
        if pd.isna(v):
            return ""
        if isinstance(v, float):
            return f"{v:.{_float_precision(col)}f}"
        s = str(v)
        if len(s) > max_col_width:
            return s[: max_col_width - 1] + "…"
        return s

    headers = [str(c) for c in df.columns]
    rows = [[_fmt(v, col) for v, col in zip(row, headers)] for row in df.values.tolist()]

    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(w, len(cell)) for w, cell in zip(widths, row)]

    def _row(cells: List[str]) -> str:
        return "| " + " | ".join(cell.ljust(w) for cell, w in zip(cells, widths)) + " |"

    header_line = _row(headers)
    sep_line = "| " + " | ".join("-" * w for w in widths) + " |"
    body_lines = [_row(row) for row in rows]
    return "\n".join([header_line, sep_line] + body_lines)


def _effective_density(n: int, m: int) -> float:
    denom = n * (n - 1)
    return float(m) / float(denom) if denom else 0.0


def _read_distances(results_dir: str, sim_id: int, sim_name: str, n: int) -> pd.DataFrame:
    path = os.path.join(results_dir, f"sim{sim_id}_{sim_name}_n{n}_distances.csv")
    return pd.read_csv(path)


def _load_llm_results(results_dir: str) -> dict | None:
    path = os.path.join(results_dir, "llm_results.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_llm_key(key: str) -> tuple[int, str, int] | None:
    m = re.match(r"sim(\d+)_(\w+)_n(\d+)_graph\.txt", key)
    if not m:
        return None
    return int(m.group(1)), m.group(2), int(m.group(3))


def _compare_llm_vs_alg(dist_df: pd.DataFrame, llm_vals: list[float], tol: float = 1e-6) -> dict:
    alg_vals = dist_df["distance"].tolist()
    n_alg = len(alg_vals)
    n_llm = len(llm_vals)
    n = min(n_alg, n_llm)
    diffs = []
    matches = 0
    for i in range(n):
        try:
            dv = float(alg_vals[i])
            lv = float(llm_vals[i])
        except Exception:
            continue
        if not np.isfinite(dv) or not np.isfinite(lv):
            continue
        d = abs(dv - lv)
        diffs.append(d)
        if d <= tol:
            matches += 1

    mean_abs = float(np.mean(diffs)) if diffs else None
    max_abs = float(np.max(diffs)) if diffs else None
    return {
        "n_alg": n_alg,
        "n_llm": n_llm,
        "matches": matches,
        "compared": len(diffs),
        "mean_abs_diff": mean_abs,
        "max_abs_diff": max_abs,
    }


def _side_by_side_df(dist_df: pd.DataFrame, llm_vals: list[float]) -> pd.DataFrame:
    alg_vals = dist_df["distance"].tolist()
    n_alg = len(alg_vals)
    n_llm = len(llm_vals)
    n = min(n_alg, n_llm)
    rows = []
    for i in range(n):
        try:
            dv = float(alg_vals[i])
        except Exception:
            dv = np.nan
        try:
            lv = float(llm_vals[i])
        except Exception:
            lv = np.nan
        diff = abs(dv - lv) if np.isfinite(dv) and np.isfinite(lv) else np.nan
        rows.append(
            {
                "vertex": f"x{i+1}",
                "alg_distance": dv,
                "llm_distance": lv,
                "abs_diff": diff,
            }
        )
    return pd.DataFrame(rows)


def _graph_json_path(results_dir: str, sim_id: int, sim_name: str, n: int) -> str:
    return os.path.join(results_dir, f"sim{sim_id}_{sim_name}_n{n}_graph.json")


def _ensure_graph_viz(results_dir: str, figures_dir: str, sim_id: int, sim_name: str, n: int) -> str:
    if n >= 100:
        raise ValueError("Visualização do grafo desativada para n >= 100")
    graph_json = _graph_json_path(results_dir, sim_id, sim_name, n)
    out_path = os.path.join(figures_dir, f"sim{sim_id}_{sim_name}_n{n}_graph.png")
    if not os.path.exists(out_path):
        draw_graph(graph_json, out_path, layout="spring", seed=42)
    return out_path


def _path_to_commas(path: object) -> str:
    if not isinstance(path, str) or not path:
        return "" if path is None else str(path)
    return path.replace(" -> ", ",").replace("X", "x")


def _analyze_run(summary_row: pd.Series, dist_df: pd.DataFrame) -> Dict[str, Any]:
    n = int(summary_row["n"])
    m = int(summary_row["m"])
    reachable = int(summary_row["dist_reachable"])
    unreachable = n - reachable

    finite = dist_df[np.isfinite(dist_df["distance"])].copy()

    # Estatísticas de hops (quando disponível)
    hop_stats = {}
    if finite["path_hops"].notna().any():
        hops = finite["path_hops"].dropna().astype(int).values
        hop_stats = {
            "hops_min": int(hops.min()) if hops.size else None,
            "hops_max": int(hops.max()) if hops.size else None,
            "hops_mean": float(hops.mean()) if hops.size else None,
            "hops_std": float(hops.std(ddof=0)) if hops.size else None,
        }

    # Ranking de distâncias (mais perto -> mais longe)
    rank_all = finite.sort_values("distance", ascending=True)[["label", "distance", "path"]]
    top_far = rank_all.sort_values("distance", ascending=False).head(10)
    top_close = rank_all.head(10)

    # Um indicador simples de "dificuldade": razão entre dist_max e dist_mean
    dist_mean = float(summary_row.get("dist_mean")) if pd.notna(summary_row.get("dist_mean")) else np.nan
    dist_max = float(summary_row.get("dist_max")) if pd.notna(summary_row.get("dist_max")) else np.nan
    spread_ratio = float(dist_max / dist_mean) if np.isfinite(dist_mean) and dist_mean != 0 else np.nan

    return {
        "n": n,
        "m": m,
        "eff_density": _effective_density(n, m),
        "reachable": reachable,
        "unreachable": unreachable,
        "spread_ratio": spread_ratio,
        "rank_all": rank_all,
        "top_far": top_far,
        "top_close": top_close,
        **hop_stats,
    }


def generate_markdown_report(summary: pd.DataFrame, results_dir: str, figures_dir: str) -> str:
    lines: List[str] = []
    lines.append(f"# Relatório — Fluxo em Redes (Caminho Mínimo)\n")
    lines.append(f"Gerado em {datetime.utcnow().isoformat()}Z\n")

    # Visão geral
    lines.append("## Visão geral\n")
    lines.append(
        "O projeto implementa três simulações de caminho mínimo a partir da raiz X1, "
        "com diferentes hipóteses sobre ciclos e sinais dos custos, e com representações distintas de grafo.\n"
    )

    # Discussão por sim
    sim_names = {
        1: "Simulação 1 — Bellman recursivo em DAG com custos negativos (lista de antecessores)",
        2: "Simulação 2 — Dijkstra Best-First com Heap (lista de sucessores, custos não-negativos)",
        3: "Simulação 3 — Floyd-Warshall (matriz de custos, custos negativos, ciclos)",
    }

    for sim_id in sorted(summary["sim_id"].unique()):
        lines.append(f"## {sim_names[int(sim_id)]}\n")
        sim_df = summary[summary["sim_id"] == sim_id].sort_values("n")

        # Comentários técnicos do algoritmo
        if int(sim_id) == 1:
            lines.append(
                "**Ponto-chave:** como o grafo não possui circuitos, a recorrência de Bellman é bem definida e pode ser "
                "avaliada recursivamente. A memoização é essencial para evitar recomputações.\n"
            )
        elif int(sim_id) == 2:
            lines.append(
                "**Ponto-chave:** o Dijkstra depende de pesos não-negativos. A fila de prioridade (Heap) garante que sempre "
                "expandimos o nó com menor distância conhecida (Best-First).\n"
            )
        else:
            lines.append(
                "**Ponto-chave:** o Floyd-Warshall calcula distâncias entre todos os pares, permitindo pesos negativos, "
                "e a resposta pedida (X1 -> demais) é a primeira linha da matriz final.\n"
            )

        for _, row in sim_df.iterrows():
            n = int(row["n"])
            sim_name = str(row.get("sim_name", "")) or ("Bellman" if int(sim_id) == 1 else "Dijkstra" if int(sim_id) == 2 else "Floyd")
            dist_df = _read_distances(results_dir, int(sim_id), sim_name, n)
            ana = _analyze_run(row, dist_df)

            lines.append(f"### Execução: n={n}\n")
            lines.append(
                f"- Arestas (m): {ana['m']} | densidade efetiva: {ana['eff_density']:.3f} | arestas negativas: {int(row['neg_edges'])}\n"
            )
            lines.append(
                f"- Alcançáveis a partir de X1: {ana['reachable']}/{ana['n']} (inalcançáveis: {ana['unreachable']})\n"
            )
            lines.append(f"- Tempo de execução: {float(row['runtime_s']):.6f} s\n")

            # Operações internas do algoritmo
            alg_ops = {k: row[k] for k in row.index if k.startswith("alg_")}
            alg_ops = {k.replace("alg_", ""): alg_ops[k] for k in alg_ops}
            lines.append("- Contadores internos: " + ", ".join(f"{k}={alg_ops[k]}" for k in sorted(alg_ops)) + "\n")

            # Estatísticas de hops
            if "hops_mean" in ana and ana["hops_mean"] is not None:
                lines.append(
                    f"- Hops (arestas no caminho): min={ana['hops_min']} | média={ana['hops_mean']:.2f} | max={ana['hops_max']} | desvio={ana['hops_std']:.2f}\n"
                )

            # Interpretação do espalhamento
            if np.isfinite(ana["spread_ratio"]):
                lines.append(
                    f"- Indicador de espalhamento (dist_max / dist_mean): {ana['spread_ratio']:.2f}. "
                    "Valores mais altos sugerem maior heterogeneidade entre caminhos curtos e longos.\n"
                )

            # Foto do grafo
            try:
                graph_viz = _ensure_graph_viz(results_dir, figures_dir, int(sim_id), sim_name, n)
                lines.append("Figura (grafo):\n")
                lines.append(f"![]({graph_viz})\n")
            except Exception as exc:
                lines.append(f"Figura (grafo) indisponível: {exc}\n")

            if n <= 10:
                lines.append("#### Ranking de distância (mais perto → mais longe)\n")
                lines.append(_safe_markdown_table(ana["rank_all"], max_rows=n) + "\n")
            else:
                lines.append("#### Vértices mais distantes (top 10)\n")
                lines.append(_safe_markdown_table(ana["top_far"], max_rows=10) + "\n")

                lines.append("#### Vértices mais próximos (top 10)\n")
                if n == 100:
                    top_close_fmt = ana["top_close"].copy()
                    if "path" in top_close_fmt.columns:
                        top_close_fmt["path"] = top_close_fmt["path"].map(_path_to_commas)
                    lines.append(_safe_markdown_table(top_close_fmt, max_rows=10) + "\n")
                else:
                    lines.append(_safe_markdown_table(ana["top_close"], max_rows=10) + "\n")

            # Série por vértice
            series = os.path.join(figures_dir, f"sim{int(sim_id)}_{sim_name}_n{n}_series.png")
            if os.path.exists(series):
                lines.append(f"Figura (série por vértice): `{series}`\n")

            # Comentários interpretativos específicos
            if int(sim_id) == 1:
                lines.append(
                    "**Comentário:** em DAGs densos, um aumento de densidade tende a reduzir distâncias médias (mais opções de atalhos). "
                    "Custos negativos podem criar caminhos muito curtos, mas como não há ciclos, não há risco de reduzir indefinidamente.\n"
                )
            elif int(sim_id) == 2:
                lines.append(
                    "**Comentário:** a forma Best-First com Heap prioriza nós com menor distância estimada. Em grafos mais densos, "
                    "o número de relaxações cresce, mas a seleção ordenada mantém a correção.\n"
                )
            else:
                lines.append(
                    "**Comentário:** o custo O(n^3) do Floyd-Warshall domina rapidamente em n=100. Mesmo assim, ele fornece todas as distâncias "
                    "entre pares, o que é útil quando queremos responder muitas consultas de caminho mínimo após uma única execução.\n"
                )

    # Comparação cruzada
    lines.append("## Comparação entre algoritmos\n")
    comp = summary.copy()
    comp["eff_density"] = comp.apply(lambda r: _effective_density(int(r["n"]), int(r["m"])), axis=1)
    if "sim_name" in comp.columns:
        comp_small = comp[["sim_id", "sim_name", "n", "runtime_s", "eff_density", "neg_edges", "dist_mean", "dist_std"]].sort_values(["n", "sim_id"])
    else:
        comp_small = comp[["sim_id", "n", "runtime_s", "eff_density", "neg_edges", "dist_mean", "dist_std"]].sort_values(["n", "sim_id"])
    lines.append(_safe_markdown_table(comp_small) + "\n")

    lines.append(
        "### Observações\n"
        "- Em termos de complexidade assintótica, Dijkstra com Heap costuma escalar melhor para grafos esparsos a moderadamente densos, "
        "enquanto Floyd-Warshall cresce com n^3 e se torna o gargalo em tamanhos maiores.\n"
        "- A simulação 1 é estruturalmente diferente: como é um DAG, o caminho mínimo pode ser resolvido via DP/topologia. A recursão com memoização "
        "tem custo proporcional a O(n+m).\n"
        "- A presença de arestas negativas (sem ciclos negativos) pode deslocar a distribuição de distâncias para valores menores e aumentar o espalhamento.\n"
    )

    lines.append("## Resumo executivo dos resultados\n")
    show_cols = [
        "sim_id",
        "sim_name",
        "n",
        "m",
        "neg_edges",
        "runtime_s",
        "dist_reachable",
        "dist_min",
        "dist_mean",
        "dist_max",
    ]
    lines.append(_safe_markdown_table(summary[show_cols].sort_values(["sim_id", "n"])) + "\n")

    # Parte 2 (linguagem generativa)

    lines.append("### Parte 2 — Modelo utilizado e especificações\n")
    lines.append(
        "(ESCREVA AQUI)\n"
        "- Modelo utilizado: GPT\n"
        "- Versão/fornecedor: 5.2 Thinking\n"
        "- Prompt final utilizado: Dado os grafos direcionados com vértices X1..Xn: (6 arquivos .txt anexados) calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices Para cada um dos arquivos .txt anexados Devolva listas de n valores d(X1)..d(Xn), uma para cada arquivo .txt.\n"
        "- Observações de execução: A LLM pensou por 2m e 37 segundos ao total para as 6 simulações\n"
        "\n"
    )

    lines.append("### Parte 2 — Comparação LLM vs algoritmos\n")
    llm = _load_llm_results(results_dir)
    if not llm:
        lines.append("Arquivo results/llm_results.json não encontrado.\n")
    else:
        results = llm.get("results", {})
        rows = []
        for key, llm_vals in results.items():
            parsed = _parse_llm_key(key)
            if not parsed:
                continue
            sim_id, sim_name, n = parsed
            dist_df = _read_distances(results_dir, sim_id, sim_name, n)
            comp = _compare_llm_vs_alg(dist_df, llm_vals)
            rows.append(
                {
                    "sim_id": sim_id,
                    "sim_name": sim_name,
                    "n": n,
                    "n_alg": comp["n_alg"],
                    "n_llm": comp["n_llm"],
                    "matches": comp["matches"],
                    "compared": comp["compared"],
                    "mean_abs_diff": comp["mean_abs_diff"],
                    "max_abs_diff": comp["max_abs_diff"],
                }
            )

        if rows:
            df_llm = pd.DataFrame(rows).sort_values(["sim_id", "n"])
            lines.append(_safe_markdown_table(df_llm, max_rows=20) + "\n")

            # Distâncias lado a lado (algoritmo vs LLM)
            for key, llm_vals in results.items():
                parsed = _parse_llm_key(key)
                if not parsed:
                    continue
                sim_id, sim_name, n = parsed
                lines.append(f"#### Lado a lado — sim{sim_id} {sim_name} n={n}\n")
                dist_df = _read_distances(results_dir, sim_id, sim_name, n)
                side_df = _side_by_side_df(dist_df, llm_vals)
                lines.append(_safe_markdown_table(side_df, max_rows=n) + "\n")
        else:
            lines.append("Nenhum resultado LLM válido encontrado em results/llm_results.json.\n")

    return "\n".join(lines)


def _df_to_reportlab_table(df: pd.DataFrame, max_rows: int = 30, font_size: int = 8, word_wrap: bool = False) -> Table:
    if len(df) > max_rows:
        df = df.head(max_rows)

    def _float_precision(col: str) -> int:
        name = col.lower()
        if "runtime" in name:
            return 6
        return 2

    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_float_dtype(df[col]):
            prec = _float_precision(str(col))
            df[col] = df[col].map(lambda v: f"{v:.{prec}f}" if pd.notna(v) else "")

    data = [list(df.columns)] + df.astype(str).values.tolist()
    t = Table(data, hAlign="LEFT")
    style_items = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9CA3AF")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    if word_wrap:
        style_items.append(("WORDWRAP", (0, 0), (-1, -1), "CJK"))

    style = TableStyle(
        style_items
    )
    t.setStyle(style)
    return t


def generate_pdf(summary: pd.DataFrame, results_dir: str, figures_dir: str, out_pdf: str) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=11))

    doc = SimpleDocTemplate(out_pdf, pagesize=A4, title="Relatório Fluxo em Redes")
    story: List[Any] = []

    story.append(Paragraph("Relatório — Fluxo em Redes (Caminho Mínimo)", styles["Title"]))
    story.append(Paragraph(f"Gerado em {datetime.utcnow().isoformat()}Z", styles["Small"]))
    story.append(Spacer(1, 12))

    sim_names = {
        1: "Simulação 1 — Bellman recursivo em DAG",
        2: "Simulação 2 — Dijkstra com Heap (Best-First)",
        3: "Simulação 3 — Floyd-Warshall (matriz de custos)",
    }

    for sim_id in sorted(summary["sim_id"].unique()):
        story.append(PageBreak())
        story.append(Paragraph(sim_names[int(sim_id)], styles["Heading1"]))

        sim_df = summary[summary["sim_id"] == sim_id].sort_values("n")
        story.append(_df_to_reportlab_table(sim_df[["n", "m", "neg_edges", "runtime_s", "dist_mean", "dist_std"]], max_rows=10))
        story.append(Spacer(1, 12))

        for _, row in sim_df.iterrows():
            n = int(row["n"])
            story.append(Paragraph(f"Execução n={n}", styles["Heading2"]))

            sim_name = str(row.get("sim_name", "")) or ("Bellman" if int(sim_id) == 1 else "Dijkstra" if int(sim_id) == 2 else "Floyd")
            dist_df = _read_distances(results_dir, int(sim_id), sim_name, n)
            ana = _analyze_run(row, dist_df)

            story.append(Paragraph(f"• Arestas (m): {ana['m']} | densidade efetiva: {ana['eff_density']:.3f} | arestas negativas: {int(row['neg_edges'])}", styles["Small"]))
            story.append(Paragraph(f"• Alcançáveis a partir de X1: {ana['reachable']}/{ana['n']}", styles["Small"]))
            story.append(Paragraph(f"• Tempo de execução: {float(row['runtime_s']):.6f} s", styles["Small"]))
            story.append(Spacer(1, 8))

            # Foto do grafo
            try:
                graph_viz = _ensure_graph_viz(results_dir, figures_dir, int(sim_id), sim_name, n)
                if os.path.exists(graph_viz):
                    story.append(Image(graph_viz, width=500, height=350))
                    story.append(Spacer(1, 6))
            except Exception:
                pass

            if n <= 10:
                story.append(Paragraph("Ranking de distância (mais perto → mais longe)", styles["Heading3"]))
                story.append(_df_to_reportlab_table(ana["rank_all"], max_rows=n))
                story.append(Spacer(1, 8))
            else:
                story.append(Paragraph("Top 10 mais distantes", styles["Heading3"]))
                story.append(_df_to_reportlab_table(ana["top_far"], max_rows=10, font_size=8, word_wrap=True))
                story.append(Spacer(1, 8))

                story.append(Paragraph("Top 10 mais próximos", styles["Heading3"]))
                if n == 100:
                    top_close_fmt = ana["top_close"].copy()
                    if "path" in top_close_fmt.columns:
                        top_close_fmt["path"] = top_close_fmt["path"].map(_path_to_commas)
                    story.append(_df_to_reportlab_table(top_close_fmt, max_rows=10, font_size=8, word_wrap=True))
                else:
                    story.append(_df_to_reportlab_table(ana["top_close"], max_rows=10, font_size=8, word_wrap=True))
                story.append(Spacer(1, 8))

            # Gráfico da série
            series = os.path.join(figures_dir, f"sim{int(sim_id)}_{sim_name}_n{n}_series.png")
            if os.path.exists(series):
                story.append(Image(series, width=500, height=250))
                story.append(Spacer(1, 6))

    # Parte 2 — espaço reservado
    story.append(PageBreak())
    story.append(Paragraph("Parte 2 — Linguagem generativa (prompts)", styles["Heading1"]))
    story.append(Paragraph("Modelo utilizado e especificações", styles["Heading2"]))
    story.append(Paragraph("• Modelo utilizado: GPT", styles["BodyText"]))
    story.append(Paragraph("• Versão/fornecedor: 5.2 Thinking", styles["BodyText"]))
    story.append(Paragraph("• Prompt final utilizado:  Dado os grafos direcionados com vértices X1..Xn: (6 arquivos .txt anexados) calcule apenas o custo do caminho mínimo de X1 até todos os demais vértices Para cada um dos arquivos .txt anexados Devolva listas de n valores d(X1)..d(Xn), uma para cada arquivo .txt.", styles["BodyText"]))
    story.append(Paragraph("• Observações de execução: A LLM pensou por 2m e 37 segundos ao total para as 6 simulações", styles["BodyText"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Comparação LLM vs algoritmos", styles["Heading2"]))
    llm = _load_llm_results(results_dir)
    if not llm:
        story.append(Paragraph("Arquivo results/llm_results.json não encontrado.", styles["BodyText"]))
    else:
        results = llm.get("results", {})
        rows = []
        for key, llm_vals in results.items():
            parsed = _parse_llm_key(key)
            if not parsed:
                continue
            sim_id, sim_name, n = parsed
            dist_df = _read_distances(results_dir, sim_id, sim_name, n)
            comp = _compare_llm_vs_alg(dist_df, llm_vals)
            rows.append(
                {
                    "sim_id": sim_id,
                    "sim_name": sim_name,
                    "n": n,
                    "n_alg": comp["n_alg"],
                    "n_llm": comp["n_llm"],
                    "matches": comp["matches"],
                    "compared": comp["compared"],
                    "mean_abs_diff": comp["mean_abs_diff"],
                    "max_abs_diff": comp["max_abs_diff"],
                }
            )

        if rows:
            df_llm = pd.DataFrame(rows).sort_values(["sim_id", "n"])
            story.append(_df_to_reportlab_table(df_llm, max_rows=20, font_size=8, word_wrap=True))

            for key, llm_vals in results.items():
                parsed = _parse_llm_key(key)
                if not parsed:
                    continue
                sim_id, sim_name, n = parsed
                story.append(Spacer(1, 8))
                story.append(Paragraph(f"Lado a lado — sim{sim_id} {sim_name} n={n}", styles["Heading3"]))
                dist_df = _read_distances(results_dir, sim_id, sim_name, n)
                side_df = _side_by_side_df(dist_df, llm_vals)
                story.append(_df_to_reportlab_table(side_df, max_rows=n, font_size=7, word_wrap=True))
        else:
            story.append(Paragraph("Nenhum resultado LLM válido encontrado em results/llm_results.json.", styles["BodyText"]))

    # Resumo executivo (ao final)
    story.append(PageBreak())
    story.append(Paragraph("Resumo executivo", styles["Heading1"]))
    show_cols = ["sim_id", "sim_name", "n", "m", "neg_edges", "runtime_s", "dist_reachable", "dist_mean", "dist_max"]
    story.append(_df_to_reportlab_table(summary[show_cols].sort_values(["sim_id", "n"]), max_rows=20))

    doc.build(story)


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera relatório (MD e PDF) a partir dos resultados")
    ap.add_argument("--results", type=str, default="results", help="Pasta com summary.csv e distâncias")
    ap.add_argument("--figures", type=str, default="figures", help="Pasta com figuras")
    ap.add_argument("--out", type=str, default="report", help="Pasta de saída")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    summary_path = os.path.join(args.results, "summary.csv")
    summary = pd.read_csv(summary_path)

    md = generate_markdown_report(summary, args.results, args.figures)
    md_path = os.path.join(args.out, "relatorio.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    pdf_path = os.path.join(args.out, "relatorio.pdf")
    generate_pdf(summary, args.results, args.figures, pdf_path)

    print(f"Markdown: {md_path}")
    print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
