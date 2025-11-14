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
        buy_price = st.number_input("Buy Price (Avg Price)", min_value=0.0, value=100.0, step=1.0, format="%.4f", key="tab1_buy",
                                   help="This is your average buy price (already includes buy fee)")
        
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
    # Total Cost = Avg Price × Quantity (avg price already includes buy fee)
    total_cost = buy_price * quantity
    
    # Calculate B.E.S Price (Break-Even Sell Price)
    if same_day == "Same Day Trading":
        # For same day: No additional fee, break even at avg price
        bes_price = buy_price
        sell_fee = 0
    else:
        # For another day: Add 1.12% to avg price for sell fee
        bes_price = buy_price * (1 + FEE_PERCENTAGE / 100)
        # Calculate sell fee based on sell price
        sell_fee = sell_price * quantity * (FEE_PERCENTAGE / 100) if sell_price > 0 else 0
    
    # Calculate proceeds from selling
    total_sell_value = sell_price * quantity
    if same_day == "Same Day Trading":
        proceeds = total_sell_value
        fee_count = "1x (included in Avg Price)"
    else:
        proceeds = total_sell_value - sell_fee
        fee_count = "2x (buy fee in Avg Price + sell fee)"

    # Calculate gain/loss
    gain_loss = proceeds - total_cost
    gain_loss_percentage = (gain_loss / total_cost) * 100 if total_cost > 0 else 0

    # Display results
    st.subheader("📈 Calculation Results")

    # Buy section
    st.markdown("### 🟢 Buy Transaction")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Quantity", f"{quantity}")
    with col2:
        st.metric("Avg Price", f"Rs. {buy_price:.4f}", 
                 help="Average buy price (already includes buy fee)")
    with col3:
        st.metric("Total Cost", f"Rs. {total_cost:.2f}")

    # Show B.E.S Price
    col1, col2 = st.columns(2)
    with col1:
        st.metric("B.E.S Price (Break-Even)", f"Rs. {bes_price:.4f}",
                 delta=f"+{((bes_price - buy_price) / buy_price * 100):.2f}%" if bes_price > buy_price else "0.00%",
                 help="Minimum sell price to break even")
    with col2:
        price_move_needed = bes_price - buy_price
        st.metric("Price Move to Break Even", f"Rs. {price_move_needed:.4f}",
                 help="How much price needs to increase from Avg Price")

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
        # Show sell fee only (buy fee already in avg price)
        st.metric("Sell Fee Paid", f"Rs. {sell_fee:.2f}", help=f"Fee charged {fee_count}")

    st.markdown("")
    st.markdown("")
    
    st.info(f"""
    **Fee Structure:**
    - Transaction Fee: **{FEE_PERCENTAGE}%**
    - **Avg Price already includes buy fee** (that's why it's called "Average Price")
    - Same Day Trading: No sell fee needed
    - Sell on Another Day: Sell fee ({FEE_PERCENTAGE}%) charged on sell transaction
    """)

    with st.expander("📋 Detailed Breakdown"):
        st.markdown(f"""
        **Understanding the Pricing:**
        
        **Buy Side:**
        - You bought at: Some original price
        - After buy fee (1.12%), your **Avg Price**: Rs. {buy_price:.4f}
        - Quantity: {quantity} stocks
        - **Total Cost: Rs. {buy_price:.4f} × {quantity} = Rs. {total_cost:.2f}**
        
        **Break-Even Analysis:**
        - Your Avg Price: Rs. {buy_price:.4f}
        - B.E.S Price (Break-Even Sell): Rs. {bes_price:.4f}
        - Price Move Needed: Rs. {price_move_needed:.4f} ({((bes_price - buy_price) / buy_price * 100):.2f}%)
        {f"- For same day: Break even at Avg Price (no sell fee)" if same_day == 'Same Day Trading' else f"- For another day: Need {FEE_PERCENTAGE}% higher to cover sell fee"}
        
        **Sell Transaction:**
        - Sell Price: Rs. {sell_price:.2f}
        - Quantity: {quantity} stocks
        - Total Sell Value: Rs. {total_sell_value:.2f}
        - Sell Fee: Rs. {sell_fee:.2f} {'(No fee - same day)' if same_day == 'Same Day Trading' else f'({FEE_PERCENTAGE}% of sell value)'}
        - **Proceeds: Rs. {proceeds:.2f}**
        
        **Summary:**
        - Total Cost: Rs. {total_cost:.2f}
        - Proceeds: Rs. {proceeds:.2f}
        - **Net Gain/Loss: Rs. {gain_loss:.2f}**
        - **Return on Investment: {gain_loss_percentage:.2f}%**
        
        **Key Formula:**
        - Total Cost = Avg Price × Quantity
        - B.E.S Price = Avg Price × 1.0112 (for another day) OR Avg Price (for same day)
        """)

# ==================== TAB 2: Break-Even Calculator ====================
with tab2:
    st.title("⚖️ Break-Even Calculator")
    st.markdown("Calculate B.E.S Price (Break-Even Sell Price) from your Average Price")
    
    st.subheader("📊 Input Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        be_avg_price = st.number_input("Avg Price", min_value=0.01, value=100.0, step=1.0, format="%.4f", key="be_avg",
                                      help="Your average buy price from the platform (includes buy fee)")
    
    with col2:
        be_quantity = st.number_input("No. of Stocks", min_value=1, value=1, step=1, key="be_qty")
    
    be_same_day = st.radio(
        "Trading Type",
        options=["Same Day Trading", "Sell on Another Day"],
        help="Same day trading: No sell fee. Another day: Sell fee applies.",
        key="be_same_day"
    )
    
    st.divider()
    
    # Calculate break-even with correct formula
    be_total_cost = be_avg_price * be_quantity
    
    if be_same_day == "Same Day Trading":
        # For same day: Break even at avg price (no sell fee)
        be_bes_price = be_avg_price
        be_sell_fee = 0
        be_price_increase = 0
        be_percentage_move = 0
    else:
        # For another day: B.E.S = Avg Price × 1.0112
        be_bes_price = be_avg_price * (1 + FEE_PERCENTAGE / 100)
        be_sell_fee = be_bes_price * be_quantity * (FEE_PERCENTAGE / 100)
        be_price_increase = be_bes_price - be_avg_price
        be_percentage_move = (be_price_increase / be_avg_price) * 100
    
    # Display results
    st.subheader("🎯 Break-Even Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Your Avg Price", f"Rs. {be_avg_price:.4f}",
                 help="Your average buy price (includes buy fee)")
    
    with col2:
        st.metric("B.E.S Price", f"Rs. {be_bes_price:.4f}",
                 delta=f"+{be_percentage_move:.2f}%" if be_percentage_move > 0 else "Break Even Now",
                 help="Break-Even Sell Price")
    
    with col3:
        st.metric("Price Move Needed", f"Rs. {be_price_increase:.4f}",
                 help="Increase needed from Avg Price to break even")
    
    st.divider()
    
    # Cost breakdown
    st.markdown("### 💵 Cost Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cost", f"Rs. {be_total_cost:.2f}",
                 help=f"Avg Price × Quantity = {be_avg_price:.4f} × {be_quantity}")
    
    with col2:
        if be_same_day == "Same Day Trading":
            st.metric("Sell Fee", "Rs. 0.00", help="No sell fee for same day")
        else:
            st.metric("Sell Fee at B.E.S", f"Rs. {be_sell_fee:.2f}",
                     help=f"Sell fee when selling at B.E.S price")
    
    with col3:
        st.metric("Break-Even Proceeds", f"Rs. {be_total_cost:.2f}",
                 help="Amount you'll receive when selling at B.E.S price")
    
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
            # Sell Price × Qty × (1 - 0.0112) = target_proceeds_needed
            target_sell_price = target_proceeds_needed / (be_quantity * (1 - FEE_PERCENTAGE / 100))
        
        # Calculate moves
        price_move = target_sell_price - be_avg_price
        pct_move = (price_move / be_avg_price) * 100
        
        target_data.append({
            'Target Profit %': f"{target_pct}%",
            'Profit Amount': f"Rs. {target_profit:.2f}",
            'Required Sell Price': f"Rs. {target_sell_price:.4f}",
            'Price Increase': f"Rs. {price_move:.4f}",
            'Move from Avg Price': f"+{pct_move:.2f}%"
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
    
    custom_move = custom_sell_price - be_avg_price
    custom_pct_move = (custom_move / be_avg_price) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Required Sell Price", f"Rs. {custom_sell_price:.4f}")
    
    with col2:
        st.metric("Price Increase Needed", f"Rs. {custom_move:.4f}")
    
    with col3:
        st.metric("Move from Avg Price", f"+{custom_pct_move:.2f}%")
    
    st.divider()
    
    # Info box
    st.info(f"""
    **How This Works:**
    
    **Your Avg Price: Rs. {be_avg_price:.4f}**
    - This already includes your buy fee (1.12%)
    - This is your actual cost per share
    
    **B.E.S Price: Rs. {be_bes_price:.4f}**
    - This is where you break even
    {f"- Same as Avg Price (no sell fee for same day)" if be_same_day == 'Same Day Trading' else f"- Avg Price × 1.0112 = Rs. {be_avg_price:.4f} × 1.0112 = Rs. {be_bes_price:.4f}"}
    {f"- No price increase needed!" if be_same_day == 'Same Day Trading' else f"- Needs {be_percentage_move:.2f}% increase to cover sell fee"}
    
    **Total Cost: Rs. {be_total_cost:.2f}**
    - Avg Price × Quantity = Rs. {be_avg_price:.4f} × {be_quantity}
    """)
    
    # Detailed calculation
    with st.expander("🔍 Detailed Break-Even Formula"):
        st.markdown(f"""
        **The Correct Formula (matching your trading platform):**
        
        **Step 1: Understanding Avg Price**
        - When you buy stocks, you pay some original price
        - After buy fee (1.12%), the platform shows you **Avg Price**
        - Your Avg Price: Rs. {be_avg_price:.4f}
        - This already includes the buy fee!
        
        **Step 2: Calculate Total Cost**
        - Total Cost = Avg Price × Quantity
        - Total Cost = Rs. {be_avg_price:.4f} × {be_quantity}
        - **Total Cost = Rs. {be_total_cost:.2f}**
        
        **Step 3: Calculate B.E.S Price (Break-Even Sell)**
        {'- For Same Day: B.E.S Price = Avg Price' if be_same_day == 'Same Day Trading' else f'- For Another Day: B.E.S Price = Avg Price × 1.0112'}
        {'- No sell fee needed for same day trading' if be_same_day == 'Same Day Trading' else f'- B.E.S Price = Rs. {be_avg_price:.4f} × 1.0112'}
        - **B.E.S Price = Rs. {be_bes_price:.4f}**
        
        **Step 4: Price Movement**
        - Price Increase = B.E.S Price - Avg Price
        - Price Increase = Rs. {be_bes_price:.4f} - Rs. {be_avg_price:.4f}
        - **Price Increase = Rs. {be_price_increase:.4f} ({be_percentage_move:.2f}%)**
        
        **Key Insight:**
        - Your platform calculates B.E.S Price by adding {FEE_PERCENTAGE}% to your Avg Price
        - This {FEE_PERCENTAGE}% covers the sell transaction fee
        - Break even when market price reaches B.E.S Price!
        """)
