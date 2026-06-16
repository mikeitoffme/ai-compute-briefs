"""
Reproducible model for two analyst slides.

All inputs are assumptions sourced in sources.md. 

"""

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def fmt_m(x):
    """Format a count of accelerators in millions."""
    return f"{x/1e6:.2f}M"


def pct(x):
    return f"{x*100:.0f}%"


# ===========================================================================
# SLIDE 1 — Fleet size and training/inference split
# ===========================================================================
# We report OPERATIONAL fleets as of May 2026, normalized to "H100-equivalents"
# (H100-eq) because Anthropic runs mostly non-NVIDIA ASICs (AWS Trainium, Google
# TPU). Raw unit counts and announced/contracted capacity are reported
# separately so they are never confused with what is running today.

# --- Conversion factors (see sources.md, "Conversion factors") -------------
KW_PER_CHIP_ALLIN = 1.5          # facility wall power per accelerator, PUE baked in (1.3-1.7)
CHIPS_PER_GW = 1e6 / KW_PER_CHIP_ALLIN   # ~667k H100-class chips per GW of IT+facility power

# Per-chip H100-equivalent multipliers (inference-relevant, conservative).
H100_EQ = {
    "H100": 1.0, "H200": 1.3, "GB200": 3.0, "GB300": 4.5,
    "TPUv6e": 1.0, "TPUv7": 2.5, "Trn2": 0.7, "Trn3": 1.7,
}


@dataclass
class Fleet:
    """Operational fleet estimate, May 2026, in H100-equivalents."""
    name: str
    h100eq_low: float
    h100eq_base: float
    h100eq_high: float
    inference_share: float       # fraction of compute serving users (base)
    inference_share_lo: float
    inference_share_hi: float
    note: str


# Anchors:
#   OpenAI  - Epoch AI: ~1.1M H100-eq mid-2025 (CI 0.8-1.4M). Hopper-class legacy
#             holds ~1.25M H100-eq; add ~0.25M GB200 coming online across
#             Azure/Oracle/CoreWeave/Abilene (x3 -> ~0.75M H100-eq) -> ~2.0M base
#             by May 2026 (1.4M low / 3.0M high).
#   Anthropic - bottom-up: Trainium2 ~0.8M units (x0.7 -> 0.56M) + Google TPU
#             ~0.6M mixed-gen (x~1.2 -> 0.72M) + NVIDIA ~0.25M incl. SpaceX
#             Colossus, H100/H200/GB200 mix (x~1.6 -> 0.40M) -> ~1.7M H100-eq base.
openai = Fleet(
    name="OpenAI",
    h100eq_low=1.4e6, h100eq_base=2.0e6, h100eq_high=3.0e6,
    inference_share=0.48, inference_share_lo=0.45, inference_share_hi=0.55,
    note="Almost entirely NVIDIA (Hopper legacy + GB200 Blackwell).",
)
anthropic = Fleet(
    name="Anthropic",
    h100eq_low=1.0e6, h100eq_base=1.7e6, h100eq_high=3.0e6,
    inference_share=0.65, inference_share_lo=0.55, inference_share_hi=0.75,
    note="Mostly ASICs: AWS Trainium (training) + Google TPU (inference); little NVIDIA.",
)

# Industry reference split (Barclays: >70% inference by 2026, ~4.5x training;
# Jensen Huang: "the vast majority of our compute today is actually inference",
# NVIDIA Q4 FY2026 call; McKinsey: >half of DC spend is GPUs/networking).
INDUSTRY_INFERENCE_SHARE = 0.65

# Announced / CONTRACTED capacity (2026-2029) — explicitly NOT today's fleet.
CONTRACTED = {
    "OpenAI": "~30+ GW announced (NVIDIA 10 + AMD 6 + Broadcom 10 + Oracle 4.5); "
              "Jensen: NVIDIA deal alone = '4-5M GPUs' by 2029.",
    "Anthropic": "up to 5 GW AWS Trainium + ~1M Google TPU (1 GW, 2026) + "
                 "~3.5 GW Google/Broadcom (from 2027) + up to 1 GW Azure NVIDIA.",
}


# H100-equivalents are a PERFORMANCE aggregate, not a physical chip count: a GB200
# delivers ~3x an H100 per chip, so a Blackwell-heavy fleet has far fewer physical
# accelerators than its H100-eq total. Blended across Hopper legacy + GB200 ramp,
# ~1.3 H100-eq per physical accelerator.
EQ_PER_PHYSICAL_CHIP = 1.3


def sanity_check_power(gw):
    """Cross-check: how many H100-class chips fit in `gw` of operational power."""
    return gw * CHIPS_PER_GW


def physical_chips(h100eq):
    """Physical accelerator count implied by an H100-equivalent aggregate."""
    return h100eq / EQ_PER_PHYSICAL_CHIP


def slide1():
    print("=" * 70)
    print("SLIDE 1 — OpenAI vs Anthropic accelerator fleets (operational, May 2026)")
    print("=" * 70)
    for f in (openai, anthropic):
        print(f"\n{f.name}")
        print(f"  Fleet (H100-equivalents): "
              f"low {fmt_m(f.h100eq_low)} | base {fmt_m(f.h100eq_base)} | high {fmt_m(f.h100eq_high)}")
        inf = f.h100eq_base * f.inference_share
        tr = f.h100eq_base * (1 - f.inference_share)
        print(f"  Split (base): inference {pct(f.inference_share)} "
              f"(~{fmt_m(inf)} H100-eq) | training+research {pct(1-f.inference_share)} (~{fmt_m(tr)})")
        print(f"  Split range:  inference {pct(f.inference_share_lo)}-{pct(f.inference_share_hi)}")
        print(f"  {f.note}")
        print(f"  Contracted (2026-2029, NOT today): {CONTRACTED[f.name]}")
    print(f"\nIndustry reference: ~{pct(INDUSTRY_INFERENCE_SHARE)} of AI compute is now inference.")
    print(f"\nSanity check: 1 GW of IT power ~= {sanity_check_power(1):,.0f} H100-class chips "
          f"(at {KW_PER_CHIP_ALLIN} kW/chip all-in).")
    oa_chips = physical_chips(openai.h100eq_base)
    oa_gw = oa_chips / CHIPS_PER_GW
    print(f"  => OpenAI's {fmt_m(openai.h100eq_base)} H100-eq is ~{fmt_m(oa_chips)} physical accelerators "
          f"(GB200 counts ~3x/chip),")
    print(f"     i.e. ~{oa_gw:.1f} GW of operational power across ALL clouds "
          f"(Azure + Oracle + CoreWeave + Stargate)")
    print(f"     — Stargate/Abilene alone is ~0.3 GW live, ~1.2 GW projected Q4-2026.")


# ===========================================================================
# SLIDE 2 — Atlas Cloud margin on DeepSeek V4 Pro
# ===========================================================================
# Cost basis: one 8x NVIDIA H200 node serving the 1.6T-param / 49B-active MoE in
# FP4 (weights ~862 GB fit a single 8xH200 node = 1,128 GB). Input tokens are
# PREFILL (compute-bound, cheap, high throughput); output tokens are DECODE
# (memory-bandwidth-bound, expensive, low throughput). That asymmetry is why
# every provider prices output ~2x input.

ATLAS_PRICE_IN = 1.68     # $ / 1M input tokens (Atlas Cloud published price)
ATLAS_PRICE_OUT = 3.38    # $ / 1M output tokens

# Reference market prices (sources.md):
DEEPSEEK_PRICE = (0.435, 0.87)        # DeepSeek first-party API (the market floor)
PREMIUM_CLUSTER = (1.74, 3.48)        # DeepInfra / Fireworks / Novita premium tier


@dataclass
class Scenario:
    name: str
    gpu_hr: float            # $ per GPU-hour
    prefill_tok_s: float     # input tokens/s for the whole 8-GPU node
    decode_tok_s: float      # output tokens/s for the whole 8-GPU node
    util: float              # effective utilization (duty cycle x batching eff.)

    NODE_GPUS = 8

    def node_hr(self):
        return self.gpu_hr * self.NODE_GPUS

    def cost_in(self):
        """$ per 1M input tokens."""
        eff_tok_per_hr = self.prefill_tok_s * 3600 * self.util
        return self.node_hr() / (eff_tok_per_hr / 1e6)

    def cost_out(self):
        """$ per 1M output tokens."""
        eff_tok_per_hr = self.decode_tok_s * 3600 * self.util
        return self.node_hr() / (eff_tok_per_hr / 1e6)


# efficient / base / conservative (pessimistic) bundles
SCENARIOS = [
    Scenario("efficient",     gpu_hr=1.50, prefill_tok_s=180_000, decode_tok_s=35_000, util=0.65),
    Scenario("base",          gpu_hr=3.00, prefill_tok_s=110_000, decode_tok_s=22_000, util=0.50),
    Scenario("conservative",  gpu_hr=6.00, prefill_tok_s=60_000,  decode_tok_s=12_000, util=0.35),
]


def margin(price, cost):
    return (price - cost) / price


def blended(price_in, price_out, cost_in, cost_out, in_share):
    """Blended margin for a workload that is `in_share` input tokens by volume."""
    out_share = 1 - in_share
    rev = price_in * in_share + price_out * out_share
    cost = cost_in * in_share + cost_out * out_share
    return rev, cost, (rev - cost) / rev


def slide2():
    print("\n" + "=" * 70)
    print("SLIDE 2 — Atlas Cloud margin on DeepSeek V4 Pro")
    print("=" * 70)
    print(f"Atlas price: ${ATLAS_PRICE_IN}/M in, ${ATLAS_PRICE_OUT}/M out")
    print(f"Market floor (DeepSeek 1st-party): ${DEEPSEEK_PRICE[0]}/${DEEPSEEK_PRICE[1]} "
          f"-> Atlas is {ATLAS_PRICE_IN/DEEPSEEK_PRICE[0]:.1f}x the floor")
    print(f"Premium cluster (DeepInfra/Fireworks/Novita): "
          f"${PREMIUM_CLUSTER[0]}/${PREMIUM_CLUSTER[1]} -> Atlas undercuts by "
          f"{(1-ATLAS_PRICE_OUT/PREMIUM_CLUSTER[1])*100:.0f}%")
    print("\nCost to serve (8x H200 node) and gross margin vs Atlas price:")
    print(f"{'scenario':<14}{'$/M in':>9}{'$/M out':>9}{'margin in':>11}{'margin out':>12}")
    for s in SCENARIOS:
        ci, co = s.cost_in(), s.cost_out()
        print(f"{s.name:<14}{ci:>9.3f}{co:>9.3f}"
              f"{pct(margin(ATLAS_PRICE_IN, ci)):>11}{pct(margin(ATLAS_PRICE_OUT, co)):>12}")

    base = SCENARIOS[1]
    ci, co = base.cost_in(), base.cost_out()
    print("\nBase-case detail:")
    print(f"  node $/hr = 8 x ${base.gpu_hr} = ${base.node_hr():.0f}")
    print(f"  cost/M input  = ${ci:.3f}  -> margin {pct(margin(ATLAS_PRICE_IN, ci))}")
    print(f"  cost/M output = ${co:.3f}  -> margin {pct(margin(ATLAS_PRICE_OUT, co))}")
    print(f"  output costs {co/ci:.1f}x input to serve, but is priced only "
          f"{ATLAS_PRICE_OUT/ATLAS_PRICE_IN:.1f}x -> output is the squeezed resource.")

    print("\nBlended gross margin at different traffic mixes (base case):")
    for in_share, label in [(0.8, "input-heavy 4:1"), (0.5, "balanced 1:1"),
                            (0.25, "output-heavy 1:3 (reasoning)")]:
        rev, cost, m = blended(ATLAS_PRICE_IN, ATLAS_PRICE_OUT, ci, co, in_share)
        print(f"  {label:<28} margin {pct(m)}  (rev ${rev:.2f} vs cost ${cost:.2f} per 1M tokens)")

    cons = SCENARIOS[2]
    ci_c, co_c = cons.cost_in(), cons.cost_out()
    print("\nSame mixes under the PESSIMISTIC cost basis (stress test, single-node penalty):")
    for in_share, label in [(0.8, "input-heavy 4:1"), (0.5, "balanced 1:1"),
                            (0.25, "output-heavy 1:3 (reasoning)")]:
        rev, cost, m = blended(ATLAS_PRICE_IN, ATLAS_PRICE_OUT, ci_c, co_c, in_share)
        print(f"  {label:<28} margin {pct(m)}  (rev ${rev:.2f} vs cost ${cost:.2f} per 1M tokens)")

    print("\nVerdict: positive gross margin on compute in EVERY scenario. Base case ~80-90%;")
    print("in the pessimistic case the blended margin stays positive but output alone")
    print(f"narrows to {pct(margin(ATLAS_PRICE_OUT, co_c))} (decode is the binding constraint).")
    print("Caveat: this is GROSS margin on marginal compute only — excludes idle")
    print("capacity, free tier, networking/egress, support and R&D.")


# ===========================================================================
# SLIDE 2 — Bottom-up TCO: build the node cost from first principles
# ===========================================================================
# The base case above uses a market GPU rental rate ($3/GPU-hr) as the cost
# basis. That rate is already a *fully loaded* price: it embeds datacenter,
# power, cooling, networking, hardware amortization AND the lessor's margin.
# Here we instead OWN the hardware and add every line item explicitly, to show
# that (a) hardware amortization dominates (~70%), power is small (~5-8%), and
# (b) the owned-TCO cost lands at or below the rental proxy -> the rental-based
# margin is, if anything, conservative.
#
# The ~76% hardware / ~5% power split printed below is DERIVED from the base-case
# line items here (not an external stat). Its structure is corroborated by
# independent TCO models: Introl (hardware depreciation ~8x electricity;
# https://introl.com/blog/gpu-infrastructure-tco-5-year-cost-model) and the
# SemiAnalysis AI Cloud TCO Model (https://semianalysis.com/ai-cloud-tco-model/).


@dataclass
class NodeTCO:
    """All-in cost per wall-clock hour of OWNING and OPERATING one 8xH200 node.

    Charged per wall-clock hour the node exists (capex/DC/staff are fixed even
    when idle); power is charged at facility load. Utilization is applied later
    in the per-token formula (effective tokens = throughput * 3600 * util)."""
    name: str
    gpu_price: float          # $ per H200
    node_overhead_capex: float  # server, CPU, RAM, NVSwitch, NICs, NVMe ($)
    life_years: float         # depreciation horizon
    node_kw_it: float         # IT power drawn by the 8-GPU node (kW)
    pue: float                # facility overhead multiplier
    elec_usd_kwh: float       # electricity price
    datacenter_hr: float      # colo space + cooling capex + networking, $/hr
    staff_hr: float           # devops/SRE/software/ops, amortized per node, $/hr

    GPUS = 8
    HOURS_PER_YEAR = 8760

    def node_capex(self):
        return self.GPUS * self.gpu_price + self.node_overhead_capex

    def hardware_hr(self):
        return self.node_capex() / (self.life_years * self.HOURS_PER_YEAR)

    def power_hr(self):
        return self.node_kw_it * self.pue * self.elec_usd_kwh

    def node_hr(self):
        return self.hardware_hr() + self.power_hr() + self.datacenter_hr + self.staff_hr

    def breakdown(self):
        return {
            "hardware amort": self.hardware_hr(),
            "power+cooling": self.power_hr(),
            "datacenter+net": self.datacenter_hr,
            "staff+ops": self.staff_hr,
        }


# low / base / high owned-TCO bundles (see sources.md, "Bottom-up TCO")
TCO = [
    NodeTCO("TCO-low",  gpu_price=28_000, node_overhead_capex=88_000,  life_years=5,
            node_kw_it=10, pue=1.20, elec_usd_kwh=0.05, datacenter_hr=1.0, staff_hr=0.75),
    NodeTCO("TCO-base", gpu_price=32_000, node_overhead_capex=120_000, life_years=3,
            node_kw_it=10, pue=1.25, elec_usd_kwh=0.08, datacenter_hr=2.0, staff_hr=1.5),
    NodeTCO("TCO-high", gpu_price=40_000, node_overhead_capex=120_000, life_years=3,
            node_kw_it=10, pue=1.30, elec_usd_kwh=0.12, datacenter_hr=3.5, staff_hr=2.5),
]


def cost_per_mtok(node_hr, tok_s, util):
    """$ per 1M tokens given an all-in node $/hr, a throughput and utilization."""
    return node_hr / (tok_s * 3600 * util / 1e6)


def slide2_tco():
    print("\n" + "=" * 70)
    print("SLIDE 2 (v2) — Bottom-up TCO for an owned 8x H200 node")
    print("=" * 70)

    # Use the SAME base-case throughput/utilization as the rental model so the
    # only thing that changes is the cost basis (rental proxy vs owned TCO).
    base = SCENARIOS[1]
    prefill, decode, util = base.prefill_tok_s, base.decode_tok_s, base.util

    print(f"{'TCO line ($/hr)':<18}{'low':>9}{'base':>9}{'high':>9}")
    keys = list(TCO[1].breakdown().keys())
    for k in keys:
        row = [t.breakdown()[k] for t in TCO]
        print(f"{k:<18}{row[0]:>9.2f}{row[1]:>9.2f}{row[2]:>9.2f}")
    totals = [t.node_hr() for t in TCO]
    print(f"{'NODE TOTAL $/hr':<18}{totals[0]:>9.2f}{totals[1]:>9.2f}{totals[2]:>9.2f}")
    print(f"{'= $/GPU-hr':<18}{totals[0]/8:>9.2f}{totals[1]/8:>9.2f}{totals[2]/8:>9.2f}")

    hw_share = TCO[1].hardware_hr() / TCO[1].node_hr()
    pw_share = TCO[1].power_hr() / TCO[1].node_hr()
    print(f"\nComposition (base): hardware amortization {pct(hw_share)}, "
          f"power+cooling only {pct(pw_share)}.")
    print("=> The chip capex dominates; electricity is a small slice. Adding")
    print("   power/DC/staff explicitly barely moves the number.")

    print("\nCost per 1M tokens by basis (same throughput, util 50%):")
    print(f"{'basis':<22}{'node $/hr':>11}{'$/M in':>9}{'$/M out':>9}"
          f"{'margin in':>11}{'margin out':>12}")
    rental_hr = base.node_hr()                 # $24 rental proxy
    rows = [("rental proxy ($3/GPU)", rental_hr)] + [(t.name, t.node_hr()) for t in TCO]
    for label, nh in rows:
        ci = cost_per_mtok(nh, prefill, util)
        co = cost_per_mtok(nh, decode, util)
        print(f"{label:<22}{nh:>11.2f}{ci:>9.3f}{co:>9.3f}"
              f"{pct(margin(ATLAS_PRICE_IN, ci)):>11}{pct(margin(ATLAS_PRICE_OUT, co)):>12}")

    tco_base_hr = TCO[1].node_hr()
    print(f"\nVerdict: owned TCO (base ~${tco_base_hr:.0f}/hr) sits BELOW the rental "
          f"proxy (${rental_hr:.0f}/hr),")
    print("so the rental-based margin is conservative. 'Atlas is profitable' holds")
    print("under both cost bases. What still sits OUTSIDE this COGS view: idle/unsold")
    print("capacity, free tier, egress, sales & marketing, support and R&D.")


if __name__ == "__main__":
    slide1()
    slide2()
    slide2_tco()
