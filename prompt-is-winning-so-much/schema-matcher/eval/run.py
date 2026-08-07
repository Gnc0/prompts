#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schema-matcher 提示词评测 runner（prompt-iter ③）

【通用、不动】config 解析 · 叉积并发 · --force-variant 变体隔离 · 多 rep 汇总 · report/stability 结构。
【必须 customize】见标 #CUSTOMIZE 的四处：① fixture 载入+渲染 ② L1 确定性检查 ③ L2 判官 rubric ④ 产物 parser。
被测对象是「system prompt 本身」→ 跑一整个 chat turn：system=变体全文，user=fixture 的 turn。
多轮 fixture 在同一 chat 内顺序跑（以验证'沿用/增量重判/已确认不推翻'）。

endpoint/key 从环境变量读，绝不进 config：
  SCHEMA_EVAL_BASE_URL / SCHEMA_EVAL_API_KEY   （或回退 OPENAI_BASE_URL / OPENAI_API_KEY）

用法：
  python run.py --configs config.json
  python run.py --configs config.json --force-variant candidateA --samples 5 --judge gpt-5 --judge-k 5 --only protocol_3turn
"""

import argparse, json, os, re, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    sys.exit("缺少 openai 包：pip install openai")

EVAL_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = EVAL_DIR.parent  # schema-matcher/

# ──────────────────────────────────────────────────────────────
# L1 确定性层（#CUSTOMIZE ②：schema-matcher 专属的格式/行为护栏）
# ──────────────────────────────────────────────────────────────
DIM_NAMES = ["抽象↔具体", "中心↔边界", "融贯↔符合", "精确↔召回", "压缩↔展开", "构成↔调节"]
GOLD_KEYS = ["abstract", "center", "coherence", "precision", "density", "modal"]

# 锚点停留的五种合法写法（判断纪律第2条；中心↔边界轴的锚点在中心端，故用"中心·锚点"）
ANCHOR_TOKENS = {"居中·锚点", "中心·锚点", "居中偏精确·锚点", "居中偏压缩·锚点", "构成·锚点"}
POLES = ["抽象", "具体", "中心", "边界", "融贯", "符合", "精确", "召回", "压缩", "展开", "构成", "调节"]
LEVELS = ["微", "中", "重"]
# 禁止的量级变体
BAD_LEVEL_VARIANTS = ["微偏", "较重", "稍微", "略微", "偏微", "重偏", "中等偏移", "略微偏"]

# 正文不得暴露的理论术语（Mention：判断显式、理论隐身）。metalevel 轮按设计关闭。
FORBIDDEN_TERMS = [
    "图式匹配", "六对图式", "六根轴", "认识对象", "认识行为",
    "错配", "锚点", "融贯", "构成性", "调节性",
    "think_schema",
    "偏抽象", "偏具体", "偏中心", "偏边界", "偏融贯", "偏符合",
    "偏精确", "偏召回", "偏压缩", "偏展开", "偏构成", "偏调节",
]

ALLOWED_VALUE_RE = re.compile(
    r"^(偏(" + "|".join(POLES) + r")·(微|中|重)|"
    + "|".join(re.escape(t) for t in sorted(ANCHOR_TOKENS)) + r"|沿用)$"
)
TS_BLOCK_RE = re.compile(r"<think_schema>\s*(.*?)\s*</think_schema>", re.DOTALL)


def parse_value_token(value_part: str):
    """校验形如 '偏抽象·微' 的取值记号。SKILL 里 ［…］ 是占位符示意（列出可选值），
    真实输出直接写选中的值，不套方括号——故不要求括号，直接取 ｜ 之前的部分。"""
    token = value_part.strip()
    # 容错：若模型真套了方括号，剥掉
    if token and token[0] in "【[｢" and token[-1] in "】]｣":
        token = token[1:-1].strip()
    for bad in BAD_LEVEL_VARIANTS:
        if bad in token:
            return None, f"非法量级变体: {bad}"
    if ALLOWED_VALUE_RE.match(token):
        return token, None
    return None, f"非法取值记号: {token!r}"


def l1_check_turn(text: str, forbidden_terms: bool):
    """对单轮 assistant 输出跑确定性检查，返回 {pass, fails:[...], details}。"""
    fails, details = [], {}

    text_stripped = text.lstrip()
    # M1：think_schema 必须出现在开头（允许前置空白）
    head_idx = text.find("<think_schema>")
    if head_idx < 0:
        fails.append("M1_think_schema_absent"); 
        return {"pass": False, "fails": fails, "details": details}
    if text[:head_idx].strip() != "":
        fails.append("M1_think_schema_not_first")

    m = TS_BLOCK_RE.search(text)
    block = m.group(1) if m else ""
    if not block:
        fails.append("M1_think_schema_unclosed"); 
        return {"pass": False, "fails": fails, "details": details}

    # 块是否唯一
    if len(TS_BLOCK_RE.findall(text)) > 1:
        fails.append("M1_multiple_blocks")

    # M2：六维逐行
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    dim_seen = {}
    for ln in lines:
        mh = re.match(r"^(\d)\.\s*([^：:]+)[：:]\s*(.+)$", ln)
        if not mh:
            continue
        idx, name, rest = mh.group(1), mh.group(2).strip(), mh.group(3)
        if name not in DIM_NAMES:
            continue
        if idx in dim_seen:
            fails.append(f"M2_dup_dim_{idx}")
        dim_seen[idx] = (name, rest)
        # 拆 '值｜依据：…'
        parts = re.split(r"[｜|]", rest, maxsplit=1)
        value_part = parts[0]
        token, err = parse_value_token(value_part)
        if err:
            fails.append(f"M3_bad_notation_{name}:{err}")
        else:
            details.setdefault("declared", {})[name] = token
        if len(parts) < 2 or "依据" not in parts[1] or not parts[1].split("依据", 1)[1].strip("：: ").strip():
            fails.append(f"M2_missing_basis_{name}")

    for i, name in enumerate(DIM_NAMES, 1):
        if str(i) not in dim_seen:
            fails.append(f"M2_dim_missing_{name}")

    # M4：分层匹配 / 搁置 / 自检 三行
    for keyword in ["分层匹配", "搁置", "自检"]:
        if keyword not in block:
            fails.append(f"M4_missing_{keyword}")

    # M5：正文理论术语隐身
    body = text[m.end():] if m else ""
    if forbidden_terms:
        leaked = [t for t in FORBIDDEN_TERMS if t in body]
        if leaked:
            fails.append(f"M5_term_leak:{','.join(leaked)}")

    return {"pass": len(fails) == 0, "fails": fails, "details": details}


# ──────────────────────────────────────────────────────────────
# L2 判官（#CUSTOMIZE ③：语义残差——声明位置 vs 应然位置一致性 + 正文是否兑现）
# ──────────────────────────────────────────────────────────────
JUDGE_RUBRIC = """你是严格的图式匹配评判官。给你 schema-matcher 规范、一轮用户输入、模型的 <think_schema> 声明、模型正文，以及设计者对该轮各维"应然位置"的预期（gold，null 表示该维无强预期、不评）。
逐维判断两件事：
A) 声明的图式位置方向是否与 gold 应然方向相符（沿用也算相符，若 gold 也是沿用；gold=null 该维记 skip）。
B) 仅对 density/modal 两维额外判"正文是否兑现声明"：偏压缩→正文是否确实短而结论化；偏展开→是否给过程；构成→是否给判定；调节→是否标明认识边界不硬断言。
事实类输入还要判"有没有编造 gold 里不存在/无法核实的确切事实"。
只输出 JSON，schema：{"dims":{"abstract":{"declared":..,"gold":..,"dir_match":true/false/skip},"center":..,"coherence":..,"precision":..,"density":{"declared":..,"gold":..,"dir_match":..,"body_honors":true/false/skip},"modal":{"declared":..,"gold":..,"dir_match":..,"body_honors":true/false/skip}},"fabrication":true/false,"note":"一句"}. 不得输出 JSON 以外内容。"""


def l2_judge_turn(judge_client, judge_model, spec_excerpt, user_turn, model_reply, gold):
    prompt = (f"【规范摘要】\n{spec_excerpt}\n\n【用户输入】{user_turn}\n\n"
              f"【gold 应然】{json.dumps(gold, ensure_ascii=False)}\n\n"
              f"【模型完整回复】\n{model_reply}")
    try:
        resp = judge_client.chat.completions.create(
            model=judge_model,
            messages=[{"role": "system", "content": JUDGE_RUBRIC},
                      {"role": "user", "content": prompt}],
            temperature=0.0, max_tokens=700,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        return data, None
    except Exception as e:
        return None, f"judge_parse_fail:{type(e).__name__}:{e}"  # parse 失败按失败处理


# ──────────────────────────────────────────────────────────────
# runner 主流程
# ──────────────────────────────────────────────────────────────
def load_variants(vdir: Path):
    variants = {}
    for p in sorted(vdir.glob("*.md")):
        variants[p.stem] = p.read_text(encoding="utf-8")
    return variants


def run_one_unit(client, model, variant_text, fixture, sample_idx, max_tokens=2048):
    """跑一个 (config,fixture,sample) 单元：fixture 内多轮顺序执行。返回每轮产物。"""
    turns_out = []
    messages = [{"role": "system", "content": variant_text}]
    for ti, turn in enumerate(fixture["turns"]):
        messages.append({"role": "user", "content": turn["user"]})
        try:
            resp = client.chat.completions.create(
                model=model, messages=messages, temperature=1.0, max_tokens=max_tokens)
            reply = resp.choices[0].message.content or ""
        except Exception as e:
            turns_out.append({"turn": ti, "error": f"api:{type(e).__name__}:{e}", "raw": ""})
            break  # loud failure：后续轮失去上下文，停
        turns_out.append({
            "turn": ti, "user": turn["user"], "raw": reply,
            "forbidden_terms": turn.get("forbidden_terms", True),
        })
        messages.append({"role": "assistant", "content": reply})  # 状态推进，使沿用可被验证
    return {"sample": sample_idx, "turns": turns_out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", default="config.json")
    ap.add_argument("--force-variant", default=None, help="所有 config 改用该变体的 prompt")
    ap.add_argument("--samples", type=int, default=None, help="覆盖每 config 重复次数")
    ap.add_argument("--judge", default=None, help="判官 model；不传则只跑 L1")
    ap.add_argument("--judge-k", type=int, default=5, help="判官取 K 次中位数")
    ap.add_argument("--only", default=None, help="只跑某些 fixture，逗号分隔 id")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="out")
    ap.add_argument("--max-tokens", type=int, default=2048)
    args = ap.parse_args()

    cfg = json.loads((EVAL_DIR / args.configs).read_text(encoding="utf-8"))
    variants = load_variants(EVAL_DIR / cfg["variants_dir"])
    fixtures = json.loads((EVAL_DIR / cfg["fixtures_file"]).read_text(encoding="utf-8"))["fixtures"]
    if args.only:
        keep = set(args.only.split(","))
        fixtures = [f for f in fixtures if f["id"] in keep]
    if args.force_variant:
        if args.force_variant not in variants:
            sys.exit(f"变体不存在: {args.force_variant}；已有: {list(variants)}")
        for c in cfg["configs"]:
            c["variant"] = args.force_variant

    base = os.environ.get("SCHEMA_EVAL_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    key = os.environ.get("SCHEMA_EVAL_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not base or not key:
        sys.exit("缺少 endpoint/key：请 export SCHEMA_EVAL_BASE_URL 与 SCHEMA_EVAL_API_KEY（或 OPENAI_*）")
    client = OpenAI(base_url=base, api_key=key)
    judge_client = client
    judge_model = args.judge or cfg.get("judge", {}).get("model")
    if judge_model == "REPLACE_WITH_JUDGE_MODEL_ID":
        judge_model = None

    # 构造叉积单元
    units = []
    for c in cfg["configs"]:
        if c["model"].startswith("REPLACE_WITH"):
            print(f"[skip] config {c['name']} 的 model 未填写，跳过", file=sys.stderr)
            continue
        reps = args.samples if args.samples is not None else c.get("reps", 3)
        for f in fixtures:
            for s in range(reps):
                units.append((c, f, s))

    outdir = EVAL_DIR / args.out
    outdir.mkdir(exist_ok=True)
    spec_excerpt = variants.get("baseline", "")[:1500]
    results = []

    def work(unit):
        c, f, s = unit
        t0 = time.time()
        try:
            run = run_one_unit(client, c["model"], variants[c["variant"]], f, s, args.max_tokens)
        except Exception as e:
            return {"config": c["name"], "model": c["model"], "variant": c["variant"],
                    "fixture": f["id"], "sample": s, "error": f"unit_crash:{e}", "turns": []}
        # 逐轮 L1
        for t in run["turns"]:
            if t.get("raw"):
                t["l1"] = l1_check_turn(t["raw"], t["forbidden_terms"])
            # L2（可选，K 次中位数）
            if judge_model and t.get("raw"):
                gold = f["turns"][t["turn"]].get("gold", {})
                votes = []
                for _ in range(args.judge_k):
                    data, err = l2_judge_turn(judge_client, judge_model, spec_excerpt,
                                              t["user"], t["raw"], gold)
                    votes.append((data, err))
                t["l2_votes"] = votes
        run.update({"config": c["name"], "model": c["model"], "variant": c["variant"],
                    "fixture": f["id"], "elapsed": round(time.time() - t0, 1)})
        # 落单文件
        fp = outdir / f"{c['name']}__{f['id']}__s{s}.json"
        fp.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
        return run

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(work, u) for u in units]
        for fut in as_completed(futs):
            results.append(fut.result())
            print(f"[done] {len(results)}/{len(units)}", file=sys.stderr)

    # 汇总：report.md（每 config×fixture 的 L1 通过率 / L2 dir_match 中位）+ stability.md
    write_reports(results, outdir, cfg, judge_model is not None)
    print(f"\n汇总写入 {outdir/'report.md'} 与 {outdir/'stability.md'}", file=sys.stderr)


def write_reports(results, outdir, cfg, has_judge):
    from collections import defaultdict
    by_cell = defaultdict(list)  # (config,fixture)->[run,...]
    for r in results:
        by_cell[(r["config"], r["fixture"])].append(r)

    lines = ["# schema-matcher 评测报告", ""]
    lines.append("L1=确定性层（格式/记号/理论隐身护栏，任一不过即该轮失败）。"
                 + ("L2=判官方向一致性+正文兑现（中位数）。" if has_judge else "（未启用判官）") + "\n")
    lines.append("| config | fixture | samples | L1 通过率 | L2 dir_match | L2 body_honors |")
    lines.append("|---|---|---|---|---|---|")
    for (cfg_name, fx_id), runs in sorted(by_cell.items()):
        n = len(runs)
        # L1：以每 run 的"所有轮都过"计通过
        l1_pass = 0
        dir_match_votes, body_votes = [], []
        for r in runs:
            if not r["turns"]:
                continue
            all_ok = all(t.get("l1", {}).get("pass") for t in r["turns"] if t.get("raw"))
            if all_ok:
                l1_pass += 1
            for t in r["turns"]:
                for data, err in t.get("l2_votes", []):
                    if err or not data:
                        continue
                    for k in ("density", "modal"):
                        v = data.get("dims", {}).get(k, {})
                        if v.get("dir_match") in (True, False):
                            dir_match_votes.append(1 if v["dir_match"] else 0)
                        if v.get("body_honors") in (True, False):
                            body_votes.append(1 if v["body_honors"] else 0)
        l1_rate = f"{l1_pass}/{n}"
        dm = f"{sum(dir_match_votes)/len(dir_match_votes):.2f}" if dir_match_votes else "-"
        bh = f"{sum(body_votes)/len(body_votes):.2f}" if body_votes else "-"
        lines.append(f"| {cfg_name} | {fx_id} | {n} | {l1_rate} | {dm} | {bh} |")
    (outdir / "report.md").write_text("\n".join(lines), encoding="utf-8")

    # stability：每个 fixture 的 L1 失败原因分布（多 rep 才有意义）
    s_lines = ["# 稳定性 / 失败原因分布", "",
               "多 rep 下 L1 失败原因的频次——同一原因反复出现=系统性缺陷，偶现=噪音。", ""]
    fail_dist = defaultdict(lambda: defaultdict(int))
    for r in results:
        for t in r["turns"]:
            for f_ in t.get("l1", {}).get("fails", []):
                key = re.sub(r":.*", "", f_)
                fail_dist[r["fixture"]][key] += 1
    for fx_id, dist in sorted(fail_dist.items()):
        if not dist:
            continue
        s_lines.append(f"## {fx_id}")
        for k, v in sorted(dist.items(), key=lambda x: -x[1]):
            s_lines.append(f"- {k}: {v}")
        s_lines.append("")
    (outdir / "stability.md").write_text("\n".join(s_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
