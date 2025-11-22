import streamlit as st
import urllib.parse

# --- 1. CONFIGURATION & DATA ---
CLIENTS = {
    "Prime Shine Cleaning": {
        "review_link": "https://g.page/r/YOUR_PRIME_SHINE_LINK/review",
        "services": ["House Clean", "Move-out Clean", "Deep Clean"],
        "competitors": {"Prime Shine": 16, "Maids of Movher": 151, "Live Clean Today": 70},
        "locations": {
            "Mead": "Mead, WA",
            "North Spokane": "North Spokane, WA",
            "South Hill": "South Hill, Spokane, WA"
        },
        "fb_groups": {
             "Spokane Mom's": "123456789", 
             "Mead Community": "987654321"
        }
    }
    # Add more clients here...
}

# --- 2. APP SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Growth Dashboard", page_icon="✨", layout="centered")

# This is the Magic CSS Block
st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #F5F7F9; /* Light Grey Background */
            color: #1E293B;
        }

        /* HIDE Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* CARD STYLE: White box with shadow */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E2E8F0;
        }

        /* BUTTONS: Modern Gradient */
        .stButton button {
            background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        .stButton button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }

        /* LINK BUTTONS (Facebook/Google) */
        a {
            text-decoration: none !important;
        }

        /* HEADERS */
        h1, h2, h3 {
            color: #0F172A;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR (Client Selector) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920323.png", width=50) # Generic Rocket Icon
    st.header("Agency Controls")
    selected_client_name = st.selectbox("Active Client", list(CLIENTS.keys()))
    st.info(f"Viewing data for: **{selected_client_name}**")
    st.markdown("---")
    st.caption("v2.0 | Automated Growth System")

data = CLIENTS[selected_client_name]

# --- 4. MAIN INTERFACE ---
# Modern Header
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="margin:0;">{selected_client_name}</h1>
        <p style="color: #64748B; font-size: 14px;">Growth Command Center</p>
    </div>
""", unsafe_allow_html=True)

# Tabs with Icons
tab1, tab2, tab3, tab4 = st.tabs(["⭐ Reviews", "📍 Rankings", "🏆 Market", "🕵️ Leads"])

# --- TAB 1: REVIEWS ---
with tab1:
    st.markdown("### 📝 Request a Review")
    st.caption("Send this immediately after a job closes.")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="e.g. Sarah")
    with col2:
        service_type = st.selectbox("Service", data["services"])

    if customer_name:
        link = data["review_link"]
        message_text = (
            f"Hi {customer_name}! Thanks for choosing {selected_client_name}. "
            f"We are trying to grow our local business and a quick 5-star rating helps us a ton. "
            f"Link: {link}"
        )
        
        # Display the script in a nice grey box
        st.success("Script Generated:")
        st.code(message_text, language=None)
        
        encoded_msg = urllib.parse.quote(message_text)
        
        # Custom HTML Button for SMS
        st.markdown(f'''
            <a href="sms:?&body={encoded_msg}" target="_blank">
                <div style="
                    background-color: #22C55E;
                    color: white;
                    padding: 12px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                    margin-top: 10px;
                    cursor: pointer;
                    box-shadow: 0 4px 6px rgba(34, 197, 94, 0.2);
                ">
                    📱 Open Text Message App
                </div>
            </a>
        ''', unsafe_allow_html=True)

# --- TAB 2: RANKINGS ---
with tab2:
    st.markdown("### 📍 Visual Rank Checker")
    st.caption("See what your customers see in different neighborhoods.")
    
    target_keyword = st.text_input("Search Term", value=data["services"][0])
    
    st.write("") # Spacer
    
    cols = st.columns(3)
    for index, (name, location_query) in enumerate(data["locations"].items()):
        query = f"{target_keyword} in {location_query}"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        with cols[index % 3]:
            # Using Streamlit's link_button but styled via CSS above
            st.link_button(f"🔍 Check {name}", search_url)

# --- TAB 3: MARKET SHARE ---
with tab3:
    st.markdown("### 🏆 Competitor Scoreboard")
    
    my_name = list(data["competitors"].keys())[0]
    my_reviews = data["competitors"][my_name]
    leader_reviews = max(data["competitors"].values())
    gap = leader_reviews - my_reviews
    
    # 3-Column Metric Display
    m1, m2, m3 = st.columns(3)
    m1.metric("Our Reviews", f"{my_reviews}", delta="Manual Update")
    m2.metric("Market Leader", f"{leader_reviews}")
    m3.metric("Gap to Close", f"{gap}", delta_color="inverse")
    
    st.bar_chart(data["competitors"])
    
    if gap > 0:
        st.warning(f"🚀 We need **{gap}** more reviews to catch the leader.")
    else:
        st.balloons()
        st.success("🎉 You are the Market Leader!")

# --- TAB 4: LEADS ---
with tab4:
    st.markdown("### 🕵️ Social Scavenger")
    st.caption("Find intent-based leads in local groups instantly.")
    
    if "fb_groups" in data:
        keywords = ["recommend", "looking for", "needed"]
        
        for group_name, group_id in data["fb_groups"].items():
            st.markdown(f"#### 👥 {group_name}")
            
            c1, c2, c3 = st.columns(3)
            # Create a button for each keyword
            for i, kw in enumerate(keywords):
                full_search = f"{data['services'][0]} {kw}"
                magic_suffix = "&filters=eyJzb3J0aW5nIjoie1widmFsdWVcIjpcImNocm9ub19kZXNjZW5kaW5nXCJ9In0%3D"
                encoded_kw = urllib.parse.quote(full_search)
                url = f"https://www.facebook.com/groups/{group_id}/search/?q={encoded_kw}{magic_suffix}"
                
                # Place buttons in columns
                if i == 0: with c1: st.link_button(f"Find '{kw}'", url)
                if i == 1: with c2: st.link_button(f"Find '{kw}'", url)
                if i == 2: with c3: st.link_button(f"Find '{kw}'", url)
            
            st.markdown("---")
