import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Trading Calculator", page_icon="📊", layout="wide")

# Fee percentage
FEE_PERCENTAGE = 1.12

# Create tabs
tab1, tab2, tab3 = st.tabs(["💹 Single Trade Calculator", "⚖️ Break-Even Calculator", "🔄 Intraday Multi-Trade Calculator"])

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

    # Calculations - New Logic
    # Step 1: Calculate buy fee and average price
    total_buy_value = buy_price * quantity
    buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
    
    # Average Price (Avg Price) = (Buy Value + Buy Fee) / Quantity
    avg_price = (total_buy_value + buy_fee) / quantity
    
    # Total Cost = Avg Price × Quantity
    total_cost = avg_price * quantity
    
    # Step 2: Calculate B.E.S Price (Break-Even Sell Price)
    if same_day == "Same Day Trading":
        # For same day: No additional fee, break even at avg price
        bes_price = avg_price
        sell_fee = 0
    else:
        # For another day: B.E.S = Avg Price × 1.0112
        bes_price = avg_price * (1 + FEE_PERCENTAGE / 100)
        # Calculate sell fee based on sell price
        sell_fee = sell_price * quantity * (FEE_PERCENTAGE / 100) if sell_price > 0 else 0
    
    # Step 3: Calculate proceeds from selling
    total_sell_value = sell_price * quantity
    if same_day == "Same Day Trading":
        proceeds = total_sell_value
        fee_count = "1x (buy only)"
    else:
        proceeds = total_sell_value - sell_fee
        fee_count = "2x (buy + sell)"

    # Calculate gain/loss
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
        st.metric("Buy Fee (1.12%)", f"Rs. {buy_fee:.2f}")
    with col4:
        st.metric("Total Cost", f"Rs. {total_cost:.2f}")

    # Show Average Price and B.E.S Price
    st.markdown("### 📊 Price Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Price", f"Rs. {avg_price:.4f}",
                 delta=f"+Rs. {avg_price - buy_price:.4f}",
                 help="Average price after including buy fee")
    with col2:
        st.metric("B.E.S Price (Break-Even)", f"Rs. {bes_price:.4f}",
                 delta=f"+{((bes_price - buy_price) / buy_price * 100):.2f}%" if bes_price > buy_price else "0.00%",
                 help="Minimum sell price to break even")
    with col3:
        price_move_needed = bes_price - buy_price
        st.metric("Price Move to Break Even", f"Rs. {price_move_needed:.4f}",
                 help="How much price needs to increase from original buy price")

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
            st.metric("Sell Fee", "Rs. 0.00", help="No sell fee on same day")
        else:
            st.metric("Sell Fee (1.12%)", f"Rs. {sell_fee:.2f}")
    with col4:
        st.metric("Proceeds", f"Rs. {proceeds:.2f}")

    st.divider()

    # Profit/Loss section
    st.markdown("### 💰 Profit/Loss Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        if gain_loss >= 0:
            st.metric("Gain/Loss", f"Rs. {gain_loss:.2f}", delta=f"+{gain_loss:.2f}", delta_color="normal")
        else:
            st.metric("Gain/Loss", f"Rs. {gain_loss:.2f}", delta=f"{gain_loss:.2f}", delta_color="inverse")

    with col2:
        if gain_loss_percentage >= 0:
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"+{gain_loss_percentage:.2f}%")
        else:
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"{gain_loss_percentage:.2f}%", delta_color="inverse")

    with col3:
        total_fees = buy_fee + sell_fee
        st.metric("Total Fees", f"Rs. {total_fees:.2f}", help=f"Fee charged {fee_count}")

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
        - Buy Price per Stock: Rs. {buy_price:.2f}
        - Quantity: {quantity} stocks
        - Total Buy Value: Rs. {total_buy_value:.2f}
        - Buy Fee ({FEE_PERCENTAGE}%): Rs. {buy_fee:.2f}
        - **Total Cost: Rs. {total_cost:.2f}**
        
        **Average Price Calculation:**
        - Avg Price = (Buy Value + Buy Fee) ÷ Quantity
        - Avg Price = (Rs. {total_buy_value:.2f} + Rs. {buy_fee:.2f}) ÷ {quantity}
        - **Avg Price = Rs. {avg_price:.4f}**
        
        **Break-Even Analysis:**
        - Avg Price: Rs. {avg_price:.4f}
        - B.E.S Price: Rs. {bes_price:.4f}
        {f"- Same as Avg Price (no sell fee for same day)" if same_day == 'Same Day Trading' else f"- B.E.S = Avg Price × 1.0112 = Rs. {avg_price:.4f} × 1.0112"}
        - Price Move Needed: Rs. {price_move_needed:.4f} ({((price_move_needed / buy_price) * 100):.2f}% from buy price)
        
        **Sell Transaction:**
        - Sell Price: Rs. {sell_price:.2f}
        - Quantity: {quantity} stocks
        - Total Sell Value: Rs. {total_sell_value:.2f}
        - Sell Fee: Rs. {sell_fee:.2f} {'(No fee - same day)' if same_day == 'Same Day Trading' else f'({FEE_PERCENTAGE}% of sell value)'}
        - **Proceeds: Rs. {proceeds:.2f}**
        
        **Summary:**
        - Total Cost: Rs. {total_cost:.2f}
        - Proceeds: Rs. {proceeds:.2f}
        - Total Fees: Rs. {total_fees:.2f}
        - **Net Gain/Loss: Rs. {gain_loss:.2f}**
        - **Return on Investment: {gain_loss_percentage:.2f}%**
        """)

# ==================== TAB 2: Break-Even Calculator ====================
with tab2:
    st.title("⚖️ Break-Even Calculator")
    st.markdown("Calculate B.E.S Price (Break-Even Sell Price) from your buy price")
    
    st.subheader("📊 Input Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        be_buy_price = st.number_input("Buy Price", min_value=0.01, value=100.0, step=1.0, format="%.2f", key="be_buy")
    
    with col2:
        be_quantity = st.number_input("No. of Stocks", min_value=1, value=1, step=1, key="be_qty")
    
    be_same_day = st.radio(
        "Trading Type",
        options=["Same Day Trading", "Sell on Another Day"],
        help="Same day trading: No sell fee. Another day: Sell fee applies.",
        key="be_same_day"
    )
    
    st.divider()
    
    # Calculate with correct formula
    # Step 1: Calculate Avg Price
    be_total_buy_value = be_buy_price * be_quantity
    be_buy_fee = be_total_buy_value * (FEE_PERCENTAGE / 100)
    be_avg_price = (be_total_buy_value + be_buy_fee) / be_quantity
    be_total_cost = be_avg_price * be_quantity
    
    # Step 2: Calculate B.E.S Price
    if be_same_day == "Same Day Trading":
        # For same day: Break even at avg price (no sell fee)
        be_bes_price = be_avg_price
        be_sell_fee = 0
        be_price_increase_from_buy = be_bes_price - be_buy_price
        be_percentage_move_from_buy = (be_price_increase_from_buy / be_buy_price) * 100
    else:
        # For another day: B.E.S = Avg Price × 1.0112
        be_bes_price = be_avg_price * (1 + FEE_PERCENTAGE / 100)
        be_sell_fee = be_bes_price * be_quantity * (FEE_PERCENTAGE / 100)
        be_price_increase_from_buy = be_bes_price - be_buy_price
        be_percentage_move_from_buy = (be_price_increase_from_buy / be_buy_price) * 100
    
    # Display results
    st.subheader("🎯 Break-Even Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Buy Price", f"Rs. {be_buy_price:.2f}",
                 help="Original buy price")
    
    with col2:
        st.metric("Avg Price", f"Rs. {be_avg_price:.4f}",
                 delta=f"+Rs. {be_avg_price - be_buy_price:.4f}",
                 help="Average price after buy fee")
    
    with col3:
        st.metric("B.E.S Price", f"Rs. {be_bes_price:.4f}",
                 delta=f"+{be_percentage_move_from_buy:.2f}%" if be_percentage_move_from_buy > 0 else "Break Even",
                 help="Break-Even Sell Price")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Price Move from Buy Price", f"Rs. {be_price_increase_from_buy:.4f}",
                 help="Total increase needed from original buy price")
    with col2:
        st.metric("% Move from Buy Price", f"{be_percentage_move_from_buy:.2f}%",
                 help="Percentage increase from buy price to break even")
    
    st.divider()
    
    # Cost breakdown
    st.markdown("### 💵 Cost Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Buy Value", f"Rs. {be_total_buy_value:.2f}")
    
    with col2:
        st.metric("Buy Fee", f"Rs. {be_buy_fee:.2f}")
    
    with col3:
        st.metric("Total Cost", f"Rs. {be_total_cost:.2f}",
                 help=f"Avg Price × Quantity")
    
    with col4:
        if be_same_day == "Same Day Trading":
            st.metric("Sell Fee", "Rs. 0.00", help="No sell fee for same day")
        else:
            st.metric("Sell Fee at B.E.S", f"Rs. {be_sell_fee:.2f}",
                     help=f"Sell fee when selling at B.E.S price")
    
    st.divider()
    
    # Profit targets
    st.markdown("### 🎯 Profit Target Scenarios")
    st.markdown("Calculate sell prices for different profit targets:")
    
    profit_targets = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
    
    target_data = []
    
    for target_pct in profit_targets:
        # Target profit amount based on total cost
        target_profit = be_total_cost * (target_pct / 100)
        target_proceeds_needed = be_total_cost + target_profit
        
        if be_same_day == "Same Day Trading":
            # No sell fee: Sell Price × Qty = target_proceeds_needed
            target_sell_price = target_proceeds_needed / be_quantity
        else:
            # With sell fee: (Sell Price × Qty) - (Sell Price × Qty × 0.0112) = target_proceeds_needed
            target_sell_price = target_proceeds_needed / (be_quantity * (1 - FEE_PERCENTAGE / 100))
        
        # Calculate moves from buy price
        price_move = target_sell_price - be_buy_price
        pct_move = (price_move / be_buy_price) * 100
        
        target_data.append({
            'Target Profit %': f"{target_pct}%",
            'Profit Amount': f"Rs. {target_profit:.2f}",
            'Required Sell Price': f"Rs. {target_sell_price:.4f}",
            'Price Increase': f"Rs. {price_move:.4f}",
            'Move from Buy Price': f"+{pct_move:.2f}%"
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
    custom_proceeds_needed = be_total_cost + custom_profit_amount
    
    if be_same_day == "Same Day Trading":
        custom_sell_price = custom_proceeds_needed / be_quantity
    else:
        custom_sell_price = custom_proceeds_needed / (be_quantity * (1 - FEE_PERCENTAGE / 100))
    
    custom_move = custom_sell_price - be_buy_price
    custom_pct_move = (custom_move / be_buy_price) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Required Sell Price", f"Rs. {custom_sell_price:.4f}")
    
    with col2:
        st.metric("Price Increase Needed", f"Rs. {custom_move:.4f}")
    
    with col3:
        st.metric("Move from Buy Price", f"+{custom_pct_move:.2f}%")
    
    st.divider()
    
    # Info box
    st.info(f"""
    **How This Works:**
    
    **Buy Price: Rs. {be_buy_price:.2f}**
    - Your original buy price
    
    **Avg Price: Rs. {be_avg_price:.4f}**
    - After adding buy fee (1.12%)
    - Formula: (Buy Value + Buy Fee) ÷ Quantity
    
    **B.E.S Price: Rs. {be_bes_price:.4f}**
    - Minimum price to break even
    {f"- Same as Avg Price (no sell fee for same day)" if be_same_day == 'Same Day Trading' else f"- Avg Price × 1.0112 = Rs. {be_avg_price:.4f} × 1.0112"}
    - Needs **{be_percentage_move_from_buy:.2f}%** increase from buy price
    
    **Total Cost: Rs. {be_total_cost:.2f}**
    - This is what you need to recover to break even
    """)
    
    # Detailed calculation
    with st.expander("🔍 Detailed Break-Even Formula"):
        st.markdown(f"""
        **Step-by-Step Calculation:**
        
        **Step 1: Calculate Buy Fee and Avg Price**
        - Buy Price: Rs. {be_buy_price:.2f}
        - Quantity: {be_quantity}
        - Buy Value: Rs. {be_buy_price:.2f} × {be_quantity} = Rs. {be_total_buy_value:.2f}
        - Buy Fee (1.12%): Rs. {be_total_buy_value:.2f} × 0.0112 = Rs. {be_buy_fee:.2f}
        - **Avg Price = (Rs. {be_total_buy_value:.2f} + Rs. {be_buy_fee:.2f}) ÷ {be_quantity}**
        - **Avg Price = Rs. {be_avg_price:.4f}**
        
        **Step 2: Calculate Total Cost**
        - Total Cost = Avg Price × Quantity
        - Total Cost = Rs. {be_avg_price:.4f} × {be_quantity}
        - **Total Cost = Rs. {be_total_cost:.2f}**
        
        **Step 3: Calculate B.E.S Price**
        {'- For Same Day: B.E.S Price = Avg Price' if be_same_day == 'Same Day Trading' else f'- For Another Day: B.E.S Price = Avg Price × 1.0112'}
        {'- No sell fee for same day' if be_same_day == 'Same Day Trading' else f'- B.E.S Price = Rs. {be_avg_price:.4f} × 1.0112'}
        - **B.E.S Price = Rs. {be_bes_price:.4f}**
        
        **Step 4: Price Movement Analysis**
        - From Buy Price: Rs. {be_bes_price:.4f} - Rs. {be_buy_price:.2f} = Rs. {be_price_increase_from_buy:.4f}
        - **Percentage Move: {be_percentage_move_from_buy:.2f}%**
        
        **Key Formula:**
        ```
        Avg Price = (Buy Price × Qty + Buy Fee) ÷ Qty
        Total Cost = Avg Price × Qty
        B.E.S Price = Avg Price × 1.0112 (for another day)
        B.E.S Price = Avg Price (for same day)
        ```
        """)

# ==================== TAB 3: Intraday Multi-Trade Calculator ====================
with tab3:
    st.title("🔄 Intraday Multi-Trade Calculator")
    st.markdown("Calculate fees for multiple buy/sell trades on the same day (CSE Rules)")
    
    st.info("""
    **CSE Intraday Trading Rule:**
    When you buy and sell the same stock on the same day, transaction fees are waived on the **matched quantity** 
    (except Share Transaction Levy - STL 0.30%). Fees are only charged on the **unmatched quantity**.
    """)
    
    # Initialize session state for trades
    if 'buy_trades' not in st.session_state:
        st.session_state.buy_trades = []
    if 'sell_trades' not in st.session_state:
        st.session_state.sell_trades = []
    
    col1, col2 = st.columns(2)
    
    # BUY TRADES SECTION
    with col1:
        st.subheader("🟢 Buy Trades")
        
        with st.form("buy_trade_form"):
            buy_qty = st.number_input("Quantity", min_value=1, value=100, step=1, key="buy_qty_input")
            buy_price = st.number_input("Price", min_value=0.01, value=100.0, step=0.01, format="%.2f", key="buy_price_input")
            add_buy = st.form_submit_button("➕ Add Buy Trade")
            
            if add_buy:
                st.session_state.buy_trades.append({'qty': buy_qty, 'price': buy_price})
                st.rerun()
        
        if st.session_state.buy_trades:
            st.markdown("**Buy Trades:**")
            for idx, trade in enumerate(st.session_state.buy_trades):
                col_a, col_b, col_c = st.columns([2, 2, 1])
                with col_a:
                    st.text(f"Qty: {trade['qty']}")
                with col_b:
                    st.text(f"Price: Rs. {trade['price']:.2f}")
                with col_c:
                    if st.button("🗑️", key=f"del_buy_{idx}"):
                        st.session_state.buy_trades.pop(idx)
                        st.rerun()
            
            if st.button("🗑️ Clear All Buys"):
                st.session_state.buy_trades = []
                st.rerun()
        else:
            st.info("No buy trades added yet")
    
    # SELL TRADES SECTION
    with col2:
        st.subheader("🔴 Sell Trades")
        
        with st.form("sell_trade_form"):
            sell_qty = st.number_input("Quantity", min_value=1, value=100, step=1, key="sell_qty_input")
            sell_price = st.number_input("Price", min_value=0.01, value=105.0, step=0.01, format="%.2f", key="sell_price_input")
            add_sell = st.form_submit_button("➕ Add Sell Trade")
            
            if add_sell:
                st.session_state.sell_trades.append({'qty': sell_qty, 'price': sell_price})
                st.rerun()
        
        if st.session_state.sell_trades:
            st.markdown("**Sell Trades:**")
            for idx, trade in enumerate(st.session_state.sell_trades):
                col_a, col_b, col_c = st.columns([2, 2, 1])
                with col_a:
                    st.text(f"Qty: {trade['qty']}")
                with col_b:
                    st.text(f"Price: Rs. {trade['price']:.2f}")
                with col_c:
                    if st.button("🗑️", key=f"del_sell_{idx}"):
                        st.session_state.sell_trades.pop(idx)
                        st.rerun()
            
            if st.button("🗑️ Clear All Sells"):
                st.session_state.sell_trades = []
                st.rerun()
        else:
            st.info("No sell trades added yet")
    
    st.divider()
    
    # CALCULATIONS
    if st.session_state.buy_trades or st.session_state.sell_trades:
        st.subheader("📊 Intraday Analysis")
        
        # Calculate totals
        total_buy_qty = sum(trade['qty'] for trade in st.session_state.buy_trades)
        total_sell_qty = sum(trade['qty'] for trade in st.session_state.sell_trades)
        
        # Calculate total buy value and weighted avg buy price
        total_buy_value = sum(trade['qty'] * trade['price'] for trade in st.session_state.buy_trades)
        weighted_avg_buy_price = total_buy_value / total_buy_qty if total_buy_qty > 0 else 0
        
        # Calculate total sell value and weighted avg sell price
        total_sell_value = sum(trade['qty'] * trade['price'] for trade in st.session_state.sell_trades)
        weighted_avg_sell_price = total_sell_value / total_sell_qty if total_sell_qty > 0 else 0
        
        # Matched quantity (intraday exemption applies)
        matched_qty = min(total_buy_qty, total_sell_qty)
        
        # Unmatched quantities
        unmatched_buy_qty = total_buy_qty - matched_qty
        unmatched_sell_qty = total_sell_qty - matched_qty
        
        # Display summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Buys", f"{total_buy_qty} shares")
            st.metric("Avg Buy Price", f"Rs. {weighted_avg_buy_price:.2f}")
            st.metric("Total Buy Value", f"Rs. {total_buy_value:.2f}")
        
        with col2:
            st.metric("Total Sells", f"{total_sell_qty} shares")
            st.metric("Avg Sell Price", f"Rs. {weighted_avg_sell_price:.2f}")
            st.metric("Total Sell Value", f"Rs. {total_sell_value:.2f}")
        
        with col3:
            st.metric("Matched Qty (Fee Exempt)", f"{matched_qty} shares", 
                     help="These shares are exempt from transaction fees (except STL)")
            st.metric("Unmatched Buys", f"{unmatched_buy_qty} shares")
            st.metric("Unmatched Sells", f"{unmatched_sell_qty} shares")
        
        st.divider()
        
        # Fee calculations
        st.markdown("### 💰 Fee Breakdown")
        
        # STL (Share Transaction Levy) - 0.30% - Applied to ALL transactions
        STL_RATE = 0.30 / 100
        TRANSACTION_FEE_RATE = (FEE_PERCENTAGE - 0.30) / 100  # 0.82% (1.12% - 0.30% STL)
        
        # Buy side fees
        # Full fee on unmatched buys, only STL on matched buys
        buy_transaction_fee_unmatched = unmatched_buy_qty * weighted_avg_buy_price * TRANSACTION_FEE_RATE
        buy_stl_all = total_buy_qty * weighted_avg_buy_price * STL_RATE  # STL on all buys
        total_buy_fees = buy_transaction_fee_unmatched + buy_stl_all
        
        # Sell side fees
        # Full fee on unmatched sells, only STL on matched sells
        sell_transaction_fee_unmatched = unmatched_sell_qty * weighted_avg_sell_price * TRANSACTION_FEE_RATE
        sell_stl_all = total_sell_qty * weighted_avg_sell_price * STL_RATE  # STL on all sells
        total_sell_fees = sell_transaction_fee_unmatched + sell_stl_all
        
        # Total fees
        total_fees = total_buy_fees + total_sell_fees
        
        # Calculate costs
        total_cost_with_fees = total_buy_value + total_buy_fees
        proceeds_after_fees = total_sell_value - total_sell_fees
        
        # Net P&L
        net_pl = proceeds_after_fees - total_cost_with_fees
        net_pl_pct = (net_pl / total_cost_with_fees * 100) if total_cost_with_fees > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Buy Fees", f"Rs. {total_buy_fees:.2f}",
                     help=f"Transaction fee on {unmatched_buy_qty} unmatched + STL on all {total_buy_qty}")
        
        with col2:
            st.metric("Sell Fees", f"Rs. {total_sell_fees:.2f}",
                     help=f"Transaction fee on {unmatched_sell_qty} unmatched + STL on all {total_sell_qty}")
        
        with col3:
            st.metric("Total Fees", f"Rs. {total_fees:.2f}")
        
        with col4:
            fee_saved = (matched_qty * weighted_avg_buy_price * TRANSACTION_FEE_RATE) + \
                       (matched_qty * weighted_avg_sell_price * TRANSACTION_FEE_RATE)
            st.metric("Fees Saved (Intraday)", f"Rs. {fee_saved:.2f}",
                     help="Transaction fees waived on matched quantity")
        
        st.divider()
        
        # P&L Summary
        st.markdown("### 📈 Profit/Loss Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cost (with fees)", f"Rs. {total_cost_with_fees:.2f}")
        
        with col2:
            st.metric("Proceeds (after fees)", f"Rs. {proceeds_after_fees:.2f}")
        
        with col3:
            if net_pl >= 0:
                st.metric("Net P&L", f"Rs. {net_pl:.2f}", 
                         delta=f"+{net_pl_pct:.2f}%")
            else:
                st.metric("Net P&L", f"Rs. {net_pl:.2f}", 
                         delta=f"{net_pl_pct:.2f}%", 
                         delta_color="inverse")
        
        st.divider()
        
        # Detailed breakdown
        with st.expander("🔍 Detailed Fee Calculation"):
            st.markdown(f"""
            **CSE Intraday Fee Structure:**
            - **Transaction Fee (excluding STL)**: 0.82% (Brokerage + SEC + CSE + CDS)
            - **Share Transaction Levy (STL)**: 0.30%
            - **Total Normal Fee**: 1.12%
            
            **Your Trades:**
            - Total Buys: {total_buy_qty} shares @ avg Rs. {weighted_avg_buy_price:.2f}
            - Total Sells: {total_sell_qty} shares @ avg Rs. {weighted_avg_sell_price:.2f}
            - **Matched Quantity**: {matched_qty} shares (intraday exemption applies)
            
            **Buy Side Fee Calculation:**
            - Unmatched quantity: {unmatched_buy_qty} shares
            - Transaction fee on unmatched: Rs. {unmatched_buy_qty * weighted_avg_buy_price:.2f} × 0.82% = Rs. {buy_transaction_fee_unmatched:.2f}
            - STL on ALL buys: Rs. {total_buy_value:.2f} × 0.30% = Rs. {buy_stl_all:.2f}
            - **Total Buy Fees: Rs. {total_buy_fees:.2f}**
            
            **Sell Side Fee Calculation:**
            - Unmatched quantity: {unmatched_sell_qty} shares
            - Transaction fee on unmatched: Rs. {unmatched_sell_qty * weighted_avg_sell_price:.2f} × 0.82% = Rs. {sell_transaction_fee_unmatched:.2f}
            - STL on ALL sells: Rs. {total_sell_value:.2f} × 0.30% = Rs. {sell_stl_all:.2f}
            - **Total Sell Fees: Rs. {total_sell_fees:.2f}**
            
            **Matched Quantity Benefit:**
            - On {matched_qty} matched shares, you save the 0.82% transaction fee
            - You still pay STL (0.30%) on matched shares
            - Total fee saved: Rs. {fee_saved:.2f}
            
            **Final P&L:**
            - Total Cost: Rs. {total_buy_value:.2f} + Rs. {total_buy_fees:.2f} = Rs. {total_cost_with_fees:.2f}
            - Proceeds: Rs. {total_sell_value:.2f} - Rs. {total_sell_fees:.2f} = Rs. {proceeds_after_fees:.2f}
            - **Net P&L: Rs. {net_pl:.2f} ({net_pl_pct:.2f}%)**
            """)
        
        # Example comparison
        with st.expander("💡 Fee Comparison: Intraday vs Multi-Day"):
            # Calculate what fees would be if this was multi-day
            full_buy_fees = total_buy_value * (FEE_PERCENTAGE / 100)
            full_sell_fees = total_sell_value * (FEE_PERCENTAGE / 100)
            multiday_total_fees = full_buy_fees + full_sell_fees
            savings = multiday_total_fees - total_fees
            
            st.markdown(f"""
            **If these were Multi-Day trades (no exemption):**
            - Buy fees: Rs. {total_buy_value:.2f} × 1.12% = Rs. {full_buy_fees:.2f}
            - Sell fees: Rs. {total_sell_value:.2f} × 1.12% = Rs. {full_sell_fees:.2f}
            - Total fees: Rs. {multiday_total_fees:.2f}
            
            **Your Intraday fees:**
            - Total fees: Rs. {total_fees:.2f}
            
            **💰 You saved: Rs. {savings:.2f}** by doing intraday trading!
            """)
    
    else:
        st.info("👆 Add buy and sell trades to see the analysis")
        
        st.markdown("""
        **How to use this calculator:**
        1. Add all your BUY trades for the day (quantity and price for each)
        2. Add all your SELL trades for the day (quantity and price for each)
        3. The calculator will:
           - Match buy and sell quantities
           - Apply CSE intraday fee exemption on matched shares
           - Calculate fees only on unmatched quantities (except STL)
           - Show your total P&L with fee breakdown
        
        **Example scenarios:**
        - **Client X**: Bought 5,000 shares, Sold 4,000 shares → Fee exemption on 4,000 shares
        - **Client Y**: Bought 900 shares, Sold 1,500 shares → Fee exemption on 900 shares
        """)
