import streamlit as st

# ======================
# 主題切換
# ======================
theme_dark = st.toggle("🌙 暗黑模式", value=True)

# ======================
# 顏色設定
# ======================
if theme_dark:
    bg_main = "#0e1117"
    section_bg = "#161b22"
    card_bg = "#1c2128"
    text_main = "#ffffff"
    text_sub = "#8b949e"
else:
    bg_main = "#f5f7fb"
    section_bg = "#ffffff"
    card_bg = "#ffffff"
    text_main = "#111111"
    text_sub = "#666666"

# ======================
# 全域CSS
# ======================
st.markdown(f"""
<style>
body {{
    background-color: {bg_main};
}}

.block-container {{
    padding-top: 2rem;
    max-width: 900px;
}}

.section {{
    background-color: {section_bg};
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
}}

.card {{
    background-color: {card_bg};
    padding: 18px;
    border-radius: 14px;
    text-align: center;
}}

.card-title {{
    font-size: 13px;
    color: {text_sub};
    margin-bottom: 6px;
}}

.card-value {{
    font-size: 26px;
    font-weight: 600;
    color: {text_main};
}}

.decimal {{
    font-size: 16px;
    color: {text_sub};
}}

.section-title {{
    font-size: 18px;
    font-weight: 600;
    color: {text_main};
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# ======================
# 標題
# ======================
st.markdown(f"""
<h1 style='text-align:center; color:{text_main};'>
🚀 Crypto Leverage Pro
</h1>
<p style='text-align:center; color:{text_sub};'>
倉位 × 槓桿 × 風險，一眼掌握
</p>
""", unsafe_allow_html=True)

# ======================
# 輸入區（上半部）
# ======================
st.markdown(f'<div class="section">', unsafe_allow_html=True)
st.markdown(f'<div class="section-title">⚙️ 條件設定</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("合約帳戶本金 (USDT)", value=1000.0)
    risk_amount = st.number_input("單筆最大可虧損 (USDT)", value=50.0)

with col2:
    margin_pct = st.number_input("投入保證金佔本金 (%)", value=10.0)
    sl_pct = st.number_input("止損距離 (%)", value=5.0)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 計算
# ======================
if sl_pct > 0 and margin_pct > 0:

    position_size = risk_amount / (sl_pct / 100)
    actual_margin = balance * (margin_pct / 100)
    leverage = position_size / actual_margin

    # ======================
    # 結果區（下半部）
    # ======================
    st.markdown(f'<div class="section">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📊 計算結果</div>', unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    def format_number(num):
        main = int(num)
        decimal = abs(num - main)
        return f"{main:,}", f"{decimal:.2f}"[1:]

    def card(title, value, color):
        main, dec = format_number(value)

        st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">
                {main}<span class="decimal">{dec}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with colA:
        card("開倉價值 (USDT)", position_size, "#00E5FF")

    with colB:
        card("槓桿倍數 (x)", leverage, "#FACC15")

    with colC:
        card("保證金 (USDT)", actual_margin, "#4ADE80")

    # ======================
    # 提示
    # ======================
    st.markdown("<br>", unsafe_allow_html=True)

    if leverage > 20:
        st.markdown(f"""
        <div style="background:#2b0000;padding:12px;border-radius:10px;color:#ff4d4f;">
        ⚠️ 槓桿過高，風險極大
        </div>
        """, unsafe_allow_html=True)

    elif leverage < 1:
        st.markdown(f"""
        <div style="background:#002b1a;padding:12px;border-radius:10px;color:#00c896;">
        💡 可用現貨，不需槓桿
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background:{card_bg};
        padding:12px;
        border-radius:10px;
        color:{text_sub};
        margin-top:10px;
    ">
    若價格反向 <b>{sl_pct}%</b>，預計虧損 <b>{risk_amount} USDT</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
