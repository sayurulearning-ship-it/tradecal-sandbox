import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Trading Calculator", page_icon="📊", layout="wide")

# Initialize session state for storing positions
if 'positions' not in st.session_state:
    st.session_state.positions = []

# Fee percentage
FEE_PERCENTAGE = 1.12

# Create tabs
tab1, tab2 = st.tabs(["💹 Single Trade Calculator", "📋 Position Tracker"])

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

    # Calculations
    if same_day == "Same Day Trading":
        total_buy_value = buy_price * quantity
        buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
        total_cost = total_buy_value + buy_fee
        
        total_sell_value = sell_price * quantity
        sell_fee = 0
        proceeds = total_sell_value
        fee_count = "1x"
    else:
        total_buy_value = buy_price * quantity
        buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
        total_cost = total_buy_value + buy_fee
        
        total_sell_value = sell_price * quantity
        sell_fee = total_sell_value * (FEE_PERCENTAGE / 100)
        proceeds = total_sell_value - sell_fee
        fee_count = "2x"

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
        """)

# ==================== TAB 2: Position Tracker & Real-time P&L ====================
with tab2:
    st.title("📋 Multi-Position Tracker")
    st.markdown("Track multiple positions and monitor real-time P&L")
    
    # Add new position section
    st.subheader("➕ Add New Position")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stock_name = st.text_input("Stock Symbol", value="STOCK", key="pos_stock")
    
    with col2:
        pos_buy_price = st.number_input("Buy Price", min_value=0.0, value=100.0, step=1.0, format="%.2f", key="pos_buy")
    
    with col3:
        pos_quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="pos_qty")
    
    with col4:
        pos_same_day = st.selectbox("Type", ["Same Day", "Another Day"], key="pos_type")
    
    with col5:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Position", use_container_width=True):
            # Calculate buy details
            total_buy_value = pos_buy_price * pos_quantity
            buy_fee = total_buy_value * (FEE_PERCENTAGE / 100)
            total_cost = total_buy_value + buy_fee
            
            position = {
                'stock': stock_name,
                'buy_price': pos_buy_price,
                'quantity': pos_quantity,
                'type': pos_same_day,
                'total_cost': total_cost,
                'buy_fee': buy_fee,
                'time_added': datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.positions.append(position)
            st.success(f"✅ Added {stock_name} position!")
            st.rerun()
    
    st.divider()
    
    # Display positions
    if len(st.session_state.positions) > 0:
        st.subheader("📊 Active Positions")
        
        # Create DataFrame for display
        positions_data = []
        total_invested = 0
        total_current_value = 0
        total_fees_paid = 0
        
        for idx, pos in enumerate(st.session_state.positions):
            col1, col2, col3, col4 = st.columns([2, 3, 3, 1])
            
            with col1:
                st.markdown(f"### {pos['stock']}")
                st.caption(f"Added: {pos['time_added']}")
            
            with col2:
                st.metric("Buy Price", f"Rs. {pos['buy_price']:.2f}")
                st.metric("Quantity", f"{pos['quantity']}")
                st.caption(f"Type: {pos['type']}")
            
            with col3:
                st.metric("Total Cost", f"Rs. {pos['total_cost']:.2f}")
                st.metric("Buy Fee", f"Rs. {pos['buy_fee']:.3f}")
                
                # Real-time P&L calculator
                current_price = st.number_input(
                    f"Current Price",
                    min_value=0.0,
                    value=pos['buy_price'],
                    step=0.1,
                    format="%.2f",
                    key=f"current_price_{idx}"
                )
                
                # Calculate unrealized P&L
                current_value = current_price * pos['quantity']
                if pos['type'] == "Same Day":
                    sell_fee = 0
                    proceeds = current_value
                else:
                    sell_fee = current_value * (FEE_PERCENTAGE / 100)
                    proceeds = current_value - sell_fee
                
                unrealized_pl = proceeds - pos['total_cost']
                unrealized_pl_pct = (unrealized_pl / pos['total_cost']) * 100
                
                if unrealized_pl >= 0:
                    st.metric("Unrealized P&L", f"Rs. {unrealized_pl:.2f}", delta=f"+{unrealized_pl_pct:.2f}%")
                else:
                    st.metric("Unrealized P&L", f"Rs. {unrealized_pl:.2f}", delta=f"{unrealized_pl_pct:.2f}%", delta_color="inverse")
                
                # Update totals
                total_invested += pos['total_cost']
                total_current_value += proceeds
                total_fees_paid += pos['buy_fee'] + sell_fee
            
            with col4:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_{idx}", help="Remove position"):
                    st.session_state.positions.pop(idx)
                    st.rerun()
            
            st.divider()
        
        # Aggregate summary
        st.subheader("💼 Portfolio Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Positions", len(st.session_state.positions))
        
        with col2:
            st.metric("Total Invested", f"Rs. {total_invested:.2f}")
        
        with col3:
            st.metric("Current Value", f"Rs. {total_current_value:.2f}")
        
        with col4:
            total_pl = total_current_value - total_invested
            total_pl_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0
            if total_pl >= 0:
                st.metric("Total P&L", f"Rs. {total_pl:.2f}", delta=f"+{total_pl_pct:.2f}%")
            else:
                st.metric("Total P&L", f"Rs. {total_pl:.2f}", delta=f"{total_pl_pct:.2f}%", delta_color="inverse")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Fees Paid", f"Rs. {total_fees_paid:.2f}")
        
        with col2:
            net_pl = total_pl
            st.metric("Net Profit/Loss", f"Rs. {net_pl:.2f}")
        
        st.divider()
        
        # Clear all button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Clear All Positions", use_container_width=True):
                st.session_state.positions = []
                st.rerun()
    
    else:
        st.info("👆 Add your first position to start tracking!")
        st.markdown("""
        **How to use:**
        1. Enter stock symbol and buy details
        2. Add position to tracker
        3. Update current price to see real-time P&L
        4. Track multiple positions simultaneously
        """)
