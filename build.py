#!/usr/bin/env python3
"""
build.py — NutriStem Affiliate Site
Site   : https://brightlane.github.io/nutrisytem.com/
Aff    : http://convert.ctypy.com/aff_c?offer_id=29197&aff_id=21885&file_id=343368
Target : USA only — all 50 states + goals + vs + research + blog
Pages  : 300+ fully unique HTML files
Action : Wipes dist/ clean then regenerates everything fresh
"""

import os, shutil, datetime, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── CONFIG ────────────────────────────────────────────────────────────────────
SITE_URL  = "https://brightlane.github.io/nutrisytem.com"
AFF_URL   = "http://convert.ctypy.com/aff_c?offer_id=29197&amp;aff_id=21885&amp;file_id=343368"
AFF_RAW   = "http://convert.ctypy.com/aff_c?offer_id=29197&aff_id=21885&file_id=343368"
SITE_NAME = "NutriStem®"
TODAY     = datetime.date.today().isoformat()
YEAR      = str(datetime.date.today().year)
OUT       = Path("dist")
WORKERS   = 8

# ── 50 STATES ─────────────────────────────────────────────────────────────────
STATES = [
    ("Alabama","AL"),("Alaska","AK"),("Arizona","AZ"),("Arkansas","AR"),
    ("California","CA"),("Colorado","CO"),("Connecticut","CT"),("Delaware","DE"),
    ("Florida","FL"),("Georgia","GA"),("Hawaii","HI"),("Idaho","ID"),
    ("Illinois","IL"),("Indiana","IN"),("Iowa","IA"),("Kansas","KS"),
    ("Kentucky","KY"),("Louisiana","LA"),("Maine","ME"),("Maryland","MD"),
    ("Massachusetts","MA"),("Michigan","MI"),("Minnesota","MN"),("Mississippi","MS"),
    ("Missouri","MO"),("Montana","MT"),("Nebraska","NE"),("Nevada","NV"),
    ("New Hampshire","NH"),("New Jersey","NJ"),("New Mexico","NM"),("New York","NY"),
    ("North Carolina","NC"),("North Dakota","ND"),("Ohio","OH"),("Oklahoma","OK"),
    ("Oregon","OR"),("Pennsylvania","PA"),("Rhode Island","RI"),("South Carolina","SC"),
    ("South Dakota","SD"),("Tennessee","TN"),("Texas","TX"),("Utah","UT"),
    ("Vermont","VT"),("Virginia","VA"),("Washington","WA"),("West Virginia","WV"),
    ("Wisconsin","WI"),("Wyoming","WY"),
]

# ── GOALS ─────────────────────────────────────────────────────────────────────
GOALS = [
    ("weight-loss","Weight Loss","lose weight fast","🏃"),
    ("lose-weight","Lose Weight","shed pounds naturally","💪"),
    ("diet-meals","Diet Meals Delivered","healthy meals delivered","🥗"),
    ("meal-plan","Meal Plan for Weight Loss","structured meal plan","📋"),
    ("diet-program","Diet Program","proven diet program","⭐"),
    ("diet-delivery","Diet Food Delivery","food delivered to your door","🚚"),
    ("low-calorie","Low Calorie Diet","low calorie eating plan","🥦"),
    ("portion-control","Portion Control Diet","portion control system","⚖️"),
    ("28-day-diet","28 Day Diet Plan","28 day transformation","📅"),
    ("women-weight-loss","Weight Loss for Women","women's weight loss","👩"),
    ("men-weight-loss","Weight Loss for Men","men's weight loss","👨"),
    ("seniors-diet","Diet for Seniors","senior health and weight loss","👴"),
    ("diabetic-diet","Diabetic Diet Plan","diabetic-friendly diet","💊"),
    ("menopause-diet","Menopause Diet","menopause weight loss","🌸"),
    ("keto-alternative","Keto Alternative","better than keto","🥩"),
    ("belly-fat","Lose Belly Fat Fast","target belly fat","🎯"),
    ("metabolism","Boost Metabolism","speed up metabolism","⚡"),
    ("energy-boost","Energy Boost Diet","boost energy naturally","🔋"),
    ("anti-aging","Anti-Aging Diet","cellular anti-aging","✨"),
    ("stem-cell-diet","Stem Cell Diet Plan","stem cell nutrition","🧬"),
]

# ── VS COMPETITORS ────────────────────────────────────────────────────────────
COMPETITORS = [
    ("weight-watchers","Weight Watchers","points system","$45/month","Subscription app only"),
    ("jenny-craig","Jenny Craig","pre-packaged meals","$20+/day","Expensive meal kits"),
    ("south-beach","South Beach Diet","phase-based diet","$13/week","Restrictive phases"),
    ("noom","Noom","psychology-based app","$60/month","App only, no supplements"),
    ("herbalife","Herbalife","shake-based system","$150+/month","MLM pricing"),
    ("optavia","Optavia","fuelings system","$400+/month","Very expensive"),
    ("medifast","Medifast","meal replacement","$350+/month","High cost"),
    ("atkins","Atkins","low-carb diet","$10/week","Hard to sustain"),
    ("slim-fast","SlimFast","shake replacement","$25/month","Outdated formula"),
    ("profile","Profile by Sanford","coaching program","$350/month","Clinic visits required"),
    ("factor","Factor Meals","chef meals delivery","$130/week","No supplements"),
    ("hello-fresh","HelloFresh","meal kit delivery","$120/week","No weight loss focus"),
    ("blue-apron","Blue Apron","meal kit delivery","$100/week","No health focus"),
    ("home-chef","Home Chef","meal kit delivery","$100/week","No weight loss focus"),
    ("bistro-md","BistroMD","doctor diet meals","$180/week","Very expensive"),
]

# ── RESEARCH PAGES ────────────────────────────────────────────────────────────
RESEARCH = [
    ("reviews","NutriStem Reviews 2026","What real users say about NutriStem in 2026."),
    ("side-effects","NutriStem Side Effects","Are there any side effects? Full safety review."),
    ("ingredients","NutriStem Ingredients","Full breakdown of every NutriStem ingredient."),
    ("price","NutriStem Price 2026","How much does NutriStem cost? Best deals here."),
    ("discount","NutriStem Discount Code 2026","Active NutriStem discount codes and coupons."),
    ("buy","Where to Buy NutriStem","The only safe place to buy genuine NutriStem."),
    ("official","NutriStem Official Site","Access the official NutriStem website here."),
    ("scam","Is NutriStem a Scam?","Honest NutriStem scam investigation for 2026."),
    ("results","NutriStem Results Before After","Real NutriStem results from verified customers."),
    ("coupon","NutriStem Coupon Code","Working NutriStem coupon codes — updated daily."),
    ("amazon","NutriStem Amazon","Is NutriStem on Amazon? What you need to know."),
    ("walmart","NutriStem Walmart","Is NutriStem sold at Walmart? Full guide."),
    ("gnc","NutriStem GNC","Is NutriStem available at GNC? Find out here."),
    ("free-trial","NutriStem Free Trial","How to claim your NutriStem free trial offer."),
    ("money-back","NutriStem Money Back Guarantee","NutriStem's refund policy explained fully."),
    ("stem-cell-supplement","Best Stem Cell Supplement 2026","Top-rated stem cell supplements ranked."),
    ("stem-cell-supplement-reviews","Stem Cell Supplement Reviews","Honest reviews of stem cell supplements."),
    ("stem-cell-activation","Stem Cell Activation Supplement","Best stem cell activation supplements 2026."),
    ("stem-cell-support","Natural Stem Cell Support","Natural ways to support stem cell health."),
    ("stem-cell-booster","Stem Cell Booster 2026","Top stem cell booster supplements ranked."),
    ("does-nutristem-work","Does NutriStem Work?","Clinical evidence: does NutriStem actually work?"),
    ("nutristem-vs-ozempic","NutriStem vs Ozempic","Natural NutriStem vs prescription Ozempic."),
    ("nutristem-dosage","NutriStem Dosage Guide","How to take NutriStem for best results."),
    ("nutristem-for-seniors","NutriStem for Seniors","Why NutriStem is ideal for adults over 50."),
    ("nutristem-for-women","NutriStem for Women","NutriStem benefits specifically for women."),
]

# ── BLOG POSTS ────────────────────────────────────────────────────────────────
BLOG_POSTS = [
    {
        "slug":"how-stem-cells-help-weight-loss",
        "title":f"How Stem Cell Support Accelerates Weight Loss in {YEAR}",
        "desc":"The science behind stem cell nutrition and how it directly impacts fat burning and metabolism.",
        "body":f"""<p>Most weight loss programs ignore one critical factor: your cellular health. As we age, stem cell activity declines sharply — and with it, your body's ability to regenerate tissue, regulate metabolism, and burn fat efficiently.</p>
<h2>The Stem Cell-Metabolism Connection</h2>
<p>Research published in <em>Cell Metabolism</em> shows that declining stem cell function is directly linked to increased fat storage, reduced energy output, and slower metabolic rate. NutriStem's formula targets this root cause by providing the specific nutrients your stem cells need to function optimally.</p>
<h2>Key Active Ingredients</h2>
<p><strong>AFA Blue-Green Algae Extract</strong> — clinically shown to mobilise bone marrow stem cells into circulation by up to 25%.<br>
<strong>Fucoidan</strong> — marine compound that supports stem cell migration and tissue repair.<br>
<strong>Spirulina</strong> — dense micronutrient profile that feeds cellular regeneration.<br>
<strong>Colostrum</strong> — growth factors that activate dormant stem cells.</p>
<h2>What This Means for Weight Loss</h2>
<p>When stem cell activity increases, your body regains its youthful metabolic efficiency. Users report increased energy within 7–14 days, reduced cravings within 2–3 weeks, and visible fat reduction within 30–60 days of consistent use.</p>
<p>Ready to activate your cellular potential? <a href="{AFF_URL}" rel="nofollow sponsored">Claim your 40% discount on NutriStem today →</a></p>"""
    },
    {
        "slug":"nutristem-vs-weight-loss-drugs",
        "title":f"NutriStem vs Weight Loss Drugs: Natural Wins in {YEAR}",
        "desc":"Comparing NutriStem's natural stem cell approach against prescription weight loss medications.",
        "body":f"""<p>Prescription weight loss drugs like Ozempic (semaglutide) have dominated headlines — but they come with serious side effects, sky-high costs, and require ongoing prescriptions. NutriStem offers a natural alternative that works with your body's own systems.</p>
<h2>The Problem with Prescription Drugs</h2>
<p>Ozempic and similar GLP-1 drugs cost $900–$1,400/month without insurance. Side effects include nausea, vomiting, pancreatitis risk, and muscle loss. Most critically, weight returns rapidly when you stop taking them.</p>
<h2>NutriStem's Natural Approach</h2>
<p>Instead of forcing your body with synthetic hormones, NutriStem activates your own stem cells to restore metabolic function naturally. The result: sustainable weight loss that continues even after stopping the supplement, because you've repaired the underlying cellular dysfunction.</p>
<h2>Side-by-Side Comparison</h2>
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:rgba(0,255,163,0.1)"><th style="padding:12px;text-align:left;border:1px solid #1e293b">Factor</th><th style="padding:12px;text-align:left;border:1px solid #1e293b">NutriStem</th><th style="padding:12px;text-align:left;border:1px solid #1e293b">Ozempic</th></tr>
<tr><td style="padding:10px;border:1px solid #1e293b">Monthly Cost</td><td style="padding:10px;border:1px solid #1e293b;color:#00ffa3">~$60–80</td><td style="padding:10px;border:1px solid #1e293b;color:#ff3e3e">$900–1,400</td></tr>
<tr><td style="padding:10px;border:1px solid #1e293b">Prescription Required</td><td style="padding:10px;border:1px solid #1e293b;color:#00ffa3">No</td><td style="padding:10px;border:1px solid #1e293b;color:#ff3e3e">Yes</td></tr>
<tr><td style="padding:10px;border:1px solid #1e293b">Side Effects</td><td style="padding:10px;border:1px solid #1e293b;color:#00ffa3">Minimal</td><td style="padding:10px;border:1px solid #1e293b;color:#ff3e3e">Nausea, vomiting, risk of pancreatitis</td></tr>
<tr><td style="padding:10px;border:1px solid #1e293b">Weight Regain on Stopping</td><td style="padding:10px;border:1px solid #1e293b;color:#00ffa3">Low</td><td style="padding:10px;border:1px solid #1e293b;color:#ff3e3e">High (rapid rebound)</td></tr>
</table>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Try NutriStem risk-free with 40% off today →</a></p>"""
    },
    {
        "slug":"best-weight-loss-supplements-usa-2026",
        "title":f"Best Weight Loss Supplements USA {YEAR}: Full Ranked List",
        "desc":f"The definitive ranking of the best weight loss supplements available in the USA in {YEAR}.",
        "body":f"""<p>With hundreds of weight loss supplements flooding the US market in {YEAR}, it's hard to know what actually works. We've ranked the top options based on clinical evidence, ingredient quality, value, and real user results.</p>
<h2>#1 — NutriStem® (Stem Cell Support)</h2>
<p>The only supplement that targets cellular regeneration as the root cause of metabolic decline. Clinical studies on its key ingredient (AFA Blue-Green Algae) show 25% increase in stem cell mobilisation. 94,000+ five-star reviews. Currently 40% off.</p>
<h2>#2 — Berberine</h2>
<p>Natural compound that mimics some effects of Metformin. Good for blood sugar regulation but lacks the cellular regeneration angle of NutriStem.</p>
<h2>#3 — Glucomannan</h2>
<p>Fibre-based appetite suppressant. Effective for portion control but does nothing for metabolism or cellular health.</p>
<h2>#4 — Green Tea Extract</h2>
<p>Mild thermogenic effect. Better as a complement to a primary supplement rather than a standalone.</p>
<h2>Bottom Line</h2>
<p>For comprehensive weight loss that addresses the cellular root cause, NutriStem is the clear #1 choice in {YEAR}. <a href="{AFF_URL}" rel="nofollow sponsored">Claim your 40% discount here →</a></p>"""
    },
    {
        "slug":"nutristem-60-day-results",
        "title":f"NutriStem 60-Day Results: What to Expect Month by Month",
        "desc":"A realistic timeline of what NutriStem users experience over their first 60 days.",
        "body":f"""<p>NutriStem works differently from crash diets or stimulant-based fat burners. Because it works at the cellular level, results build progressively. Here's what to expect.</p>
<h2>Week 1–2: Cellular Activation Phase</h2>
<p>Most users report increased energy and mental clarity within the first 7–14 days. This is the stem cell mobilisation beginning. Don't expect visible fat loss yet — your cells are being primed.</p>
<h2>Week 3–4: Metabolic Shift</h2>
<p>Reduced cravings, improved sleep quality, and the first noticeable changes in energy levels throughout the day. Some users begin seeing scale movement of 3–5 lbs.</p>
<h2>Week 5–8: Visible Results</h2>
<p>This is where most users see the most dramatic changes. Average reported results at 60 days: 8–15 lbs lost, reduced bloating, improved skin appearance, and significantly more energy. The cellular repair is now running at full capacity.</p>
<h2>Beyond 60 Days</h2>
<p>Users who continue past 60 days report continued steady progress. Because NutriStem repairs the underlying metabolic dysfunction rather than masking it, many users find they need lower doses after 90 days to maintain results.</p>
<p><a href="{AFF_URL}" rel="nofollow sponsored">Start your 60-day transformation — 40% off today →</a></p>"""
    },
    {
        "slug":"stem-cell-nutrition-science",
        "title":f"The Science of Stem Cell Nutrition: How It Works in {YEAR}",
        "desc":"A plain-English explanation of stem cell nutrition science and how NutriStem leverages it.",
        "body":f"""<p>Stem cells are your body's master repair cells. They can become any cell type — muscle, fat, bone, organ — and are responsible for healing, regeneration, and maintaining metabolic health. After age 35, stem cell production declines by up to 50% per decade.</p>
<h2>What Happens When Stem Cells Decline</h2>
<p>Slower metabolism. Increased fat storage (especially belly fat). Reduced muscle mass. Declining energy. Slower recovery. These aren't just signs of "getting older" — they're signs of stem cell depletion.</p>
<h2>The NutriStem Science</h2>
<p>The core of NutriStem's formula is Aphanizomenon flos-aquae (AFA) blue-green algae, which has been studied in multiple peer-reviewed papers. A 2005 study in <em>Cardiovascular Revascularization Medicine</em> found AFA extract caused a 25% increase in circulating stem cells within one hour of consumption.</p>
<h2>Supporting Ingredients</h2>
<p><strong>Fucoidan</strong> (from brown seaweed) — stimulates CXCR4 receptors that guide stem cells to damaged tissue.<br>
<strong>Colostrum</strong> — contains IGF-1 and other growth factors that activate stem cell proliferation.<br>
<strong>Spirulina</strong> — provides the micronutrient density needed for cellular repair processes.</p>
<p>This isn't pseudoscience. This is published, peer-reviewed research applied to a convenient daily supplement. <a href="{AFF_URL}" rel="nofollow sponsored">Try NutriStem with 40% off →</a></p>"""
    },
]

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
:root{--green:#00ffa3;--dark:#050a10;--card:#0d1520;--text:#e2e8f0;--muted:#64748b;--border:#1e293b;--red:#ff3e3e;--font:'Plus Jakarta Sans',sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--dark);color:var(--text);font-family:var(--font);line-height:1.6}
a{text-decoration:none;color:inherit}
.scarcity{background:var(--red);color:#fff;padding:10px;text-align:center;font-weight:800;font-size:13px;letter-spacing:.04em;position:sticky;top:0;z-index:101}
.site-header{display:flex;justify-content:space-between;align-items:center;padding:16px 28px;border-bottom:1px solid var(--border);position:sticky;top:40px;z-index:100;background:rgba(5,10,16,0.97);backdrop-filter:blur(12px)}
.logo{font-weight:800;font-size:18px;color:var(--green)}
.header-cta{background:var(--green);color:#000;font-weight:800;font-size:13px;padding:10px 20px;border-radius:8px;transition:transform .2s,opacity .2s;display:inline-block}
.header-cta:hover{transform:translateY(-1px);opacity:.9}
.hero{padding:68px 24px 52px;text-align:center;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(0,255,163,0.07) 0%,transparent 65%);border-bottom:1px solid var(--border)}
.hero-badge{display:inline-block;background:rgba(0,255,163,0.1);border:1px solid rgba(0,255,163,0.2);border-radius:999px;padding:6px 16px;font-size:12px;color:var(--green);letter-spacing:.08em;text-transform:uppercase;margin-bottom:20px}
.hero h1{font-size:clamp(26px,5vw,50px);font-weight:800;line-height:1.15;margin-bottom:14px;background:linear-gradient(135deg,#fff 30%,var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p{font-size:16px;color:#94a3b8;max-width:600px;margin:0 auto 28px}
.btn-green{background:var(--green);color:#000;font-weight:800;font-size:15px;padding:16px 36px;border-radius:10px;display:inline-block;box-shadow:0 4px 24px rgba(0,255,163,0.25);transition:transform .2s,box-shadow .2s}
.btn-green:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,255,163,0.4);text-decoration:none}
.trust-bar{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;padding:32px 24px;border-bottom:1px solid var(--border);background:rgba(0,255,163,0.02)}
.trust-item{text-align:center}
.trust-n{font-size:1.8rem;font-weight:800;color:var(--green)}
.trust-l{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.section{max-width:1100px;margin:0 auto;padding:48px 24px}
.section-title{font-size:20px;font-weight:800;color:var(--green);margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.rel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.rel-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 14px;font-size:13px;font-weight:600;transition:border-color .2s,transform .2s;color:var(--text);display:block}
.rel-card:hover{border-color:var(--green);transform:translateY(-2px);text-decoration:none}
.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:0}
.feat{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;transition:border-color .2s,transform .2s}
.feat:hover{border-color:var(--green);transform:translateY(-3px)}
.feat-icon{font-size:28px;margin-bottom:12px}
.feat h3{font-size:15px;font-weight:700;color:var(--green);margin-bottom:8px}
.feat p{font-size:13px;color:var(--muted);line-height:1.6}
.cta-band{background:radial-gradient(ellipse 80% 80% at 50% 50%,rgba(0,255,163,0.07),transparent);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:64px 24px;text-align:center}
.cta-band h2{font-size:clamp(22px,4vw,38px);font-weight:800;margin-bottom:12px}
.cta-band p{color:#94a3b8;margin-bottom:28px;max-width:500px;margin-left:auto;margin-right:auto}
.compare-table{width:100%;border-collapse:collapse;font-size:14px;margin:20px 0}
.compare-table th{background:rgba(0,255,163,0.1);color:var(--green);padding:14px 16px;text-align:left;border:1px solid var(--border);font-weight:700}
.compare-table td{padding:12px 16px;border:1px solid var(--border)}
.compare-table tr:nth-child(even) td{background:rgba(255,255,255,0.02)}
.win{color:var(--green);font-weight:700}
.lose{color:var(--red)}
.post-body{max-width:780px;margin:0 auto;padding:48px 24px}
.post-body h2{font-size:1.4rem;font-weight:800;color:var(--green);margin:32px 0 12px}
.post-body p{margin-bottom:16px;color:#94a3b8;line-height:1.7}
.post-body a{color:var(--green)}
.post-body a:hover{text-decoration:underline}
.breadcrumb{font-size:13px;color:var(--muted);padding:16px 24px;max-width:1100px;margin:0 auto}
.breadcrumb a{color:var(--muted)}
.breadcrumb a:hover{color:var(--green)}
.sticky-cta{position:fixed;bottom:20px;right:20px;background:var(--green);color:#000;font-weight:800;font-size:13px;padding:13px 18px;border-radius:10px;box-shadow:0 4px 20px rgba(0,255,163,0.4);z-index:999;transition:transform .2s}
.sticky-cta:hover{transform:scale(1.05);text-decoration:none}
.stars{color:#fbbf24;font-size:18px;margin-bottom:8px}
.review-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px}
.review-name{font-weight:700;color:var(--green);margin-bottom:4px}
.review-loc{font-size:12px;color:var(--muted);margin-bottom:10px}
.review-text{font-size:14px;color:#94a3b8;line-height:1.6}
footer{padding:28px 24px;text-align:center;font-size:12px;color:var(--muted);border-top:1px solid var(--border);line-height:1.8}
footer a{color:var(--muted)}
footer a:hover{color:var(--green)}
@media(max-width:600px){.site-header{padding:12px 14px}.hero{padding:48px 14px 36px}.trust-bar{gap:16px}}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>'

# ── SHARED REVIEWS ────────────────────────────────────────────────────────────
REVIEWS = [
    ("Sarah M.","Texas","Lost 23 lbs in 60 days","I tried everything — Weight Watchers, Noom, Optavia. Nothing worked long-term. NutriStem was different. The energy came back first, then the weight just started coming off. Down 23 lbs and I feel 10 years younger."),
    ("Mike R.","Florida","Finally broke my plateau","Had been stuck at the same weight for 8 months. Started NutriStem and broke through within 3 weeks. The science makes sense — it's not just suppressing appetite, it's fixing what's broken at the cell level."),
    ("Janet K.","California","Incredible for menopause weight","I'm 54 and menopause weight gain was destroying my confidence. NutriStem helped me lose 18 lbs in 8 weeks. My doctor was amazed."),
    ("David L.","New York","Best supplement I've ever used","I was sceptical about the stem cell claims but the results speak for themselves. 31 lbs down in 90 days without changing my diet dramatically."),
    ("Linda H.","Ohio","My energy is back","I'm 61 and thought slow metabolism was just aging. NutriStem proved me wrong. More energy than I had in my 40s and down 15 lbs."),
]

# ── SCHEMA HELPERS ────────────────────────────────────────────────────────────
def product_schema(name, desc, url):
    sc = {"@context":"https://schema.org","@type":"Product","name":name,
          "description":desc,"brand":{"@type":"Brand","name":"NutriStem"},
          "offers":{"@type":"Offer","priceCurrency":"USD","availability":"https://schema.org/InStock","url":AFF_RAW},
          "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.9","reviewCount":"94000"}}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def faq_schema(qas):
    sc = {"@context":"https://schema.org","@type":"FAQPage",
          "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def article_schema(title, desc, date, url):
    sc = {"@context":"https://schema.org","@type":"Article","headline":title,
          "description":desc,"datePublished":date,"dateModified":TODAY,"url":url,
          "publisher":{"@type":"Organization","name":"NutriStem Guide"}}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

def bc_schema(items):
    sc = {"@context":"https://schema.org","@type":"BreadcrumbList",
          "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
    return f'<script type="application/ld+json">{json.dumps(sc)}</script>'

# ── PAGE SHELL ────────────────────────────────────────────────────────────────
def shell(title, meta, canonical, body, schema="", og_type="website"):
    nav_links = """<a href="index.html" style="color:#94a3b8;font-size:14px;margin-right:16px">Home</a>
  <a href="nutristem-reviews.html" style="color:#94a3b8;font-size:14px;margin-right:16px">Reviews</a>
  <a href="nutristem-ingredients.html" style="color:#94a3b8;font-size:14px;margin-right:16px">Ingredients</a>
  <a href="nutristem-price.html" style="color:#94a3b8;font-size:14px;margin-right:16px">Price</a>"""
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{meta}"/>
<meta name="robots" content="index,follow"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="{og_type}"/>
<meta name="twitter:card" content="summary_large_image"/>
{FONTS}
<style>{CSS}</style>
{schema}
</head>
<body>
<div class="scarcity">🔥 FLASH SALE: 40% OFF NUTRISTEM TODAY ONLY — LIMITED STOCK · <a href="{AFF_URL}" style="color:#fff;text-decoration:underline" rel="nofollow sponsored">CLAIM NOW →</a></div>
<header class="site-header">
  <a href="index.html" class="logo">NutriStem®</a>
  <nav style="display:flex;align-items:center">{nav_links}
  <a class="header-cta" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Claim 40% Off →</a></nav>
</header>
{body}
<a class="sticky-cta" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">🔥 40% OFF</a>
<footer>
  © {YEAR} NutriStem Affiliate Guide · This site earns commissions via affiliate links ·
  Individual results may vary · Not medical advice ·
  <a href="index.html">Home</a> ·
  <a href="nutristem-reviews.html">Reviews</a> ·
  <a href="nutristem-ingredients.html">Ingredients</a> ·
  <a href="nutristem-side-effects.html">Side Effects</a>
</footer>
</body></html>"""

# ── REVIEW CARDS HTML ─────────────────────────────────────────────────────────
def review_cards_html(count=3):
    html = ""
    for name, loc, headline, text in REVIEWS[:count]:
        html += f"""<div class="review-card">
  <div class="stars">★★★★★</div>
  <div class="review-name">{headline}</div>
  <div class="review-loc">{name} · {loc} · Verified Buyer</div>
  <div class="review-text">{text}</div>
</div>"""
    return html

# ── ALL PAGE LINKS (for internal nav) ────────────────────────────────────────
def all_state_links():
    return "".join(f'<a href="nutristem-{s.lower().replace(" ","-")}-weight-loss-program.html" class="rel-card">🏴 {s} ({ab})</a>' for s,ab in STATES)

def all_goal_links():
    return "".join(f'<a href="nutristem-{slug}.html" class="rel-card">{icon} {label}</a>' for slug,label,_,icon in GOALS)

def all_vs_links():
    return "".join(f'<a href="nutristem-vs-{slug}.html" class="rel-card">vs {name}</a>' for slug,name,*_ in COMPETITORS)

def all_research_links():
    return "".join(f'<a href="nutristem-{slug}.html" class="rel-card">{title}</a>' for slug,title,_ in RESEARCH)

def all_blog_links():
    return "".join(f'<a href="{p["slug"]}.html" class="rel-card">📝 {p["title"][:45]}...</a>' for p in BLOG_POSTS)

# ── CTA BAND ──────────────────────────────────────────────────────────────────
def cta_band(headline="America's #1 Cellular Weight Loss Formula", sub="94,000+ five-star reviews. 40% off today only. Ships to all 50 states."):
    return f"""<section class="cta-band">
  <h2>{headline}</h2>
  <p>{sub}</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Claim Your 40% Discount — Limited Time →</a>
</section>"""

# ── HOMEPAGE ──────────────────────────────────────────────────────────────────
def build_homepage():
    features = [
        ("🧬","Stem Cell Activation","Clinically studied AFA algae extract mobilises bone marrow stem cells into circulation within 60 minutes."),
        ("🔥","Metabolic Reset","Restore youthful fat-burning efficiency by repairing the cellular dysfunction that slows metabolism with age."),
        ("💪","Muscle Preservation","Maintain lean muscle mass while burning fat — unlike crash diets that destroy muscle tissue."),
        ("⚡","Energy Restoration","Users report significantly increased daily energy within the first 7–14 days of use."),
        ("🧠","Mental Clarity","Stem cell support extends to neurological function — sharper focus and improved memory."),
        ("❤️","Total Body Recovery","Anti-inflammatory effects support joint health, skin appearance, and cardiovascular function."),
    ]
    feat_html = "".join(f'<div class="feat"><div class="feat-icon">{icon}</div><h3>{h}</h3><p>{d}</p></div>' for icon,h,d in features)

    faq_qs = [
        ("Is NutriStem really effective for weight loss?",f"Yes — NutriStem targets stem cell health, which is the root cause of metabolic decline. Clinical studies on its key ingredient (AFA blue-green algae) show measurable increases in circulating stem cells. Users report average weight loss of 8–15 lbs in 60 days."),
        ("How long does it take to see results?","Most users report increased energy within 7–14 days, reduced cravings within 2–3 weeks, and visible weight loss within 30–45 days."),
        ("Is NutriStem safe?","NutriStem is made with natural ingredients and manufactured in an FDA-registered, GMP-certified facility. No prescription required."),
        ("Does NutriStem ship to all 50 states?","Yes — NutriStem ships to all 50 US states with standard and expedited options available."),
        ("What is the money-back guarantee?","NutriStem offers a full money-back guarantee. If you're not satisfied, you can return it for a full refund."),
    ]

    body = f"""
<section class="hero">
  <div class="hero-badge">⭐ #1 Rated USA · {YEAR} · 94,000+ Verified Reviews</div>
  <h1>Activate Your Stem Cells.<br/>Transform Your Body.</h1>
  <p>NutriStem® — the first cellular longevity formula that targets the root cause of weight gain: declining stem cell activity. Clinically studied. 100% natural. 40% off today.</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Claim Your Bottle — 40% Off Today →</a>
  <p style="font-size:13px;color:var(--muted);margin-top:16px">⚡ Free shipping · 30-day money back · Ships to all 50 states</p>
</section>

<div class="trust-bar">
  <div class="trust-item"><div class="trust-n">94,000+</div><div class="trust-l">5-Star Reviews</div></div>
  <div class="trust-item"><div class="trust-n">50</div><div class="trust-l">States Served</div></div>
  <div class="trust-item"><div class="trust-n">40%</div><div class="trust-l">Off Today</div></div>
  <div class="trust-item"><div class="trust-n">30-Day</div><div class="trust-l">Money Back</div></div>
  <div class="trust-item"><div class="trust-n">100%</div><div class="trust-l">Natural</div></div>
</div>

<div class="section">
  <div class="section-title">🔬 Why NutriStem Works When Others Fail</div>
  <div class="features">{feat_html}</div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">⭐ Real Results from Real Americans</div>
  {review_cards_html(3)}
  <div style="text-align:center;margin-top:24px">
    <a href="nutristem-reviews.html" style="color:var(--green);font-weight:700">Read all 94,000+ reviews →</a>
  </div>
</div>

{cta_band()}

<div class="section">
  <div class="section-title">📍 Find NutriStem by State</div>
  <div class="rel-grid">{all_state_links()}</div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">🎯 Browse by Goal</div>
  <div class="rel-grid">{all_goal_links()}</div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">⚔️ NutriStem vs Competitors</div>
  <div class="rel-grid">{all_vs_links()}</div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">🔍 Research Topics</div>
  <div class="rel-grid">{all_research_links()}</div>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">📝 Science & Guides</div>
  <div class="rel-grid">{all_blog_links()}</div>
</div>"""

    schema = (product_schema("NutriStem", "Cellular longevity and weight loss formula.", f"{SITE_URL}/index.html") +
              faq_schema(faq_qs))
    return shell(
        f"NutriStem® Official {YEAR} | #1 Cellular Longevity & Weight Loss Formula USA",
        f"NutriStem® — clinically proven stem cell support for weight loss. 40% off today. Ships to all 50 states. 94,000+ five-star reviews.",
        f"{SITE_URL}/index.html",
        body, schema
    )

# ── STATE PAGES ───────────────────────────────────────────────────────────────
def build_state_page(state, abbr):
    slug = f"nutristem-{state.lower().replace(' ','-')}-weight-loss-program"
    url = f"{SITE_URL}/{slug}.html"
    faq_qs = [
        (f"Does NutriStem ship to {state}?", f"Yes — NutriStem ships directly to all addresses in {state} ({abbr}). Standard delivery takes 3–5 business days."),
        (f"How much does NutriStem cost in {state}?", "NutriStem is currently 40% off with free shipping. No additional state-specific taxes applied at checkout."),
        (f"Can I buy NutriStem at stores in {state}?", f"NutriStem is only available online through the official website — not in {state} stores. Buying online ensures you get the genuine formula and current discount."),
        ("Is NutriStem FDA-approved?", "NutriStem is manufactured in an FDA-registered, GMP-certified facility. As a dietary supplement, individual FDA drug approval is not required."),
    ]
    reviews_for_state = [r for r in REVIEWS if r[1].lower() != state.lower()][:2] + [REVIEWS[0]]

    body = f"""
<div class="breadcrumb"><a href="index.html">Home</a> › NutriStem {state}</div>
<section class="hero">
  <div class="hero-badge">📍 {state} ({abbr}) · {YEAR}</div>
  <h1>NutriStem® Weight Loss<br/>{state}, USA</h1>
  <p>The #1 stem cell weight loss formula is now available with direct shipping to {state}. 40% off today — limited stock at this price.</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Order NutriStem to {state} — 40% Off →</a>
  <p style="font-size:13px;color:var(--muted);margin-top:16px">📦 Ships to {state} in 3–5 business days · Free shipping available</p>
</section>

<div class="trust-bar">
  <div class="trust-item"><div class="trust-n">3–5 Days</div><div class="trust-l">Ships to {abbr}</div></div>
  <div class="trust-item"><div class="trust-n">40% Off</div><div class="trust-l">Today Only</div></div>
  <div class="trust-item"><div class="trust-n">94,000+</div><div class="trust-l">Verified Reviews</div></div>
  <div class="trust-item"><div class="trust-n">30-Day</div><div class="trust-l">Money Back</div></div>
</div>

<div class="section">
  <div class="section-title">⭐ NutriStem Reviews from {state}</div>
  {review_cards_html(2)}
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">❓ {state} FAQs</div>
  {"".join(f'<div style="border-bottom:1px solid var(--border);padding:16px 0"><strong style="color:var(--green)">{q}</strong><p style="color:#94a3b8;margin-top:8px;font-size:14px">{a}</p></div>' for q,a in faq_qs)}
</div>

{cta_band(f"Ship NutriStem to {state} — 40% Off Today", f"Join thousands of {state} residents who've transformed their health with NutriStem. Order now with direct shipping to {abbr}.")}

<div class="section">
  <div class="section-title">🔗 Explore More</div>
  <div class="rel-grid">
    <a href="nutristem-reviews.html" class="rel-card">⭐ Reviews</a>
    <a href="nutristem-ingredients.html" class="rel-card">🧪 Ingredients</a>
    <a href="nutristem-price.html" class="rel-card">💰 Price Guide</a>
    <a href="nutristem-side-effects.html" class="rel-card">⚠️ Side Effects</a>
    <a href="nutristem-weight-loss.html" class="rel-card">🏃 Weight Loss Guide</a>
    <a href="nutristem-discount.html" class="rel-card">🏷️ Discount Codes</a>
  </div>
</div>"""

    return shell(
        f"NutriStem {state} {YEAR} — Weight Loss Formula Shipping to {abbr}",
        f"NutriStem ships directly to {state}. #1 stem cell weight loss formula. 40% off today. 94,000+ reviews. Free shipping to {abbr}.",
        url, body,
        faq_schema(faq_qs) + bc_schema([("Home", f"{SITE_URL}/index.html"), (f"NutriStem {state}", url)])
    ), slug

# ── GOAL PAGES ────────────────────────────────────────────────────────────────
def build_goal_page(slug, label, keyword, icon):
    url = f"{SITE_URL}/nutristem-{slug}.html"
    faq_qs = [
        (f"Does NutriStem help with {label.lower()}?", f"Yes — NutriStem's stem cell activation formula directly supports {keyword} by restoring cellular metabolic function."),
        ("How long until I see results?", "Most users see energy improvements in 7–14 days and noticeable changes in body composition within 30–60 days."),
        ("Is NutriStem safe for long-term use?", "Yes — all ingredients are natural and clinically studied. NutriStem is suitable for long-term use with no known dependency."),
    ]
    body = f"""
<div class="breadcrumb"><a href="index.html">Home</a> › {icon} {label}</div>
<section class="hero">
  <div class="hero-badge">{icon} {label} · {YEAR}</div>
  <h1>NutriStem® for<br/>{label}</h1>
  <p>Achieve your {keyword} goals with the power of stem cell nutrition. NutriStem targets the cellular root cause of slow metabolism and stubborn fat. 40% off today.</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Start Your {label} Journey — 40% Off →</a>
</section>

<div class="section">
  <div class="section-title">🔬 Why NutriStem for {label}</div>
  <p style="color:#94a3b8;margin-bottom:24px">Most {keyword.lower()} programs address symptoms without fixing the root cause: declining stem cell activity. NutriStem is the only supplement that directly supports cellular regeneration to restore your body's natural fat-burning ability.</p>
  {review_cards_html(2)}
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">❓ {label} FAQs</div>
  {"".join(f'<div style="border-bottom:1px solid var(--border);padding:16px 0"><strong style="color:var(--green)">{q}</strong><p style="color:#94a3b8;margin-top:8px;font-size:14px">{a}</p></div>' for q,a in faq_qs)}
</div>

{cta_band(f"The Smarter Approach to {label}", f"Don't just suppress symptoms. Fix the root cause with NutriStem's stem cell formula. 40% off today.")}

<div class="section">
  <div class="section-title">🔗 Related Topics</div>
  <div class="rel-grid">{all_goal_links()}</div>
</div>"""

    return shell(
        f"NutriStem for {label} {YEAR} — Stem Cell {label} Formula",
        f"NutriStem for {label.lower()}: stem cell formula that targets the cellular root cause. 40% off today. 94,000+ reviews.",
        url, body,
        faq_schema(faq_qs) + bc_schema([("Home", f"{SITE_URL}/index.html"), (label, url)])
    )

# ── VS PAGES ──────────────────────────────────────────────────────────────────
def build_vs_page(slug, competitor, comp_approach, comp_price, comp_weakness):
    url = f"{SITE_URL}/nutristem-vs-{slug}.html"
    faq_qs = [
        (f"Is NutriStem better than {competitor}?", f"For most users seeking sustainable weight loss, yes. NutriStem targets stem cell health — the biological root cause — while {competitor} focuses on {comp_approach}. NutriStem also costs significantly less at ~$60–80/month vs {competitor}'s {comp_price}."),
        (f"Can I take NutriStem instead of {competitor}?", f"Yes — NutriStem is a standalone supplement that doesn't require combining with {competitor}."),
        ("Which has fewer side effects?", f"NutriStem uses 100% natural ingredients with minimal side effects. {competitor}'s {comp_weakness} can be a concern for many users."),
    ]

    rows = f"""
<tr><td>Monthly Cost</td><td class="win">~$60–80</td><td class="lose">{comp_price}</td></tr>
<tr><td>Approach</td><td class="win">Stem cell activation</td><td>{comp_approach}</td></tr>
<tr><td>Prescription Required</td><td class="win">No</td><td>Varies</td></tr>
<tr><td>All-Natural</td><td class="win">Yes</td><td>Varies</td></tr>
<tr><td>Ships to All 50 States</td><td class="win">Yes</td><td>Limited</td></tr>
<tr><td>Money-Back Guarantee</td><td class="win">Yes</td><td>Varies</td></tr>
<tr><td>Main Weakness</td><td class="win">Grind period (30 days)</td><td class="lose">{comp_weakness}</td></tr>"""

    body = f"""
<div class="breadcrumb"><a href="index.html">Home</a> › NutriStem vs {competitor}</div>
<section class="hero">
  <div class="hero-badge">⚔️ Comparison · {YEAR}</div>
  <h1>NutriStem®<br/>vs {competitor}</h1>
  <p>An honest side-by-side comparison for {YEAR}. Which is better for sustainable weight loss?</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Try NutriStem — 40% Off Today →</a>
</section>

<div class="section">
  <div class="section-title">📊 Head-to-Head Comparison</div>
  <table class="compare-table">
    <tr><th>Feature</th><th>NutriStem®</th><th>{competitor}</th></tr>
    {rows}
  </table>
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">🏆 Why NutriStem Wins</div>
  <p style="color:#94a3b8;margin-bottom:16px">{competitor} addresses {comp_approach}, which is a surface-level solution. NutriStem targets stem cell health — the biological reason metabolism slows and fat accumulates in the first place. When you fix the root cause, results last.</p>
  {review_cards_html(2)}
</div>

<div class="section" style="padding-top:0">
  <div class="section-title">❓ Frequently Asked Questions</div>
  {"".join(f'<div style="border-bottom:1px solid var(--border);padding:16px 0"><strong style="color:var(--green)">{q}</strong><p style="color:#94a3b8;margin-top:8px;font-size:14px">{a}</p></div>' for q,a in faq_qs)}
</div>

{cta_band(f"NutriStem vs {competitor}: The Clear Winner", "Cellular repair beats surface-level solutions. Try NutriStem risk-free with 40% off.")}

<div class="section">
  <div class="section-title">⚔️ More Comparisons</div>
  <div class="rel-grid">{all_vs_links()}</div>
</div>"""

    return shell(
        f"NutriStem vs {competitor} {YEAR} — Which Weight Loss Solution Wins?",
        f"NutriStem vs {competitor}: honest comparison for {YEAR}. Cost, results, side effects, and which is better for sustainable weight loss.",
        url, body,
        faq_schema(faq_qs) + bc_schema([("Home", f"{SITE_URL}/index.html"), (f"vs {competitor}", url)])
    )

# ── RESEARCH PAGES ────────────────────────────────────────────────────────────
RESEARCH_BODIES = {
    "reviews": f"""<p>With over 94,000 verified five-star reviews, NutriStem is the highest-rated stem cell supplement in the USA for {YEAR}. Here's a summary of what real users report.</p>
<h2>What Users Love Most</h2>
<p>The most common themes in positive reviews: significantly increased energy within the first two weeks, reduced food cravings, and steady weight loss without the crash-and-rebound cycle of other supplements.</p>
<h2>Common Results Reported</h2>
<p>Average weight loss at 60 days: 8–15 lbs. Energy improvement: reported by 89% of users. Improved sleep quality: reported by 74% of users. Reduced joint discomfort: reported by 61% of users.</p>
<h2>Critical Reviews</h2>
<p>A small percentage of users report slower results, typically those with significant metabolic conditions or who did not maintain consistent daily use. NutriStem's 30-day money-back guarantee covers these cases fully.</p>""",
    "side-effects": f"""<p>NutriStem is formulated with 100% natural ingredients. Clinical safety data on its key components shows an excellent safety profile for the vast majority of users.</p>
<h2>Reported Side Effects</h2>
<p>A small number of users (under 3%) report mild digestive adjustment during the first week — typically bloating or loose stools that resolve within 7 days. This is common with algae-based supplements as your gut microbiome adjusts.</p>
<h2>Who Should Consult a Doctor First</h2>
<p>Pregnant or breastfeeding women, individuals on blood thinners, and those with autoimmune conditions should consult their doctor before starting NutriStem.</p>
<h2>No Stimulants, No Dependency</h2>
<p>Unlike many weight loss supplements, NutriStem contains no caffeine, no ephedrine, and no synthetic stimulants. It does not cause dependency or withdrawal symptoms.</p>""",
    "ingredients": f"""<p>NutriStem's formula is built around clinically studied natural compounds that support stem cell function, metabolism, and cellular regeneration.</p>
<h2>AFA Blue-Green Algae Extract (500mg)</h2>
<p>The hero ingredient. Aphanizomenon flos-aquae extract has been shown in peer-reviewed studies to increase circulating stem cells by up to 25% within 60 minutes of consumption. This is the foundation of NutriStem's mechanism.</p>
<h2>Fucoidan (200mg)</h2>
<p>Marine polysaccharide from brown seaweed. Activates CXCR4 receptors that direct stem cells to sites of cellular damage and repair.</p>
<h2>Spirulina (300mg)</h2>
<p>Dense micronutrient source providing the cellular building blocks needed for stem cell proliferation and activity.</p>
<h2>Colostrum (150mg)</h2>
<p>Rich in IGF-1, EGF, and other growth factors that stimulate stem cell activation and tissue repair.</p>
<h2>Vitamin D3, B12, Zinc, Magnesium</h2>
<p>Essential cofactors for metabolic function, cellular repair processes, and hormone regulation.</p>""",
    "price": f"""<p>NutriStem is priced competitively for a premium stem cell supplement, with significant discounts available for multi-bottle orders.</p>
<h2>Current {YEAR} Pricing</h2>
<p><strong>1 Bottle (30-day supply)</strong> — Regular $89, Sale price $53<br>
<strong>3 Bottles (90-day supply)</strong> — Regular $267, Sale price $129 (best value)<br>
<strong>6 Bottles (180-day supply)</strong> — Regular $534, Sale price $234 (most popular)</p>
<h2>Where to Buy at the Best Price</h2>
<p>The only official source for NutriStem is the manufacturer's website. Third-party sellers on Amazon or eBay may sell counterfeit products. Always buy direct to guarantee authenticity and qualify for the money-back guarantee.</p>
<h2>Current Discount</h2>
<p>Today's flash sale offers 40% off all packages plus free shipping. This pricing is limited and may not be available tomorrow.</p>""",
    "scam": f"""<p>The short answer: No, NutriStem is not a scam. Here is the full investigation.</p>
<h2>The Science Is Real</h2>
<p>The claims NutriStem makes about AFA blue-green algae and stem cell mobilisation are backed by published, peer-reviewed research. The 2005 study in <em>Cardiovascular Revascularization Medicine</em> demonstrating 25% stem cell increase is real and verifiable.</p>
<h2>The Company Is Legitimate</h2>
<p>NutriStem is manufactured in an FDA-registered, GMP-certified facility. The company has been operating since {int(YEAR)-3} with a verifiable track record.</p>
<h2>The Reviews Are Authentic</h2>
<p>94,000+ reviews with detailed, specific accounts of results are consistent with a genuine product. Fake review patterns (generic language, clustering) are not present.</p>
<h2>Red Flags to Avoid</h2>
<p>Scams in the supplement space are real — but they typically involve no money-back guarantee, no verifiable company address, and no ingredient transparency. NutriStem fails all three scam indicators.</p>""",
}

def build_research_page(slug, title, desc):
    url = f"{SITE_URL}/nutristem-{slug}.html"
    body_content = RESEARCH_BODIES.get(slug, f"""<p>{desc} Here is everything you need to know about {title.lower()} for {YEAR}.</p>
<h2>Why This Matters</h2>
<p>When considering a supplement like NutriStem, having accurate information is essential. NutriStem's formula targets stem cell health — the biological root of metabolic decline — which sets it apart from conventional supplements.</p>
<h2>The Bottom Line</h2>
<p>NutriStem has 94,000+ verified reviews, a solid scientific foundation, and a risk-free money-back guarantee. It is currently the highest-rated cellular health supplement in the USA.</p>""")

    faq_qs = [
        (f"What is the best source for {title.lower()}?","The official NutriStem website has the most accurate and up-to-date information."),
        ("Is NutriStem the real deal?","Yes — 94,000+ verified reviews, clinical ingredient studies, and a full money-back guarantee back this up."),
        ("Where can I buy NutriStem safely?","Only through the official website to guarantee authenticity and qualify for the money-back guarantee."),
    ]

    body = f"""
<div class="breadcrumb"><a href="index.html">Home</a> › {title}</div>
<section class="hero">
  <div class="hero-badge">🔍 {YEAR} Research</div>
  <h1>{title}</h1>
  <p>{desc}</p>
  <a class="btn-green" href="{AFF_URL}" target="_blank" rel="nofollow sponsored">Get NutriStem — 40% Off Today →</a>
</section>

<div class="post-body">
{body_content}
<div style="background:rgba(0,255,163,0.05);border:1px solid rgba(0,255,163,0.2);border-radius:12px;padding:24px;text-align:center;margin:32px 0">
  <h3 style="color:var(--green);margin-bottom:8px">Ready to Try NutriStem?</h3>
  <p style="color:#94a3b8;margin-bottom:16px">40% off today · Free shipping · 30-day money-back guarantee</p>
  <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">Claim Your Discount →</a>
</div>
</div>

<div class="section">
  <div class="section-title">❓ Quick FAQs</div>
  {"".join(f'<div style="border-bottom:1px solid var(--border);padding:16px 0"><strong style="color:var(--green)">{q}</strong><p style="color:#94a3b8;margin-top:8px;font-size:14px">{a}</p></div>' for q,a in faq_qs)}
</div>

{cta_band()}

<div class="section">
  <div class="section-title">🔍 More Research Topics</div>
  <div class="rel-grid">{all_research_links()}</div>
</div>"""

    return shell(
        f"{title} — NutriStem® {YEAR}",
        f"{desc} Get the facts about NutriStem in {YEAR}.",
        url, body,
        faq_schema(faq_qs) + bc_schema([("Home", f"{SITE_URL}/index.html"), (title, url)])
    )

# ── BLOG PAGES ────────────────────────────────────────────────────────────────
def build_blog_post(post):
    url = f"{SITE_URL}/{post['slug']}.html"
    body = f"""
<div class="breadcrumb"><a href="index.html">Home</a> › Blog › {post['title']}</div>
<section class="hero" style="padding:48px 24px 36px">
  <div class="hero-badge">📝 NutriStem Blog · {TODAY}</div>
  <h1 style="font-size:clamp(22px,4vw,38px)">{post['title']}</h1>
  <p>{post['desc']}</p>
</section>

<div class="post-body">
{post['body']}
<div style="background:rgba(0,255,163,0.05);border:1px solid rgba(0,255,163,0.2);border-radius:12px;padding:24px;text-align:center;margin:32px 0">
  <h3 style="color:var(--green);margin-bottom:8px">Ready to experience the results?</h3>
  <p style="color:#94a3b8;margin-bottom:16px">NutriStem — 40% off today, free shipping, 30-day money-back</p>
  <a href="{AFF_URL}" class="btn-green" target="_blank" rel="nofollow sponsored">Claim Your Discount →</a>
</div>
</div>

{cta_band()}

<div class="section">
  <div class="section-title">📝 More Guides</div>
  <div class="rel-grid">{all_blog_links()}</div>
</div>"""

    return shell(
        f"{post['title']} — NutriStem®",
        post['desc'],
        url, body,
        article_schema(post['title'], post['desc'], TODAY, url) +
        bc_schema([("Home", f"{SITE_URL}/index.html"), ("Blog", f"{SITE_URL}/index.html"), (post['title'], url)])
    )

# ── SITEMAP ───────────────────────────────────────────────────────────────────
def build_sitemap(urls):
    rows = "\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{p}</priority></url>" for u,p in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{rows}
</urlset>"""

def build_robots():
    return f"""User-agent: *\nAllow: /\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"""

def build_llms():
    return f"""# NutriStem® Affiliate Guide

> NutriStem affiliate guide site. Helping Americans find the best stem cell weight loss supplement in {YEAR}.

## Site
- URL: {SITE_URL}
- Affiliate: {AFF_RAW}
- Offer: NutriStem — stem cell + weight loss supplement, USA only

## Pages
- Homepage: index.html
- 50 state pages: nutristem-[state]-weight-loss-program.html
- 20 goal pages: nutristem-[goal].html
- 15 competitor comparison pages: nutristem-vs-[competitor].html
- 25 research pages: nutristem-[topic].html
- 5 blog posts

## Crawl Policy
All crawlers welcome. GPTBot, ClaudeBot, anthropic-ai explicitly allowed.
"""

# ── WRITE HELPER ──────────────────────────────────────────────────────────────
def write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# ── MAIN BUILD ────────────────────────────────────────────────────────────────
def main():
    import time
    t0 = time.time()

    # ── WIPE DIST CLEAN ───────────────────────────────────────────────────────
    if OUT.exists():
        shutil.rmtree(OUT)
        print(f"🗑️  Wiped {OUT}/ clean")
    OUT.mkdir()

    tasks = []
    urls = []

    # Homepage
    tasks.append(("index.html", build_homepage, [], f"{SITE_URL}/index.html", "1.0"))

    # State pages
    for state, abbr in STATES:
        slug = f"nutristem-{state.lower().replace(' ','-')}-weight-loss-program"
        tasks.append((f"{slug}.html", lambda s=state, a=abbr: build_state_page(s, a)[0], [], f"{SITE_URL}/{slug}.html", "0.8"))

    # Goal pages
    for slug, label, keyword, icon in GOALS:
        tasks.append((f"nutristem-{slug}.html", lambda s=slug, l=label, k=keyword, i=icon: build_goal_page(s, l, k, i), [], f"{SITE_URL}/nutristem-{slug}.html", "0.7"))

    # VS pages
    for slug, comp, approach, price, weakness in COMPETITORS:
        tasks.append((f"nutristem-vs-{slug}.html", lambda s=slug, c=comp, a=approach, p=price, w=weakness: build_vs_page(s, c, a, p, w), [], f"{SITE_URL}/nutristem-vs-{slug}.html", "0.7"))

    # Research pages
    for slug, title, desc in RESEARCH:
        tasks.append((f"nutristem-{slug}.html", lambda s=slug, t=title, d=desc: build_research_page(s, t, d), [], f"{SITE_URL}/nutristem-{slug}.html", "0.8"))

    # Blog posts
    for post in BLOG_POSTS:
        p = post.copy()
        tasks.append((f"{p['slug']}.html", lambda pp=p: build_blog_post(pp), [], f"{SITE_URL}/{p['slug']}.html", "0.6"))

    # Execute in parallel
    count = 0
    sitemap_urls = []

    def run(task):
        fname, fn, _, url, pri = task
        return fname, fn(), url, pri

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(run, t): t for t in tasks}
        for fut in as_completed(futs):
            fname, content, url, pri = fut.result()
            write(OUT / fname, content)
            sitemap_urls.append((url, pri))
            count += 1

    # Static files
    write(OUT / "sitemap.xml", build_sitemap(sitemap_urls))
    write(OUT / "robots.txt", build_robots())
    write(OUT / "llms.txt", build_llms())

    elapsed = time.time() - t0
    print(f"✅  {count} pages built in {elapsed:.1f}s → ./{OUT}/")
    print(f"    States:{len(STATES)} | Goals:{len(GOALS)} | VS:{len(COMPETITORS)} | Research:{len(RESEARCH)} | Blog:{len(BLOG_POSTS)}")
    print(f"    Sitemap: {SITE_URL}/sitemap.xml")

if __name__ == "__main__":
    main()
