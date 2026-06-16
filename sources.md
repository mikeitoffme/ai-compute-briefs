# Sources & assumptions

Research date: June 2026. 
Every assumption in `model.py` traces to a source below. Where sources disagree
or numbers are inferred, a low/base/high range is used instead of a point value.

---

## Slide 1 — OpenAI & Anthropic fleets

### OpenAI
- Altman: "well over 1 million GPUs" online by end-2025 — [x.com/sama](https://x.com/sama/status/1947057625780396512), [Tom's Hardware](https://www.tomshardware.com/tech-industry/sam-altman-teases-100-million-gpu-scale-for-openai-that-could-cost-usd3-trillion-chatgpt-maker-to-cross-well-over-1-million-by-end-of-year)
- **Epoch AI: ~1.1M H100-equivalents mid-2025 (90% CI 0.8–1.4M)** — the anchor for the operational estimate — [epoch.ai](https://epoch.ai/gradient-updates/how-many-digital-workers-could-openai-deploy)
- **Base build to May 2026 (~2.0M H100-eq):** Hopper-class legacy ~1.25M H100-eq (the mid-2025 anchor grown modestly) + ~0.25M GB200 coming online across Azure/Oracle/CoreWeave/Abilene (×3 → ~0.75M H100-eq). Low 1.4M / high 3.0M brackets the uncertainty. Consistent with Altman's "well over 1M GPUs" end-2025 plus three quarters of Blackwell ramp.
- **Train/inference: ~44% inference mid-2025** (rising) — [epoch.ai](https://epoch.ai/gradient-updates/how-many-digital-workers-could-openai-deploy); 2024 compute mostly experiments — [epoch.ai](https://epoch.ai/data-insights/openai-compute-spend)
- API throughput 6B+ tokens/min (DevDay, Oct 2025); ChatGPT 800M→900M WAU — [DevDay/Tibor Blaho](https://x.com/btibor91/status/1975285391373566414), [TechCrunch](https://techcrunch.com/2025/10/06/sam-altman-says-chatgpt-has-hit-800m-weekly-active-users/)
- Operational power today ~0.3 GW (Abilene live) → 1.2 GW projected Q4 2026 — [Epoch AI](https://epoch.ai/blog/openai-stargate-where-the-us-sites-stand)
- Contracted (2026–2029): NVIDIA 10 GW ("4–5M GPUs") — [NVIDIA](https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems); AMD 6 GW — [AMD IR](https://ir.amd.com/news-events/press-releases/detail/1260/); Broadcom 10 GW custom (inference) — [Broadcom IR](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10); Oracle 4.5 GW — [OpenAI](https://openai.com/index/stargate-advances-with-partnership-with-oracle/); Abilene 450k GB200 — [DCD](https://www.datacenterdynamics.com/en/news/openai-and-oracle-to-deploy-450000-gb200-gpus-at-stargate-abilene-data-center/)

### Anthropic
- Project Rainier ~500k Trainium2 operational; >1M Trainium2 by end-2026; ~1 GW Trainium2+3 by end-2026; up to 5 GW AWS — [aboutamazon](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster), [anthropic.com](https://www.anthropic.com/news/anthropic-amazon-compute)
- "currently use over one million Trainium2 chips to train and serve Claude" — [anthropic.com](https://www.anthropic.com/news/anthropic-amazon-compute)
- Google TPU: up to ~1M TPUs / >1 GW in 2026 — [Google press](https://www.googlecloudpresscorner.com/2025-10-23-Anthropic-to-Expand-Use-of-Google-Cloud-TPUs-and-Services), [CNBC](https://www.cnbc.com/2025/10/23/anthropic-google-cloud-deal-tpu.html); +~3.5 GW Google/Broadcom from 2027 — [Tom's Hardware](https://www.tomshardware.com/tech-industry/broadcom-expands-anthropic-deal-to-3-5gw-of-google-tpu-capacity-from-2027), [anthropic.com](https://www.anthropic.com/news/google-broadcom-partnership-compute)
- NVIDIA via Azure up to 1 GW + $30B — [Microsoft](https://blogs.microsoft.com/blog/2025/11/18/microsoft-nvidia-and-anthropic-announce-strategic-partnerships/); SpaceX Colossus >220k NVIDIA GPUs / >300 MW (36-month commitment, used for inference — fact-check: not a short lease) — [DCD](https://www.datacenterdynamics.com/en/news/anthropic-to-use-all-of-spacex-xais-colossus-1-data-center-compute/), [CNBC](https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html)
- Workload-by-cloud: "Google Cloud serves most of Anthropic's skyrocketing inference needs"; AWS = training backbone — [SemiAnalysis](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion)
- Revenue run-rate >$30B (from ~$9B end-2025) — [anthropic.com](https://www.anthropic.com/news/anthropic-amazon-compute)
- $100B+ AWS commitment — [anthropic.com](https://www.anthropic.com/news/anthropic-amazon-compute)

### Conversion factors
- Power: GB200 1,200 W, H100 700 W chip TDP; rack-level ~1.3–1.7 kW/GPU; hyperscale PUE 1.1–1.2 → **~1.5 kW/chip all-in (H100-class) ⇒ ~667k chips/GW** — [SemiAnalysis](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks), [Sunbird DCIM](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72), [Uptime/mgrid PUE](https://mgrid.org/2025/10/01/uptime-institute-data-center-pue-stagnation-2025-liquid-cooling/)
- **H100-eq vs physical chips (power cross-check):** H100-eq is a *performance* aggregate, not a chip count — a GB200 is ~3× an H100 per chip. Blended across Hopper legacy + GB200 ramp, ~1.3 H100-eq per physical accelerator, so ~2.0M H100-eq ⇒ ~1.5M physical chips ⇒ **~2–2.4 GW operational across all clouds** (Azure + Oracle + CoreWeave + Stargate). The 0.3 GW live / 1.2 GW projected-Q4-2026 figures are **Stargate/Abilene only**, not OpenAI's total footprint, so they are a lower bound on the multi-cloud total rather than a ceiling.
- H100-eq multipliers (conservative): H200 ~1.3×, GB200 ~3×, GB300 ~4.5×, TPU v6e ~1×, TPU v7 ~2.5×, Trainium2 ~0.7×, Trainium3 ~1.7× — [SemiAnalysis TPUv7](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the), [SemiAnalysis Trainium2](https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking), [NVIDIA GB200](https://developer.nvidia.com/blog/nvidia-gb200-nvl72-delivers-trillion-parameter-llm-training-and-real-time-inference/)
- Capex cross-check: ~$50B/GW all-in (~half GPUs), ~$60k/H100-class all-in → ~500k GPUs/GW — agrees with power method — [Orennia](https://orennia.com/insights/what-it-actually-costs-to-build-a-1-gw-data-center)
- Industry train/inference: **Barclays >70% inference by 2026** (solid forecast, ~4.5× training) — [Barclays](https://www.ib.barclays/our-insights/3-point-perspective/the-next-wave-of-AI-demand-and-adoption.html); **Jensen Huang: "the vast majority of our compute today is actually inference"** (NVIDIA Q4 FY2026 call, Feb 2026 — fact-check: he did NOT cite a specific "~70% of revenue"); McKinsey reports ">50% of DC spend is GPUs/networking" (a spend figure, not a clean inference-share) — [McKinsey](https://www.mckinsey.com/featured-insights/week-in-charts/the-future-of-ai-workloads)

---

## Slide 2 — Atlas Cloud / DeepSeek V4 Pro

### Model & pricing
- DeepSeek V4 Pro: 1.6T total MoE, ~49B active, 1M context, 384+1 experts (6 active), sparse/compressed attention (27% prefill FLOPs & 10% KV cache vs V3.2), open weights MIT — **preview released Apr 24 2026**  — [HF](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [DeepSeek API news](https://api-docs.deepseek.com/news/news260424), [TechCrunch](https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/)
- Atlas price $1.68/$3.38 — published on Atlas Cloud's public model page, and ~3% below the verified premium cluster $1.74/$3.48, so it is consistent with that tier — [atlascloud.ai/models](https://www.atlascloud.ai/models/deepseek-ai/deepseek-v4-pro)
- DeepSeek first-party API: $0.435 in / $0.87 out (after permanent 75% cut) — [Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v4-pro/providers), [Engadget](https://www.engadget.com/2180062/deepseek-permanently-reduces-the-price-of-its-flagship-v4-model-by-75-percent/)
- Premium-tier cluster $1.74/$3.48 (DeepInfra, Fireworks, Novita) — [Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v4-pro/providers), [DeepInfra](https://deepinfra.com/blog/deepseek-v4-pro-pricing-guide-2026-providers-cost-analysis)

### Serving config & throughput
- Single 8×H200 node (1,128 GB) holds the ~862 GB FP4 checkpoint; FP4 experts + FP8 attention — [vLLM recipe](https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro), [codersera](https://codersera.com/blog/deepseek-v4-vram-gpu-requirements-2026/)
  - **Memory-headroom caveat:** ~862 GB of weights in 1,128 GB leaves ~266 GB for KV-cache + activations. At full 1M context that bounds the batch size and therefore decode throughput on a *single* node. Most production traffic runs well below 1M context, but the high-throughput base/efficient figures implicitly assume either short-to-moderate contexts or a disaggregated (multi-node) decode tier; the conservative case stress-tests the single-node-constrained regime.
- DeepSeek V3/R1 production (official): ~73.7k input tok/s & ~14.8k output tok/s **per 8-GPU node** on H800; disclosed 545% theoretical cost/profit margin (their model assumes ~$2/GPU-hr rental) — [DeepSeek Open Infra Day 6](https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md)
  - **Scope of this source:** it is a *throughput anchor* for a **different model (V3/R1 on H800)**, scaled to V4 Pro on H200 for the per-token cost. It does **NOT** back the $19/hr node TCO (that is the independent NodeTCO bottom-up below) nor the $24/hr rental (that is the $3/GPU-hr market rate). Its own ~$2/GPU-hr only corroborates the low end of our rental range.
  - **EP-scale caveat:** DeepSeek's figures come from a large *disaggregated* deployment (prefill and decode run across many nodes with wide expert parallelism). A single 8×H200 node loses that EP efficiency, so its per-GPU throughput is lower than the cluster average — another reason the conservative scenario, not the base, represents the true single-node floor.
- LMSYS GB200 NVL72 (V3.2-class): 26,156 prefill & 13,386 decode **tok/s/GPU** — used only as an upper-bound sanity anchor: NVL72 is a 72-GPU NVLink domain whose interconnect is *why* decode scales there, so it is **not** like-for-like with an 8×H200 node and is not used to set the base throughput — [LMSYS](https://www.lmsys.org/blog/2025-09-25-gb200-part-2/)
- GPU rental mid-2026: H200 ~$2.60 (cheap) / ~$3.95 (median) / ~$6 (premium), spot ~$1.5–2 — [GMI](https://www.gmicloud.ai/en/blog/h200-gpu-provider-pricing), [Spheron](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)

### Cost-model assumptions (8×H200 node)
| Scenario | $/GPU-hr | prefill tok/s/node | decode tok/s/node | utilization |
|---|---|---|---|---|
| efficient | 1.50 | 180,000 | 35,000 | 0.65 |
| base | 3.00 | 110,000 | 22,000 | 0.50 |
| conservative | 6.00 | 60,000 | 12,000 | 0.35 |

Throughput for V4 Pro specifically is extrapolated from DeepSeek's own V3/R1 node
figures and LMSYS GB200 measurements, adjusted for V4's lower prefill FLOPs / KV
cache. Output (decode) is the swing variable; the conservative case stress-tests
it. Conclusion (positive gross margin) holds across the full range.

### Bottom-up TCO — owned 8×H200 node, $/hr built from line items
The market rental rate ($3/GPU-hr) is a *loaded* proxy (it already contains DC,
power, cooling, networking, hardware amortization + lessor margin). Rebuilds
the cost from first principles and confirms the two methods bracket each other.

| Line item | low | base | high | basis / source |
|---|---|---|---|---|
| H200 price, $/GPU | 28,000 | 32,000 | 40,000 | bare-GPU $25–40k — [IntuitionLabs](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide), [CloudZero](https://www.cloudzero.com/blog/h100-gpu-cost/) |
| node overhead capex, $ | 88,000 | 120,000 | 120,000 | server/CPU/RAM/NVSwitch/NICs/NVMe; 8-GPU server $300–500k total — [Orennia](https://orennia.com/insights/what-it-actually-costs-to-build-a-1-gw-data-center) |
| depreciation, years | 5 | 3 | 3 | AI hardware useful life 3–5 yr |
| node IT power, kW | 10 | 10 | 10 | 8×H200 ~700 W + host ≈ 10 kW — [SemiAnalysis](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) |
| PUE | 1.20 | 1.25 | 1.30 | hyperscale 1.1–1.2; conservative — [Uptime/mgrid](https://mgrid.org/2025/10/01/uptime-institute-data-center-pue-stagnation-2025-liquid-cooling/) |
| electricity, $/kWh | 0.05 | 0.08 | 0.12 | US industrial/wholesale band |
| datacenter + network, $/hr | 1.0 | 2.0 | 3.5 | colo space + cooling capex + networking |
| staff + ops, $/hr | 0.75 | 1.5 | 2.5 | devops/SRE/software amortized over a large fleet |

Result: node TCO ≈ **$9 / $19 / $24 per hour** (low/base/high) = **$1.2 / $2.4 / $3.0
per GPU-hr**, vs the $3/GPU-hr rental proxy. The owned-TCO base sits *below* the rental
proxy, so the rental-based margin is conservative.

**Provenance of the "~76% hardware / ~5% power" split:** this is a
**derived figure**, computed from the NodeTCO base case above (hardware $14.31/hr ÷
$18.81/hr = 76%; power+cooling $1.00/hr ÷ $18.81/hr = 5%) — not an external statistic.
Denominator is node-level (hardware+power+DC+staff), which is why hardware's share is
higher than in "full" datacenter TCO. The **structure is corroborated by independent
TCO models**:
- [Introl — GPU Infrastructure 5-Year TCO](https://introl.com/blog/gpu-infrastructure-tco-5-year-cost-model): hardware depreciation **$1.69/GPU-hr vs electricity $0.21/GPU-hr ⇒ hardware ≈ 8× power**; over a full 3-yr TCO, hardware 35–50%, electricity 10–20%, networking/space/staff the rest.
- [SemiAnalysis — AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/): same hierarchy — depreciation dominates, power a minority share.

So the directional claim (chip amortization dominates; electricity is a small slice,
~8× smaller than hardware) is well-supported; the exact ~5% is our base assumption
(power runs ~5–15% depending on electricity price and how much overhead is loaded into
the denominator).

## Slide 2 — Alice / YandexGPT comparison (slide reference)
Used on the slide to anchor the Atlas/DeepSeek benchmark to a comparable company.

- **Alice AI inference scale:** ~**2.9B LLM ("Нейро") queries in 2025**; **~47.3M MAU** (Sept 2025) — [Yandex year-end (Habr)](https://habr.com/ru/news/982724/), [Yandex Q3 2025](https://yandex.ru/company/news/29-10-2025).
- **YandexGPT 5.1 Pro API price:** **~0.80 RUB / 1k tokens** (flat, ~$11 / 1M) — current best-supported figure as of Jun 2026 — [toolarium](https://toolarium.ru/yandexgpt-obzor-vozmozhnosti/), [mysummit](https://mysummit.school/blog/en/yandexgpt-review-2026/). The **0.40 RUB/1k** quoted at the Aug-2025 launch was a promo and is now stale; one source reports a higher 2/6 RUB in/out tier, so 0.80 is the central estimate (Yandex AI Studio billing console is the authority).
- **GigaChat 2 (Sber) API price (RF benchmark):** Lite **0.065** / Pro **0.5** / Max **0.65** RUB per 1k tokens (flat, sync) ⇒ ~$0.9 / $6.9 / $9.0 per 1M — [developers.sber.ru tariffs](https://developers.sber.ru/docs/ru/gigachat/tariffs/legal-tariffs) (eff. 1 Feb 2026).
- **USD conversion:** 0.80 RUB/1k × 1000 = 800 RUB / 1M ÷ **USD/RUB 72.14** (CBR, 17 Jun 2026) = **≈ $11 / 1M tokens** — [CBR](https://www.cbr.ru/currency_base/daily/), [TradingEconomics RUB](https://tradingeconomics.com/russia/currency).
- **Caveats:** (a) the YandexGPT/GigaChat figures are flat per-1k *prices*, not split input/output; (b) YandexGPT 5.1 Pro is ~32B dense (built on Qwen-2.5-32B-base) vs DeepSeek V4 Pro 1.6T MoE — **different model class**, so the comparison is on price/scale, not like-for-like; (c) **GPU fleet is NOT used** for the price comparison — Yandex's cloud/GPU business spun off into **Nebius** (separate company); only the **~3,776-A100** public supercomputers (Chervonenkis/Galushkin/Lyapunov, 2021) are documented, so we compare demand scale and per-token price only.
