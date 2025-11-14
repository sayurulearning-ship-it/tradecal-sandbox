import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Trading Calculator", page_icon="📊", layout="wide")

# Fee percentage
FEE_PERCENTAGE = 1.12

# Create tabs
tab1, tab2 = st.tabs(["💹 Single Trade Calculator", "⚖️ Break-Even Calculator"])

# ==================== TAB 1: Original Calculator ====================
with tab1:
    # Title and description
    st.title("📊 Trading Calculator")
    st.markdown("Calculate your trading profits with transaction fees")

    # Input section
    st.subheader("Trade Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        buy_price = st.number_input("Buy Price", min_value=0.0, value=100.0, step=1.0, format="%.2f", key="tab1_buy")
        
    with col2:
        sell_price = st.number_input("Sell Price", min_value=0.0, value=105.0, step=1.0, format="%.2f", key="tab1_sell")

    with col3:
        quantity = st.number_input("No. of Stocks", min_value=1, value=1, step=1, key="tab1_qty")

    # Trading day option
    same_day = st.radio(
        "Trading Type",
        options=["Same Day Trading", "Sell on Another Day"],
        help="Same day trading: Fee charged once. Another day: Fee charged twice.",
        key="tab1_same_day"
    )

    st.divider()

    # Calculations with Average Price (B.E.S Price)
    total_buy_value = buy_price * quantity
    buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
    total_cost = total_buy_value + buy_fee
    
    # Calculate Average Price (B.E.S Price) - this is the adjusted buy price after fees
    avg_price_bes = total_cost / quantity
    
    if same_day == "Same Day Trading":
        # Fee charged once (on buy)
        total_sell_value = sell_price * quantity
        sell_fee = 0
        proceeds = total_sell_value
        fee_count = "1x"
    else:
        # Fee charged twice (on buy and sell)
        total_sell_value = sell_price * quantity
        sell_fee = total_sell_value * (FEE_PERCENTAGE / 100)
        proceeds = total_sell_value - sell_fee
        fee_count = "2x"

    # Calculate gain/loss based on average price
    gain_loss = proceeds - total_cost
    gain_loss_percentage = (gain_loss / total_cost) * 100 if total_cost > 0 else 0

    # Display results
    st.subheader("📈 Calculation Results")

    # Buy section
    st.markdown("### 🟢 Buy Transaction")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Quantity", f"{quantity}")
    with col2:
        st.metric("Buy Price", f"Rs. {buy_price:.2f}")
    with col3:
        st.metric("Fee (1.12%)", f"Rs. {buy_fee:.3f}")
    with col4:
        st.metric("Total Cost", f"Rs. {total_cost:.2f}", delta=None, delta_color="normal")

    # Show Average Price (B.E.S Price)
    st.info(f"**📊 B.E.S Price (Avg Price): Rs. {avg_price_bes:.4f}** - This is your effective buy price per stock after fees")

    st.divider()

    # Sell section
    st.markdown("### 🔴 Sell Transaction")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Quantity", f"{quantity}")
    with col2:
        st.metric("Sell Price", f"Rs. {sell_price:.2f}")
    with col3:
        if same_day == "Same Day Trading":
            st.metric("Fee", "Rs. 0.00", help="No fee on same day sell")
        else:
            st.metric("Fee (1.12%)", f"Rs. {sell_fee:.3f}")
    with col4:
        st.metric("Proceeds", f"Rs. {proceeds:.3f}")

    st.divider()

    # Profit/Loss section
    st.markdown("### 💰 Profit/Loss Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        if gain_loss >= 0:
            st.metric("Gain/Loss", f"Rs. {gain_loss:.3f}", delta=f"+{gain_loss:.3f}", delta_color="normal")
        else:
            st.metric("Gain/Loss", f"Rs. {gain_loss:.3f}", delta=f"{gain_loss:.3f}", delta_color="inverse")

    with col2:
        if gain_loss_percentage >= 0:
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"+{gain_loss_percentage:.2f}%")
        else:
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"{gain_loss_percentage:.2f}%", delta_color="inverse")

    with col3:
        total_fees = buy_fee + sell_fee
        st.metric("Total Fees", f"Rs. {total_fees:.3f}", help=f"Fee charged {fee_count}")

    st.markdown("")
    st.markdown("")
    
    st.info(f"""
    **Fee Structure:**
    - Transaction Fee: **{FEE_PERCENTAGE}%**
    - Same Day Trading: Fee charged **once** (on buy only)
    - Sell on Another Day: Fee charged **twice** (on buy and sell)
    """)

    with st.expander("📋 Detailed Breakdown"):
        st.markdown(f"""
        **Buy Transaction:**
        - Quantity: {quantity} stocks
        - Buy Price per Stock: Rs. {buy_price:.2f}
        - Total Buy Value: Rs. {total_buy_value:.2f}
        - Buy Fee ({FEE_PERCENTAGE}%): Rs. {buy_fee:.3f}
        - **Total Cost: Rs. {total_cost:.2f}**
        - **B.E.S Price (Avg Price): Rs. {avg_price_bes:.4f}** (Total Cost ÷ Quantity)
        
        **Sell Transaction:**
        - Quantity: {quantity} stocks
        - Sell Price per Stock: Rs. {sell_price:.2f}
        - Total Sell Value: Rs. {total_sell_value:.2f}
        - Sell Fee: Rs. {sell_fee:.3f} {'(No fee - same day)' if same_day == 'Same Day Trading' else f'({FEE_PERCENTAGE}%)'}
        - **Proceeds: Rs. {proceeds:.3f}**
        
        **Summary:**
        - Total Fees Paid: Rs. {total_fees:.3f}
        - Net Gain/Loss: Rs. {gain_loss:.3f}
        - Return on Investment: {gain_loss_percentage:.2f}%
        
        **Note:** The B.E.S Price (Avg Price) represents your effective cost per share after including the buy fee. 
        To make profit, your sell price must be higher than Rs. {avg_price_bes:.4f} (plus sell fees if applicable).
        """)

# ==================== TAB 2: Break-Even Calculator ====================
with tab2:
    st.title("⚖️ Break-Even Calculator")
    st.markdown("Calculate minimum sell price to break even after fees (based on B.E.S Price)")
    
    st.subheader("📊 Input Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        be_buy_price = st.number_input("Buy Price", min_value=0.01, value=100.0, step=1.0, format="%.2f", key="be_buy")
    
    with col2:
        be_quantity = st.number_input("No. of Stocks", min_value=1, value=1, step=1, key="be_qty")
    
    be_same_day = st.radio(
        "Trading Type",
        options=["Same Day Trading", "Sell on Another Day"],
        help="Same day trading: Fee charged once. Another day: Fee charged twice.",
        key="be_same_day"
    )
    
    st.divider()
    
    # Calculate break-even with B.E.S Price
    be_total_buy_value = be_buy_price * be_quantity
    be_buy_fee = be_total_buy_value * (FEE_PERCENTAGE / 100)
    be_total_cost = be_total_buy_value + be_buy_fee
    
    # Calculate B.E.S Price (Average Price)
    be_avg_price = be_total_cost / be_quantity
    
    if be_same_day == "Same Day Trading":
        # For same day: Sell price * quantity = total_cost
        # No sell fee
        be_sell_price = be_total_cost / be_quantity
        be_sell_fee = 0
        be_proceeds = be_sell_price * be_quantity
    else:
        # For another day: (Sell price * quantity) - sell_fee = total_cost
        # sell_fee = (Sell price * quantity) * 0.0112
        # (Sell price * quantity) * (1 - 0.0112) = total_cost
        # Sell price = total_cost / (quantity * (1 - 0.0112))
        be_sell_price = be_total_cost / (be_quantity * (1 - FEE_PERCENTAGE / 100))
        be_sell_fee = (be_sell_price * be_quantity) * (FEE_PERCENTAGE / 100)
        be_proceeds = (be_sell_price * be_quantity) - be_sell_fee
    
    be_price_increase = be_sell_price - be_buy_price
    be_percentage_move = (be_price_increase / be_buy_price) * 100
    
    # Price increase from B.E.S Price
    be_price_increase_from_avg = be_sell_price - be_avg_price
    be_percentage_move_from_avg = (be_price_increase_from_avg / be_avg_price) * 100
    
    # Display B.E.S Price prominently
    st.markdown("### 📊 Your Average Price (B.E.S Price)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Buy Price", f"Rs. {be_buy_price:.2f}")
    with col2:
        st.metric("B.E.S Price (Avg Price)", f"Rs. {be_avg_price:.4f}", 
                 delta=f"+Rs. {be_avg_price - be_buy_price:.4f}",
                 help="Your effective cost per share after including buy fees")
    with col3:
        st.metric("Total Cost", f"Rs. {be_total_cost:.2f}")
    
    st.divider()
    
    # Display break-even results
    st.subheader("🎯 Break-Even Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Break-Even Sell Price", f"Rs. {be_sell_price:.3f}", 
                 help="Minimum sell price to recover all costs including fees")
    
    with col2:
        st.metric("Move from Buy Price", f"Rs. {be_price_increase:.3f}",
                 delta=f"+{be_percentage_move:.2f}%",
                 help="Price increase from original buy price")
    
    with col3:
        st.metric("Move from B.E.S Price", f"Rs. {be_price_increase_from_avg:.3f}",
                 delta=f"+{be_percentage_move_from_avg:.2f}%",
                 help="Price increase from average price (B.E.S)")
    
    st.divider()
    
    # Cost breakdown
    st.markdown("### 💵 Cost Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Buy Cost", f"Rs. {be_total_buy_value:.2f}")
    
    with col2:
        st.metric("Buy Fee", f"Rs. {be_buy_fee:.3f}")
    
    with col3:
        if be_same_day == "Same Day Trading":
            st.metric("Sell Fee", "Rs. 0.00", help="No fee on same day sell")
        else:
            st.metric("Sell Fee", f"Rs. {be_sell_fee:.3f}")
    
    with col4:
        total_be_fees = be_buy_fee + be_sell_fee
        st.metric("Total Fees", f"Rs. {total_be_fees:.3f}")
    
    st.divider()
    
    # Profit targets
    st.markdown("### 🎯 Profit Target Scenarios")
    st.markdown("Calculate sell prices for different profit targets (based on B.E.S Price):")
    
    profit_targets = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    
    target_data = []
    
    for target_pct in profit_targets:
        # Target profit amount based on total cost
        target_profit = be_total_cost * (target_pct / 100)
        target_proceeds = be_total_cost + target_profit
        
        if be_same_day == "Same Day Trading":
            # No sell fee for same day
            target_sell_price = target_proceeds / be_quantity
        else:
            # With sell fee
            target_sell_price = target_proceeds / (be_quantity * (1 - FEE_PERCENTAGE / 100))
        
        # Calculate percentage from B.E.S Price
        pct_from_avg = ((target_sell_price - be_avg_price) / be_avg_price) * 100
        
        target_data.append({
            'Target Profit %': f"{target_pct}%",
            'Profit Amount': f"Rs. {target_profit:.2f}",
            'Required Sell Price': f"Rs. {target_sell_price:.2f}",
            'Move from Buy Price': f"+{((target_sell_price - be_buy_price) / be_buy_price * 100):.2f}%",
            'Move from B.E.S Price': f"+{pct_from_avg:.2f}%"
        })
    
    df = pd.DataFrame(target_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Custom profit target
    st.markdown("### 🎲 Custom Profit Target")
    
    col1, col2 = st.columns(2)
    
    with col1:
        custom_target = st.number_input(
            "Desired Profit %",
            min_value=0.01,
            max_value=1000.0,
            value=5.0,
            step=0.5,
            format="%.2f",
            key="custom_target"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        custom_profit_amount = be_total_cost * (custom_target / 100)
        st.metric("Target Profit Amount", f"Rs. {custom_profit_amount:.2f}")
    
    # Calculate custom target sell price
    custom_proceeds = be_total_cost + custom_profit_amount
    
    if be_same_day == "Same Day Trading":
        custom_sell_price = custom_proceeds / be_quantity
    else:
        custom_sell_price = custom_proceeds / (be_quantity * (1 - FEE_PERCENTAGE / 100))
    
    custom_move = custom_sell_price - be_buy_price
    custom_pct_move = (custom_move / be_buy_price) * 100
    custom_move_from_avg = custom_sell_price - be_avg_price
    custom_pct_move_from_avg = (custom_move_from_avg / be_avg_price) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Required Sell Price", f"Rs. {custom_sell_price:.3f}")
    
    with col2:
        st.metric("Move from Buy Price", f"Rs. {custom_move:.3f}", 
                 delta=f"+{custom_pct_move:.2f}%")
    
    with col3:
        st.metric("Move from B.E.S Price", f"Rs. {custom_move_from_avg:.3f}",
                 delta=f"+{custom_pct_move_from_avg:.2f}%")
    
    st.divider()
    
    # Info box
    st.info(f"""
    **Break-Even Explained (with B.E.S Price):**
    - Original Buy Price: **Rs. {be_buy_price:.2f}**
    - B.E.S Price (Avg Price): **Rs. {be_avg_price:.4f}** (includes buy fee)
    - Total cost including fees: **Rs. {be_total_cost:.2f}**
    - To break even, sell price must be: **Rs. {be_sell_price:.3f}**
    
    **Fee Impact:**
    - Transaction Fee: **{FEE_PERCENTAGE}%**
    - Total Fees to Break Even: **Rs. {total_be_fees:.3f}**
    - Break-Even requires **{be_percentage_move:.2f}%** move from buy price
    - Break-Even requires **{be_percentage_move_from_avg:.2f}%** move from B.E.S price
    """)
    
    # Detailed calculation
    with st.expander("🔍 Detailed Break-Even Calculation"):
        st.markdown(f"""
        **Step-by-Step Calculation:**
        
        **Buy Side:**
        1. Buy Price per Stock: Rs. {be_buy_price:.2f}
        2. Quantity: {be_quantity} stocks
        3. Total Buy Value: Rs. {be_buy_price:.2f} × {be_quantity} = Rs. {be_total_buy_value:.2f}
        4. Buy Fee ({FEE_PERCENTAGE}%): Rs. {be_total_buy_value:.2f} × {FEE_PERCENTAGE/100} = Rs. {be_buy_fee:.3f}
        5. **Total Cost: Rs. {be_total_buy_value:.2f} + Rs. {be_buy_fee:.3f} = Rs. {be_total_cost:.2f}**
        6. **B.E.S Price (Avg Price): Rs. {be_total_cost:.2f} ÷ {be_quantity} = Rs. {be_avg_price:.4f}**
        
        **Sell Side (Break-Even):**
        {'7. Sell Fee: Rs. 0.00 (Same day trading - no sell fee)' if be_same_day == 'Same Day Trading' else f'7. Sell Fee ({FEE_PERCENTAGE}%): Rs. {be_sell_fee:.3f}'}
        8. Required Proceeds: Rs. {be_proceeds:.3f} (must equal Total Cost)
        9. **Break-Even Sell Price: Rs. {be_sell_price:.3f}**
        
        **Price Movement:**
        10. From Buy Price: Rs. {be_sell_price:.3f} - Rs. {be_buy_price:.2f} = Rs. {be_price_increase:.3f} ({be_percentage_move:.2f}%)
        11. From B.E.S Price: Rs. {be_sell_price:.3f} - Rs. {be_avg_price:.4f} = Rs. {be_price_increase_from_avg:.3f} ({be_percentage_move_from_avg:.2f}%)
        
        **Key Insight:** 
        The B.E.S Price (Rs. {be_avg_price:.4f}) is your true effective cost per share after fees. 
        This is the baseline price you should monitor in your trading platform.
        {'For same day trading, you break even at this exact price since there is no sell fee.' if be_same_day == 'Same Day Trading' else f'For multi-day trading, you need Rs. {be_sell_price:.3f} to cover both buy and sell fees.'}
        """)
