"""CineMatch visual system kept separate from application logic."""

APP_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
    --ink: #f7f5f1;
    --muted: #9a9ba7;
    --line: rgba(255, 255, 255, .09);
    --orange: #ff6846;
    --violet: #8b5cf6;
}

html { scroll-behavior: smooth; }
.stApp {
    background:
        radial-gradient(circle at 10% 12%, rgba(139, 92, 246, .17), transparent 27rem),
        radial-gradient(circle at 92% 8%, rgba(255, 104, 70, .14), transparent 25rem),
        #090a0f;
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}
.stApp::before {
    content: ''; position: fixed; inset: 0; pointer-events: none; opacity: .12;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.22'/%3E%3C/svg%3E");
}
[data-testid="stHeader"], #MainMenu, footer { display: none; }
.block-container { max-width: 1320px; padding: 1.1rem 2.5rem 4rem; }
h1, h2, h3, .brand { font-family: 'Manrope', sans-serif !important; }
p { color: var(--muted); }

.nav {
    display: flex; justify-content: space-between; align-items: center;
    padding: .45rem 0 1.35rem; border-bottom: 1px solid var(--line);
}
.brand { color: var(--ink); font-size: 1.1rem; font-weight: 800; letter-spacing: -.03em; }
.brand-mark {
    display: inline-grid; place-items: center; width: 30px; height: 30px;
    margin-right: .55rem; border-radius: 10px;
    background: linear-gradient(135deg, var(--orange), var(--violet));
    box-shadow: 0 7px 22px rgba(255, 104, 70, .25);
}
.nav-status { color: #babac3; font-size: .78rem; font-weight: 600; }
.status-dot {
    width: 7px; height: 7px; border-radius: 50%; display: inline-block;
    background: #42d392; margin-right: .42rem;
    box-shadow: 0 0 0 4px rgba(66, 211, 146, .1);
}

.hero { padding: 4.9rem 0 2rem; text-align: center; }
.eyebrow {
    display: inline-flex; color: #d6c7ff; font-size: .73rem; font-weight: 700;
    letter-spacing: .14em; text-transform: uppercase; background: rgba(139, 92, 246, .1);
    border: 1px solid rgba(177, 142, 255, .2); padding: .52rem .8rem; border-radius: 999px;
}
.hero h1 {
    max-width: 900px; margin: 1.25rem auto .95rem; color: var(--ink);
    font-size: clamp(3rem, 6.6vw, 6.2rem); line-height: .96;
    letter-spacing: -.075em; font-weight: 800;
}
.hero h1 em {
    font-style: normal; color: transparent;
    background: linear-gradient(100deg, #ff7a59, #ad8cff 62%, #67e8f9);
    background-clip: text; -webkit-background-clip: text;
}
.hero > p { max-width: 690px; margin: 0 auto; font-size: 1.05rem; line-height: 1.7; }

[data-testid="stVerticalBlockBorderWrapper"] {
    max-width: 1050px; margin: 1.15rem auto .8rem; padding: 1rem;
    border: 1px solid var(--line); border-radius: 22px;
    background: rgba(21, 22, 30, .8); backdrop-filter: blur(18px);
    box-shadow: 0 22px 70px rgba(0, 0, 0, .35);
}
[data-testid="stWidgetLabel"] p {
    color: #b8b8c2; font-size: .72rem; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
}
[data-testid="stTextInput"] input,
[data-baseweb="select"] > div {
    background: #11121a !important; border: 1px solid rgba(255,255,255,.1) !important;
    color: var(--ink) !important; border-radius: 14px !important; min-height: 52px;
}
[data-testid="stTextInput"] input:focus { border-color: rgba(173,140,255,.7) !important; }
[data-baseweb="select"] input { color: var(--ink) !important; }
[data-baseweb="popover"] { color: #11131a; }
.stButton > button {
    width: 100%; min-height: 52px; border: 0; border-radius: 14px;
    background: linear-gradient(110deg, var(--orange), #ff477e 52%, var(--violet));
    color: white; font-weight: 800; box-shadow: 0 10px 28px rgba(255, 71, 126, .23);
    transition: transform .18s ease, filter .18s ease;
}
.stButton > button:hover { transform: translateY(-2px); filter: brightness(1.08); color: white; border: 0; }
.stButton > button:active { transform: translateY(0); }
.search-summary { text-align: center; color: #858691; font-size: .76rem; margin-top: .55rem; }
.search-summary strong { color: #d8d8df; }
.quick-label {
    margin-top: .55rem; text-align: center; color: #70717d; font-size: .7rem;
    letter-spacing: .12em; text-transform: uppercase;
}
[data-testid="column"] [data-testid="stButton"] button[kind="secondary"] {
    min-height: 38px; padding: .35rem .8rem; background: rgba(255,255,255,.035);
    border: 1px solid var(--line); box-shadow: none; color: #aaaab4; font-size: .78rem;
}

.section-heading {
    display: flex; align-items: end; justify-content: space-between;
    margin: 4.4rem 0 1.4rem;
}
.section-heading span {
    color: var(--orange); font-size: .7rem; letter-spacing: .14em;
    text-transform: uppercase; font-weight: 700;
}
.section-heading h2 { color: var(--ink); font-size: 1.8rem; letter-spacing: -.04em; margin: .28rem 0 0; }
.section-heading p { margin: 0; font-size: .84rem; }

.feature {
    min-height: 440px; display: flex; align-items: center; overflow: hidden;
    position: relative; border: 1px solid var(--line); border-radius: 30px;
    background-position: center; background-size: cover;
    box-shadow: 0 28px 90px rgba(0,0,0,.35);
}
.feature::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(0deg, rgba(8,9,14,.55), transparent 38%);
    pointer-events: none;
}
.feature-copy { max-width: 720px; padding: 3.25rem; position: relative; z-index: 1; }
.feature-kicker {
    color: #d5c7ff; font-size: .7rem; letter-spacing: .14em;
    text-transform: uppercase; font-weight: 700;
}
.feature h2 {
    color: var(--ink); font-size: clamp(2.7rem, 5vw, 5rem); line-height: .96;
    letter-spacing: -.065em; margin: .9rem 0 1rem;
}
.tagline { color: #e5e5eb; font-size: 1rem; font-weight: 600; margin-bottom: .8rem; }
.overview { color: #b8b9c3; max-width: 680px; line-height: 1.75; font-size: .92rem; }
.chips { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.4rem; }
.chip {
    color: #e1e1e7; background: rgba(12,13,18,.62); border: 1px solid rgba(255,255,255,.12);
    backdrop-filter: blur(10px); border-radius: 999px; padding: .42rem .68rem; font-size: .72rem;
}

.movie-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(175px, 1fr)); gap: 1.25rem 1rem;
}
.movie-card { min-width: 0; }
.movie-poster {
    aspect-ratio: 2 / 3; border-radius: 18px; background-position: center; background-size: cover;
    position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,.1);
    box-shadow: 0 18px 45px rgba(0,0,0,.28);
    transition: transform .24s ease, box-shadow .24s ease;
}
.movie-card:hover .movie-poster { transform: translateY(-7px); box-shadow: 0 28px 60px rgba(0,0,0,.42); }
.rank-badge, .match-badge {
    position: absolute; z-index: 2; color: white; font-weight: 800; font-size: .65rem;
    letter-spacing: .04em; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,.18);
}
.rank-badge { top: .7rem; left: .7rem; background: rgba(8,9,13,.55); padding: .42rem .5rem; border-radius: 9px; }
.match-badge { left: .7rem; bottom: .7rem; background: rgba(8,9,13,.72); padding: .42rem .52rem; border-radius: 8px; }
.fallback-art { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 1.35rem; }
.fallback-art::after {
    content: ''; position: absolute; width: 170px; height: 170px;
    border: 1px solid rgba(255,255,255,.24); border-radius: 50%; right: -65px; top: -45px;
}
.fallback-art span, .fallback-art small {
    color: rgba(255,255,255,.72); font-size: .56rem; letter-spacing: .12em;
    text-transform: uppercase; font-weight: 700;
}
.fallback-art strong {
    color: white; font-family: 'Manrope'; font-size: clamp(1.2rem, 1.65vw, 1.85rem);
    line-height: 1.02; letter-spacing: -.055em; margin: .6rem 0;
}
.movie-copy { padding: .88rem .18rem 0; }
.movie-copy h3 {
    color: var(--ink); font-size: .92rem; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis; margin: 0 0 .38rem;
}
.movie-meta { display: flex; align-items: center; gap: .42rem; color: #a6a6b1; font-size: .69rem; }
.movie-meta .dot { width: 3px; height: 3px; background: #656672; border-radius: 50%; }
.movie-copy p { margin: .35rem 0 0; font-size: .68rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.footer-note {
    text-align: center; color: #60616c; font-size: .7rem; margin-top: 4.5rem;
    padding-top: 1.4rem; border-top: 1px solid var(--line);
}

@media (max-width: 900px) {
    .block-container { padding-inline: 1.15rem; }
    .hero { padding-top: 3.8rem; }
    .feature { min-height: 400px; background-position: 62% center; }
    .feature-copy { padding: 2rem; }
    .section-heading p { display: none; }
}
@media (max-width: 620px) {
    .hero h1 { font-size: 3.15rem; }
    .nav-status { display: none; }
    .feature { min-height: 460px; align-items: end; background-position: 68% center; }
    .feature-copy { padding: 1.5rem; }
    .overview { display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
    .movie-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem .7rem; }
}
</style>
"""
