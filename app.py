import streamlit as st

# ======================
# 主題切換
# ======================
theme_dark = st.toggle("🌙 Dark Mode", value=True)

# ======================
# 顏色系統（對比拉開）
# ======================
if theme_dark:
    bg = "#0d1117"
    section = "#111827"
    card = "#1f2933"
    text_main = "#ffffff"
    text_sub = "#9ca3af"
else:
    bg = "#f3f4f6"
    section = "#ffffff"
    card = "#ffffff"
    text_main = "#111111"
    text_sub = "#6b7280"

# ======================
# CSS（重做）
# ======================
st.markdown(f"""
<style>
body {{
    background-color: {bg};
}}

.block-container {{
    max-width: 880px;
    padding-top: 2rem;
}}

/* 區塊 */
.section {{
    background: {section};
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 30px;
}}

/* 卡片（重點） */
.card {{
    background: {card};
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    transition: 0.2s;
}}
.card:hover {{
    transform: translateY(-2px);
}}

/* 標題 */
.title {{
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
    color: {text_main};
}}

/* 卡片標題 */
.card-title {{
    font-size: 12px;
    color: {text_sub};
    margin-bottom: 8px;
}}

/* 數字 */
.card-value {{
    font-size: 30px;
    font-weight: 700;
    color: {text_main};
}}

/* 小數 */
.decimal {{
    font-size: 16px;
    color: {text_sub};
    margin-left: 2px;
}}
</style>
""", unsafe_allow_html=True)

# ======================
# Header
# ======================
st.markdown(f"""
<h1 style="text-align:center;color:{text_main};">
🚀 Crypto Leverage Pro
</h1>
<p style="text-align:center;color:{text_sub};">
Position • Leverage • Risk
</p>
""", unsafe_allow_html=True)

# ======================
# 上半部：輸入
# ======================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="title">⚙️ 條件設定</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("本金 (USDT)", value=1000.0)
    risk_amount = st.number_input("單筆虧損 (USDT)", value=50.0)

with col2:
    margin_pct = st.number_input("保證金 (%)", value=10.0)
    sl_pct = st.number_input("止損 (%)", value=5.0)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# 計算
# ======================
if sl_pct > 0 and margin_pct > 0:

    position_size = risk_amount / (sl_pct / 100)
    actual_margin = balance * (margin_pct / 100)
    leverage = position_size / actual_margin

    # ======================
    # 下半部：結果
    # ======================
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">📊 計算結果</div>', unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    def format_num(x):
        main = int(x)
        dec = abs(x - main)
        return f"{main:,}", f"{dec:.2f}"[1:]

    def card_ui(title, val):
        main, dec = format_num(val)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">
                {main}<span class="decimal">{dec}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with colA:
        card_ui("開倉價值", position_size)

    with colB:
        card_ui("槓桿倍數", leverage)

    with colC:
        card_ui("保證金", actual_margin)

    st.markdown('</div>', unsafe_allow_html=True)
