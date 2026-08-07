"""Design-basis baseline run: Helion's own implied point at 1 GWe."""
from study import build_model, load_config, run

if __name__ == "__main__":
    cfg = load_config("baseline.yaml")
    model = build_model(cfg)
    result, diag = run(model, dict(cfg["forward"]))
    pt = result.power_table
    print(f"LCOE            {diag['lcoe']:.1f} $/MWh")
    print(f"n_mod           {diag['n_mod']}")
    print(f"f_rep           {diag['f_rep_hz']:.2f} Hz")
    print(f"capital         {diag['capital_per_kw']:.0f} $/kW")
    print(f"p_fus/module    {float(pt.p_fus):.1f} MW")
    print(f"wall flux       {diag['q_wall_mw_m2']:.2f} MW/m^2")
    print(f"flash energy    {diag['e_flash_mj_m2']:.2f} MJ/m^2")
    for w in diag["warnings"]:
        print(f"warning: {w}")
