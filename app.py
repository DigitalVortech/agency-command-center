import streamlit as st
from streamlit_option_menu import option_menu # NEW LIBRARY
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
}

# --- 2. APP SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Growth Dashboard", page_icon="⚡", layout="wide")

# Custom CSS for a "SaaS Platform" look
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1E293B;
        }
        
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Card Styling */
        .metric-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        
        /* Custom Button Styling */
        .stButton button {
            background-color: #0F172A;
            color: white;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            padding: 10px 20px;
            transition: all 0.2s;
        }
        .stButton button:hover {
            background-color: #334155;
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    # App Logo / Title
    st.markdown("### ⚡ AgencyOS")
    
    # Client Selector
    selected_client_name = st.selectbox("Select Client", list(CLIENTS.keys()))
    st.markdown("---")
    
    # PRO NAVIGATION MENU (No more emojis)
    selected = option_menu(
        menu_title="Main Menu",
        options=["Review Generator", "Rank Checker", "Competitors", "Lead Scavenger"],
        icons=["star-fill", "geo-alt-fill", "trophy-fill", "search"], # BOOTSTRAP ICONS
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8f9fa"},
            "icon": {"color": "#0066cc", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eef2ff"},
            "nav-link-selected": {"background-color": "#0F172A"},
        }
    )
    
    st.markdown("---")
    st.caption("v2.1 | Enterprise Edition")

data = CLIENTS[selected_client_name]

# --- 4. MAIN CONTENT AREA ---

# HEADER
st.markdown(f"## {selected_client_name}")
st.markdown(f"**Dashboard** > *{selected}*")
st.write("") # Spacer

# --- PAGE 1: REVIEW GENERATOR ---
if selected == "Review Generator":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Request a Review")
    st.info("💡 Pro Tip: Send this while you are still physically at the job site.")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="Jane Doe")
    with col2:
        service_type = st.selectbox("Service Type", data["services"])

    if customer_name:
        link = data["review_link"]
        message_text = (
            f"Hi {customer_name}! Thanks for choosing {selected_client_name}. "
            f"We are trying to grow our local business and a quick 5-star rating helps us a ton. "
            f"Link: {link}"
        )
        st.code(message_text, language=None)
        encoded_msg = urllib.parse.quote(message_text)
        
        # Professional "Action" Button
        st.markdown(f'''
            <a href="sms:?&body={encoded_msg}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#22C55E; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold; box-shadow: 0 4px 6px rgba(34, 197, 94, 0.3);">
                    📨 Send Text Message Now
                </div>
            </a>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2: RANK CHECKER ---
if selected == "Rank Checker":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Live Rank Verification")
    
    target_keyword = st.text_input("Search Keyword", value=data["services"][0])
    st.write("Click a location to simulate a customer search:")
    
    cols = st.columns(3)
    for index, (name, location_query) in enumerate(data["locations"].items()):
        query = f"{target_keyword} in {location_query}"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        with cols[index % 3]:
            st.link_button(f"🔎 {name}", search_url, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 3: COMPETITORS ---
if selected == "Competitors":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Market Share Analysis")
    
    my_name = list(data["competitors"].keys())[0]
    my_reviews = data["competitors"][my_name]
    leader_reviews = max(data["competitors"].values())
    gap = leader_reviews - my_reviews
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Your Reviews", f"{my_reviews}")
    m2.metric("Market Leader", f"{leader_reviews}")
    m3.metric("Gap to Leader", f"{gap}", delta_color="inverse")
    
    st.bar_chart(data["competitors"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 4: LEAD SCAVENGER ---
if selected == "Lead Scavenger":
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Social Listening Tool")
    
    if "fb_groups" in data:
        keywords = ["recommend", "looking for", "needed"]
        for group_name, group_id in data["fb_groups"].items():
            st.markdown(f"**{group_name}**")
            
            # Grid of nice pill-shaped buttons
            c1, c2, c3 = st.columns(3)
            for i, kw in enumerate(keywords):
                full_search = f"{data['services'][0]} {kw}"
                magic_suffix = "&filters=eyJzb3J0aW5nIjoie1widmFsdWVcIjpcImNocm9ub19kZXNjZW5kaW5nXCJ9In0%3D"
                encoded_kw = urllib.parse.quote(full_search)
                url = f"https://www.facebook.com/groups/{group_id}/search/?q={encoded_kw}{magic_suffix}"
                
                if i == 0:
                    with c1: st.link_button(f"Find '{kw}'", url, use_container_width=True)
                if i == 1:
                    with c2: st.link_button(f"Find '{kw}'", url, use_container_width=True)
                if i == 2:
                    with c3: st.link_button(f"Find '{kw}'", url, use_container_width=True)
            st.write("")
    st.markdown('</div>', unsafe_allow_html=True)
