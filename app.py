import streamlit as st

# 網頁設定
st.set_page_config(page_title="Crypto Leverage Pro", layout="centered")

# 標題與樣式
st.title("🚀 加密貨幣永續合約計算器")
st.markdown("---")

# 側邊欄或主畫面輸入
col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("1. 合約帳戶本金 (USDT)", min_value=0.0, value=1000.0, step=100.0)
    risk_amount = st.number_input("2. 單筆最大可虧損金額 (USDT)", min_value=0.0, value=50.0, step=10.0)

with col2:
    margin_pct = st.slider("3. 投入保證金佔本金 %", min_value=1, max_value=100, value=10)
    sl_pct = st.number_input("4. 止損距離 % (例如 5% 輸入 5)", min_value=0.1, value=5.0, step=0.5)

# 計算邏輯
if sl_pct > 0 and margin_pct > 0:
    # 開倉總價值 = 虧損金額 / 止損比例
    position_size = risk_amount / (sl_pct / 100)
    
    # 實際投入的保證金金額
    actual_margin = balance * (margin_pct / 100)
    
    # 槓桿倍數 = 開倉總價值 / 投入保證金
    leverage = position_size / actual_margin

    st.markdown("---")
    st.subheader("📊 計算結果")
    
    # 使用 Metric 卡片呈現專業感
    res_col1, res_col2, res_col3 = st.columns(3)
    
    res_col1.metric("建議開倉價值", f"{position_size:,.2f} USDT")
    res_col2.metric("建議槓桿倍數", f"{leverage:.2f} x")
    res_col3.metric("投入保證金金額", f"{actual_margin:,.2f} USDT")

    # 警示訊息
    if leverage > 20:
        st.warning("⚠️ 警告：槓桿倍數過高，請注意強平風險！")
    elif leverage < 1:
        st.info("💡 提示：此倉位不需要開槓桿，現貨即可覆蓋。")
        
    st.info(f"💡 說明：若價格觸及 {sl_pct}% 止損，你將損失 {risk_amount} USDT。")
