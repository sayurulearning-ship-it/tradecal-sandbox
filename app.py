import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="CalqTrade", page_icon="🪙", layout="wide")

# Fee percentage
FEE_PERCENTAGE = 1.12

# Create tabs
tab1, tab2 = st.tabs(["💹 Single Trade Calculator", "⚖️ Break-Even Calculator"])

# ==================== TAB 1: Original Calculator ====================
with tab1:
    # Title and description
    st.title("🪙 CalqTrade")
    st.markdown("Calculate trading profits with transaction fees")

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
    
    # STL Rate (Share Transaction Levy)
    STL_RATE = 0.30 / 100
    
    # Step 2: Calculate B.E.S Price (Break-Even Sell Price)
    if same_day == "Same Day Trading":
        # For same day: Only STL (0.30%) on sell, no other transaction fees
        # B.E.S Price needs to cover: Total Cost + STL on sell
        # Total Cost = (B.E.S Price × Qty) - (B.E.S Price × Qty × 0.003)
        # Total Cost = B.E.S Price × Qty × (1 - 0.003)
        # B.E.S Price = Total Cost / (Qty × (1 - 0.003))
        bes_price = total_cost / (quantity * (1 - STL_RATE))
        # Calculate actual sell fee (only STL) based on sell price
        sell_fee = sell_price * quantity * STL_RATE if sell_price > 0 else 0
    else:
        # For another day: B.E.S = Avg Price × 1.0112
        bes_price = avg_price * (1 + FEE_PERCENTAGE / 100)
        # Calculate sell fee based on sell price
        sell_fee = sell_price * quantity * (FEE_PERCENTAGE / 100) if sell_price > 0 else 0
    
    # Step 3: Calculate proceeds from selling
    total_sell_value = sell_price * quantity
    proceeds = total_sell_value - sell_fee
    fee_count = "Buy: 1.12%, Sell: 0.30% (STL only)" if same_day == "Same Day Trading" else "2x (buy 1.12% + sell 1.12%)"

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
            st.metric("Sell Fee (STL 0.30%)", f"Rs. {sell_fee:.2f}", help="Only STL charged on same day sell")
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
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"+{gain_loss_percentage:.2f}%", delta_color="normal")
        else:
            st.metric("Return %", f"{gain_loss_percentage:.2f}%", delta=f"{gain_loss_percentage:.2f}%", delta_color="inverse")

    with col3:
        total_fees = buy_fee + sell_fee
        st.metric("Total Fees", f"Rs. {total_fees:.2f}", help=f"Fee charged {fee_count}")

    st.markdown("")
    st.markdown("")
    
    st.info(f"""
    **Fee Structure:**
    - Transaction Fee: **{FEE_PERCENTAGE}%** (includes 0.82% brokerage + 0.30% STL)
    - Same Day Trading: Buy fee **1.12%**, Sell fee **0.30% (STL only)**
    - Sell on Another Day: Fee charged **twice** (1.12% on buy and 1.12% on sell)
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
        {f"- B.E.S = Total Cost ÷ (Qty × 0.997) - includes 0.30% STL on sell" if same_day == 'Same Day Trading' else f"- B.E.S = Avg Price × 1.0112 = Rs. {avg_price:.4f} × 1.0112"}
        - Price Move Needed: Rs. {price_move_needed:.4f} ({((price_move_needed / buy_price) * 100):.2f}% from buy price)
        
        **Sell Transaction:**
        - Sell Price: Rs. {sell_price:.2f}
        - Quantity: {quantity} stocks
        - Total Sell Value: Rs. {total_sell_value:.2f}
        - Sell Fee: Rs. {sell_fee:.2f} {'(STL 0.30% only - same day)' if same_day == 'Same Day Trading' else f'({FEE_PERCENTAGE}% - full fee)'}
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
    st.title("🪙 CalqTrade")
    st.markdown("Calculate B.E.S Price (Break-Even Sell Price) from buy price")
    
    st.subheader("Input Details")
    
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
    # STL Rate (Share Transaction Levy)
    STL_RATE = 0.30 / 100
    
    if be_same_day == "Same Day Trading":
        # For same day: Only STL (0.30%) on sell
        # B.E.S Price = Total Cost / (Qty × (1 - 0.003))
        be_bes_price = be_total_cost / (be_quantity * (1 - STL_RATE))
        be_sell_fee = be_bes_price * be_quantity * STL_RATE
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
            st.metric("Sell Fee (STL)", f"Rs. {be_sell_fee:.2f}", 
                     help="STL 0.30% on same day sell")
        else:
            st.metric("Sell Fee at B.E.S", f"Rs. {be_sell_fee:.2f}",
                     help=f"Sell fee when selling at B.E.S price")
    
    st.divider()
    
    # Profit targets
    st.markdown("### 🎯 Profit Target Scenarios")
    st.markdown("Calculate sell prices for different profit targets:")
    
    profit_targets = [0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
    
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
    {f"- Formula: Total Cost ÷ (Qty × 0.997) - includes 0.30% STL on sell" if be_same_day == 'Same Day Trading' else f"- Avg Price × 1.0112 = Rs. {be_avg_price:.4f} × 1.0112"}
    - Needs **{be_percentage_move_from_buy:.2f}%** increase from buy price
    
    **Total Cost: Rs. {be_total_cost:.2f}**
    - This is what you need to recover to break even
    
    **Fee Structure:**
    {f"- Same Day: Buy 1.12%, Sell 0.30% (STL only)" if be_same_day == 'Same Day Trading' else f"- Multi-Day: Buy 1.12%, Sell 1.12% (full fees)"}
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
        {'- For Same Day: B.E.S Price = Total Cost ÷ (Qty × 0.997)' if be_same_day == 'Same Day Trading' else f'- For Another Day: B.E.S Price = Avg Price × 1.0112'}
        {'- Accounts for 0.30% STL on sell' if be_same_day == 'Same Day Trading' else f'- B.E.S Price = Rs. {be_avg_price:.4f} × 1.0112'}
        - **B.E.S Price = Rs. {be_bes_price:.4f}**
        
        **Step 4: Price Movement Analysis**
        - From Buy Price: Rs. {be_bes_price:.4f} - Rs. {be_buy_price:.2f} = Rs. {be_price_increase_from_buy:.4f}
        - **Percentage Move: {be_percentage_move_from_buy:.2f}%**
        
        **Key Formula:**
        ```
        Avg Price = (Buy Price × Qty + Buy Fee) ÷ Qty
        Total Cost = Avg Price × Qty
        {'B.E.S Price = Total Cost ÷ (Qty × 0.997) [same day - includes STL]' if be_same_day == 'Same Day Trading' else 'B.E.S Price = Avg Price × 1.0112 [another day - full fees]'}
        ```
        """)
