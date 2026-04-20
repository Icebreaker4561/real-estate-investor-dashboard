#!/usr/bin/env python3
"""
Developer economics calculator — Georgian cottage village formats.
Independently verifies and recalculates all 3 developer format models.

FORMULAS:
  margin_pct  = margin / sale_price  (% of revenue — стандарт застройщика)
  roi_pct     = project_profit / project_costs  (% of invested capital)
  breakeven   = ceil(project_costs / sale_price)  (минимум ед. для выхода в 0)
"""
import math

FORMATS = [
    {
        "name": "Формат 1: Тбилиси пригород",
        "emoji": "🏙️",
        "description": "25 домов × 160 м², газобетон, Сагурамо/Мцхета",
        "units": 25,
        "area_per_unit": 160,         # м² жилой площади
        "total_land_m2": 8_333,       # реальные 0.83 га под 25 домов (300 м²/ед. × 25 + 10% серв.)
        "land_price_per_m2": 55,      # $/м², ⚠️ допущение (оптовая Тбилиси пригород)
        "land_warning": True,
        "construction_per_m2": 600,   # $/м², стандарт (подтверждено инвестором)
        "infra_per_unit": 20_000,     # дороги, коммуникации
        "permits_per_unit": 7_000,    # проект + разрешения
        "sales_pct": 0.05,            # % от цены продажи
        "pm_per_unit": 8_000,         # управление проектом
        "sale_price_per_m2": 1_400,   # $/м², рыночная цена (Tranio/Galt&Taggart)
        "duration_months": 30,
        "target_buyer": "IT-семьи, релоканты, долгосрочная аренда",
        "catalyst": None,
    },
    {
        "name": "Формат 2: Гонио (прибрежный рост)",
        "emoji": "🌊",
        "description": "20 домов × 180 м², участок 300 м²/ед., стандарт, 5 км от Батуми",
        "units": 20,
        "area_per_unit": 180,
        "total_land_m2": 8_000,       # 20 × ~300 м² + дороги/общее
        "land_price_per_m2": 175,     # $/м², подтверждено инвестором-резидентом апр.2026
        "land_warning": False,
        "construction_per_m2": 600,
        "infra_per_unit": 28_000,     # дороги, сети, забор
        "permits_per_unit": 9_000,
        "sales_pct": 0.05,
        "pm_per_unit": 10_000,
        "sale_price_per_m2": 1_800,   # $/м², рыночный ориентир Гонио (Korter.ge апр.2026)
        "duration_months": 36,
        "target_buyer": "Инвесторы под STR, туристы",
        "catalyst": "Emaar Gonio Marina ($5.5B, анонс 2025) ↑ цены",
    },
    {
        "name": "Формат 3: Квариати/Чакви (премиум)",
        "emoji": "🏆",
        "description": "12 вилл × 250 м², участок 350 м²/ед., монолит + чистовая, 1-я линия",
        "units": 12,
        "area_per_unit": 250,
        "total_land_m2": 6_600,       # 12 × ~350 м² + дороги/общее
        "land_price_per_m2": 175,
        "land_warning": False,
        "construction_per_m2": 750,   # премиум, подтверждено инвестором
        "infra_per_unit": 45_000,     # бассейн, ландшафт, забор
        "permits_per_unit": 18_000,
        "sales_pct": 0.05,
        "pm_per_unit": 15_000,
        "sale_price_per_m2": 2_000,   # $/м², ориентир (Diamond Villas $1 579 + ~25% премиум)
        "duration_months": 42,
        "target_buyer": "Состоятельные иностранцы под STR / летний дом",
        "catalyst": None,
    },
]


def calc_format(f):
    u = f["units"]

    # --- COSTS per unit ---
    land_total = f["total_land_m2"] * f["land_price_per_m2"]
    land_per_unit = land_total / u

    construction = f["area_per_unit"] * f["construction_per_m2"]
    sale_price = f["area_per_unit"] * f["sale_price_per_m2"]
    sales_cost = sale_price * f["sales_pct"]

    cost_subtotal = (
        land_per_unit
        + construction
        + f["infra_per_unit"]
        + f["permits_per_unit"]
        + f["pm_per_unit"]
    )
    total_cost = cost_subtotal + sales_cost
    margin = sale_price - total_cost
    margin_pct = margin / sale_price * 100  # % of revenue (застройщик-стандарт)

    # --- PROJECT totals ---
    project_costs = total_cost * u
    project_revenue = sale_price * u
    project_profit = project_revenue - project_costs
    roi_pct = project_profit / project_costs * 100

    # --- Breakeven: ceil (нужно продать минимум X ед. чтобы покрыть ВСЕ затраты) ---
    breakeven_units_exact = project_costs / sale_price
    breakeven_units = math.ceil(breakeven_units_exact)
    breakeven_pct = breakeven_units / u * 100

    return {
        "land_total": land_total,
        "land_per_unit": land_per_unit,
        "construction": construction,
        "sales_cost": sales_cost,
        "total_cost": total_cost,
        "sale_price": sale_price,
        "margin": margin,
        "margin_pct": margin_pct,
        "project_costs": project_costs,
        "project_revenue": project_revenue,
        "project_profit": project_profit,
        "roi_pct": roi_pct,
        "breakeven_units": breakeven_units,
        "breakeven_pct": breakeven_pct,
    }


def fmt_usd(v):
    return f"${v:,.0f}".replace(",", " ")


def fmt_pct(v):
    return f"{v:.1f}%"


def print_format(f, r):
    warn = " ⚠️" if f["land_warning"] else ""
    print(f"\n{'='*62}")
    print(f"  {f['emoji']}  {f['name']}")
    print(f"  {f['description']}")
    print(f"{'='*62}")

    u = f["units"]

    print(f"\n  {'--- ЗАТРАТЫ НА 1 ОБЪ ЕКТ ---':}")
    print(f"  {'Земля (опт)' + warn:<35} {fmt_usd(r['land_per_unit']):>10}")
    print(f"    {f['total_land_m2']:,} м² × ${f['land_price_per_m2']}/м² ÷ {u} ед.")
    print(f"  {'Строительство':<35} {fmt_usd(r['construction']):>10}")
    print(f"    {f['area_per_unit']} м² × ${f['construction_per_m2']}/м²")
    print(f"  {'Инфра':<35} {fmt_usd(f['infra_per_unit']):>10}")
    print(f"  {'Проект + разрешения':<35} {fmt_usd(f['permits_per_unit']):>10}")
    print(f"  {'Продажи и маркетинг 5%':<35} {fmt_usd(r['sales_cost']):>10}")
    print(f"    5% × {fmt_usd(r['sale_price'])}")
    print(f"  {'Управление проектом':<35} {fmt_usd(f['pm_per_unit']):>10}")
    print(f"  {'-'*47}")
    print(f"  {'ИТОГО ЗАТРАТ':<35} {fmt_usd(r['total_cost']):>10}")
    print(f"  {'Цена продажи (${}/м²)'.format(f['sale_price_per_m2']):<35} {fmt_usd(r['sale_price']):>10}")
    print(f"  {'МАРЖА ЗАСТРОЙЩИКА':<35} {fmt_usd(r['margin']):>10}  ({fmt_pct(r['margin_pct'])})")

    print(f"\n  {'--- ВЕСЬ ПРОЕКТ ({} ед.) ---'.format(u):}")
    print(f"  {'Вложения (все затраты)':<35} {fmt_usd(r['project_costs']):>10}")
    print(f"  {'Выручка (все продажи)':<35} {fmt_usd(r['project_revenue']):>10}")
    print(f"  {'ПРИБЫЛЬ':<35} {fmt_usd(r['project_profit']):>10}")
    print(f"  {'ROI (прибыль / вложения)':<35} {fmt_pct(r['roi_pct']):>10}  за {f['duration_months']} мес.")
    print(f"  {'Breakeven':<35} {r['breakeven_units']}/{u} ед.  ({fmt_pct(r['breakeven_pct'])})")

    print(f"\n  Целевой покупатель: {f['target_buyer']}")
    if f.get("catalyst"):
        print(f"  Катализатор: {f['catalyst']}")

    if f["land_warning"]:
        print(f"\n  ⚠️  Земля: допущение без прямого источника по Тбилиси пригород.")
        print(f"      Оптовая цена $55/м² — оценка на основе Tranio/Galt&Taggart.")


def main():
    print("DEVELOPER ECONOMICS — Коттеджные поселки Грузия 2025–2026")
    print("Расчёт на 1 объект. Земля — оптовая закупка всего участка.")

    results = []
    for f in FORMATS:
        r = calc_format(f)
        results.append((f, r))
        print_format(f, r)

    # --- Сводная таблица ---
    print(f"\n\n{'='*62}")
    print("  СВОДНАЯ ТАБЛИЦА")
    print(f"{'='*62}")
    print(f"  {'Параметр':<28} {'Ф1':>10} {'Ф2':>10} {'Ф3':>10}")
    print(f"  {'-'*58}")

    rows = [
        ("Затраты/ед.", lambda r: fmt_usd(r["total_cost"])),
        ("Цена продажи/ед.", lambda r: fmt_usd(r["sale_price"])),
        ("Маржа/ед.", lambda r: fmt_usd(r["margin"])),
        ("Маржа %", lambda r: fmt_pct(r["margin_pct"])),
        ("Прибыль (проект)", lambda r: fmt_usd(r["project_profit"])),
        ("Вложения (проект)", lambda r: fmt_usd(r["project_costs"])),
        ("ROI проекта", lambda r: fmt_pct(r["roi_pct"])),
        ("Breakeven (ед.)", lambda r: f"{r['breakeven_units']}"),
        ("Breakeven %", lambda r: fmt_pct(r["breakeven_pct"])),
    ]

    for label, fn in rows:
        vals = [fn(r) for _, r in results]
        print(f"  {label:<28} {vals[0]:>10} {vals[1]:>10} {vals[2]:>10}")

    print(f"\n  Срок реализации (мес.)   {'30':>10} {'36':>10} {'42':>10}")
    print()


# ─────────────────────────────────────────────────────────────
# SECTION 8 — Investor calculator (apartment 50 m²)
# ─────────────────────────────────────────────────────────────

SEC8_PARAMS = {
    "area": 50,
    "renovation_per_m2": 700,
    "tax_rate": 0.05,
    "mgmt_rate": 0.30,          # STR only
    "util_per_m2_month": 2.0,   # $1 коммун. + $1 ТО
}

SEC8_SCENARIOS = [
    # LTR Tbilisi — Сабуртало ($1 200/м²)
    {"name": "LTR Tbilisi Пессимист", "price_m2": 1200, "str": False,
     "gross_yr": 450 * 12,   "html_net": 3930,  "html_yield_pct": 4.1},
    {"name": "LTR Tbilisi Реалист",   "price_m2": 1200, "str": False,
     "gross_yr": 550 * 12,   "html_net": 5070,  "html_yield_pct": 5.3},
    {"name": "LTR Tbilisi Оптимист",  "price_m2": 1200, "str": False,
     "gross_yr": 700 * 12,   "html_net": 6780,  "html_yield_pct": 7.1},

    # STR Tbilisi — центр ($1 600/м²)
    {"name": "STR Tbilisi Пессимист", "price_m2": 1600, "str": True,
     "gross_yr": 57 * 149,   "html_net": 4320,  "html_yield_pct": 3.8},
    {"name": "STR Tbilisi Реалист",   "price_m2": 1600, "str": True,
     "gross_yr": 42 * 230,   "html_net": 5079,  "html_yield_pct": 4.4},
    {"name": "STR Tbilisi Оптимист",  "price_m2": 1600, "str": True,
     "gross_yr": 62 * 252,   "html_net": 8956,  "html_yield_pct": 7.8},

    # STR Batumi — 1-я линия ($1 600/м²)
    {"name": "STR Batumi Пессимист",  "price_m2": 1600, "str": True,
     "gross_yr": 3766,        "html_net": 1248,  "html_yield_pct": 1.1},
    {"name": "STR Batumi Реалист",    "price_m2": 1600, "str": True,
     "gross_yr": 43 * 193,    "html_net": 4194,  "html_yield_pct": 3.6},
    {"name": "STR Batumi Оптимист",   "price_m2": 1600, "str": True,
     "gross_yr": 63 * 204,    "html_net": 7153,  "html_yield_pct": 6.2},
]


def calc_sec8(s):
    p = SEC8_PARAMS
    investment = s["price_m2"] * p["area"] + p["renovation_per_m2"] * p["area"]
    util_yr = p["util_per_m2_month"] * p["area"] * 12
    gross = s["gross_yr"]
    mgmt = gross * p["mgmt_rate"] if s["str"] else 0
    tax = gross * p["tax_rate"]
    net = gross - mgmt - tax - util_yr
    yield_pct = net / investment * 100
    return {"investment": investment, "gross": gross, "mgmt": mgmt,
            "tax": tax, "util_yr": util_yr, "net": net, "yield_pct": yield_pct}


def verify_sec8():
    print(f"\n{'='*62}")
    print("  SECTION 8 — КАЛЬКУЛЯТОР ИНВЕСТОРА (9 сценариев)")
    print(f"{'='*62}")
    all_ok = True
    for s in SEC8_SCENARIOS:
        r = calc_sec8(s)
        checks = [
            ("Net доход/год", r["net"],       s["html_net"],       1),
            ("Net yield %",   r["yield_pct"], s["html_yield_pct"], 0.1),
        ]
        ok_all = all(abs(c - h) <= t for _, c, h, t in checks)
        if not ok_all:
            all_ok = False
        status = "✅" if ok_all else "❌"
        print(f"  {status} {s['name']:<28}  "
              f"net={r['net']:,.0f} (HTML={s['html_net']:,})  "
              f"yield={r['yield_pct']:.1f}% (HTML={s['html_yield_pct']}%)")
        if not ok_all:
            for label, calc, html, tol in checks:
                if abs(calc - html) > tol:
                    print(f"      ❌ {label}: скрипт={calc:.1f}  HTML={html}")
    return all_ok


# ─────────────────────────────────────────────────────────────
# SECTION 10 — Cottage yield table (investor-buyer)
# ─────────────────────────────────────────────────────────────

SEC10_COTTAGES = [
    {"name": "Тбилиси LTR 160м²", "area": 160, "price": 224_000, "str": False,
     "gross_yr": 1500 * 12,  "mgmt_rate": 0,
     "html_tax": 900, "html_util": 3840, "html_net": 13260, "html_yield": 5.9},
    {"name": "Гонио STR 180м²",   "area": 180, "price": 324_000, "str": True,
     "gross_yr": 183 * 120, "mgmt_rate": 0.30,
     "html_tax": 1098, "html_util": 4320, "html_net": 9954, "html_yield": 3.1},
    {"name": "Квариати STR 250м²","area": 250, "price": 500_000, "str": True,
     "gross_yr": 150 * 200, "mgmt_rate": 0.30,
     "html_tax": 1500, "html_util": 6000, "html_net": 13500, "html_yield": 2.7},
]


def calc_sec10(c):
    gross = c["gross_yr"]
    mgmt = gross * c["mgmt_rate"]
    tax = gross * 0.05
    util_yr = 2.0 * c["area"] * 12
    net = gross - mgmt - tax - util_yr
    yield_pct = net / c["price"] * 100
    return {"mgmt": mgmt, "tax": tax, "util_yr": util_yr,
            "net": net, "yield_pct": yield_pct}


def verify_sec10():
    print(f"\n{'='*62}")
    print("  SECTION 10 — ДОХОДНОСТЬ КОТТЕДЖА (инвестор-покупатель)")
    print(f"{'='*62}")
    all_ok = True
    for c in SEC10_COTTAGES:
        r = calc_sec10(c)
        checks = [
            ("−Налог",      r["tax"],      c["html_tax"],   1),
            ("−Эксплуат.",  r["util_yr"],  c["html_util"],  1),
            ("Net доход",   r["net"],      c["html_net"],   1),
            ("Net yield %", r["yield_pct"],c["html_yield"],  0.1),
        ]
        ok_all = all(abs(cv - h) <= t for _, cv, h, t in checks)
        if not ok_all:
            all_ok = False
        status = "✅" if ok_all else "❌"
        print(f"  {status} {c['name']}")
        for label, calc, html, tol in checks:
            ok = abs(calc - html) <= tol
            sym = "  ✅" if ok else "  ❌"
            if not ok:
                all_ok = False
            fmt_c = f"{calc:.1f}" if isinstance(calc, float) and calc < 100 else f"{calc:,.0f}"
            fmt_h = f"{html:.1f}" if isinstance(html, float) and html < 100 else f"{html:,}"
            print(f"    {sym} {label:<14} скрипт={fmt_c}  HTML={fmt_h}")
    return all_ok


EXPECTED_HTML = [
    # (total_cost, sale_price, margin, margin_pct, project_profit, project_costs, roi_pct, breakeven_units, breakeven_pct)
    (160_533, 224_000, 63_467, 28.3, 1_586_685, 4_013_315, 39.5, 18, 72.0),
    (241_200, 324_000, 82_800, 25.6, 1_656_000, 4_824_000, 34.3, 15, 75.0),
    (386_750, 500_000, 113_250, 22.7, 1_359_000, 4_641_000, 29.3, 10, 83.3),
]

def verify_vs_html():
    print(f"\n{'='*62}")
    print("  ВЕРИФИКАЦИЯ vs ЗНАЧЕНИЯ В ДАШБОРДЕ")
    print(f"{'='*62}")
    all_ok = True
    for i, (f, exp) in enumerate(zip(FORMATS, EXPECTED_HTML), 1):
        r = calc_format(f)
        checks = [
            ("Итого затрат",   r["total_cost"],      exp[0], 1),
            ("Цена продажи",   r["sale_price"],       exp[1], 1),
            ("Маржа $",        r["margin"],           exp[2], 1),
            ("Маржа %",        r["margin_pct"],       exp[3], 0.1),
            ("Прибыль проект", r["project_profit"],   exp[4], 1),
            ("Вложения проект",r["project_costs"],    exp[5], 1),
            ("ROI %",          r["roi_pct"],          exp[6], 0.1),
            ("Breakeven ед.",  r["breakeven_units"],  exp[7], 0),
            ("Breakeven %",    r["breakeven_pct"],    exp[8], 0.2),
        ]
        print(f"\n  Формат {i}: {f['name']}")
        for label, calc, html, tol in checks:
            ok = abs(calc - html) <= tol
            status = "✅" if ok else "❌"
            if not ok:
                all_ok = False
            print(f"    {status} {label:<22} скрипт={calc:,.1f}  HTML={html:,.1f}")
    print(f"\n  {'✅ Все значения совпадают с дашбордом.' if all_ok else '❌ Есть расхождения — нужно обновить дашборд.'}")
    return all_ok


if __name__ == "__main__":
    main()
    ok1 = verify_vs_html()
    ok2 = verify_sec8()
    ok3 = verify_sec10()
    print(f"\n{'='*62}")
    if ok1 and ok2 and ok3:
        print("  ✅ ВСЕ ПРОИЗВОДНЫЕ ЦИФРЫ ВЕРНЫ — дашборд корректен.")
    else:
        print("  ❌ НАЙДЕНЫ РАСХОЖДЕНИЯ — см. ❌ выше, нужно обновить HTML.")
    print(f"{'='*62}\n")
