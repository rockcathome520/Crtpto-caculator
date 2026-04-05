import streamlit as st

# ======================
# 主題切換
# ======================
theme_dark = st.toggle("🌙 暗黑模式", value=True)

# ======================
# 動態 CSS
# ======================
if theme_dark:
    bg_color = "#0e1117"
    card_bg = "#161b22"
    text_color = "#ffffff"
    sub_text = "#8b949e"
else:
    bg_color = "#f5f7fb"
    card_bg = "#ffffff"
    text_color = "#111111"
    sub_text = "#555555"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
}}
.block-container {{
    padding-top: 2rem;
}}
.card {{
    background-color: {card_bg};
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    text-align: center;
}}
.card-title {{
    color: {sub_text};
    font-size: 14px;
}}
.card-value {{
    font-size: 28px;
    font-weight: bold;
    color: {text_color};
}}
hr {{
    border: 1px solid #222;
}}
</style>
""", unsafe_allow_html=True)

# ======================
# 標題
# ======================
st.markdown(f"""
<h1 style='text-align: center; color:{text_color};'>
🚀 Crypto Leverage Pro
</h1>
<p style='text-align: center; color:{sub_text};'>
倉位 × 槓桿 × 風險，一眼掌握
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ======================
# 輸入區
# ======================
col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("1. 合約帳戶本金 (USDT)", min_value=0.0, value=1000.0, step=100.0)
    risk_amount = st.number_input("2. 單筆最大可虧損金額 (USDT)", min_value=0.0, value=50.0, step=10.0)

with col2:
    margin_pct = st.slider("3. 投入保證金佔本金 %", min_value=1, max_value=100, value=10)
    sl_pct = st.number_input("4. 止損距離 %", min_value=0.1, value=5.0, step=0.5)

# ======================
# 計算
# ======================
if sl_pct > 0 and margin_pct > 0:

    position_size = risk_amount / (sl_pct / 100)
    actual_margin = balance * (margin_pct / 100)
    leverage = position_size / actual_margin

    st.markdown("---")

    # ======================
    # 卡片 UI
    # ======================
    colA, colB, colC = st.columns(3)

    def card(title, value, color):
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value" style="color:{color};">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    with colA:
        card("開倉價值", f"{position_size:,.0f} USDT", "#00E5FF")

    with colB:
        card("槓桿倍數", f"{leverage:.2f}x", "#FACC15")

    with colC:
        card("保證金", f"{actual_margin:,.0f} USDT", "#4ADE80")

    # ======================
    # 風險提示
    # ======================
    st.markdown("<br>", unsafe_allow_html=True)

    if leverage > 20:
        st.markdown(f"""
        <div style="background-color:#2b0000;padding:15px;border-radius:10px;color:#ff4d4f;">
        ⚠️ 槓桿過高，請注意強平風險！
        </div>
        """, unsafe_allow_html=True)

    elif leverage < 1:
        st.markdown(f"""
        <div style="background-color:#002b1a;padding:15px;border-radius:10px;color:#00c896;">
        💡 此倉位不需槓桿，現貨即可
        </div>
        """, unsafe_allow_html=True)

    # ======================
    # 說明區
    # ======================
    st.markdown(f"""
    <div style="
        background-color:{card_bg};
        padding:15px;
        border-radius:10px;
        color:{sub_text};
        margin-top:10px;
    ">
    💡 若價格反向 <b>{sl_pct}%</b>，  
    預計虧損 <b>{risk_amount} USDT</b>
    </div>
    """, unsafe_allow_html=True)
