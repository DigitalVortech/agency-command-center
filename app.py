import streamlit as st
import urllib.parse

# --- 1. AGENCY DATABASE (Add all your clients here) ---
CLIENTS = {
    "Prime Shine Cleaning": {
        "review_link": "https://g.page/r/YOUR_PRIME_SHINE_LINK/review",
        "services": ["House Clean", "Move-out Clean", "Deep Clean"],
        "competitors": {
            "Prime Shine": 16, 
            "Maids of Movher": 151, 
            "Live Clean Today": 70
        },
        "locations": {
            "Mead": "Mead, WA",
            "North Spokane": "North Spokane, WA",
            "South Hill": "South Hill, Spokane, WA"
        },
        # Add Group IDs here (Find these in the URL: facebook.com/groups/123456/)
        "fb_groups": {
             "Spokane Mom's": "123456789", 
             "Mead Community": "987654321"
        }
    },
    "Spotless Window Washing": {
        "review_link": "https://g.page/r/YOUR_WINDOW_LINK/review",
        "services": ["Window Cleaning", "Gutter Cleaning", "Pressure Washing"],
        "competitors": {
            "Spotless Windows": 5, 
            "Pane in the Glass": 45, 
            "Spokane Window Pro": 88
        },
        "locations": {
            "Spokane Valley": "Spokane Valley, WA",
            "Liberty Lake": "Liberty Lake, WA"
        },
        "fb_groups": {
             "Spokane Swip Swap": "1122334455", 
             "Valley News": "99887766"
        }
    }
}

# --- APP SETUP ---
st.set_page_config(page_title="Agency Command Center", page_icon="🚀")

# --- SIDEBAR: CLIENT SELECTOR ---
st.sidebar.header("🚀 Agency Controls")
selected_client_name = st.sidebar.selectbox("Select Client Profile", list(CLIENTS.keys()))

# Load the data for the selected client
data = CLIENTS[selected_client_name]

# --- MAIN APP INTERFACE ---
st.title(f"Dashboard: {selected_client_name}")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["⭐⭐ Review Gen", "📍 Rank Check", "🏆 Competitors", "🕵️ Lead Scavenger"])

# --- TAB 1: DYNAMIC REVIEW GENERATOR ---
with tab1:
    st.header("Review Request Tool")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name", placeholder="e.g., John")
    with col2:
        service_type = st.selectbox("Service Performed", data["services"])

    if customer_name:
        link = data["review_link"]
        message_text = (
            f"Hi {customer_name}! Thanks for choosing {selected_client_name} for your {service_type.lower()}. "
            f"We are trying to grow our local business and a quick review helps us a ton. "
            f"Link: {link}"
        )
        st.code(message_text, language=None)
        encoded_msg = urllib.parse.quote(message_text)
        st.markdown(f'''<a href="sms:?&body={encoded_msg}"><button style="background-color:#00CC66;color:white;padding:10px;border:none;border-radius:5px;width:100%">📱 Text {customer_name} Now</button></a>''', unsafe_allow_html=True)

# --- TAB 2: DYNAMIC RANK CHECKER ---
with tab2:
    st.header(f"Rankings for {selected_client_name}")
    target_keyword = st.text_input("Keyword", value=data["services"][0])
    st.write("Select Neighborhood to Scout:")
    cols = st.columns(3)
    for index, (name, location_query) in enumerate(data["locations"].items()):
        query = f"{target_keyword} in {location_query}"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        with cols[index % 3]:
            st.link_button(f"🔍 {name}", search_url)

# --- TAB 3: DYNAMIC SCOREBOARD ---
with tab3:
    st.header("Competitor Analysis")
    my_name = list(data["competitors"].keys())[0]
    my_reviews = data["competitors"][my_name]
    leader_reviews = max(data["competitors"].values())
    col1, col2 = st.columns(2)
    col1.metric("Our Reviews", f"{my_reviews}")
    col2.metric("Market Leader", f"{leader_reviews}")
    st.bar_chart(data["competitors"])

# --- TAB 4: LEAD SCAVENGER ---
with tab4:
    st.header("🕵️ Lead Scavenger")
    st.info("Click to see who is asking for services RIGHT NOW (Sorted by Most Recent).")
    
    keywords = ["recommend", "looking for", "needed", "help"]
    
    if "fb_groups" in data:
        for group_name, group_id in data["fb_groups"].items():
            st.subheader(f"🔎 {group_name}")
            # Create grid for buttons
            cols = st.columns(len(keywords))
            for i, kw in enumerate(keywords):
                # Combine client service with search term (e.g., "window cleaning needed")
                full_search = f"{data['services'][0]} {kw}"
                
                # Magic suffix for "Most Recent" filter
                magic_suffix = "&filters=eyJzb3J0aW5nIjoie1widmFsdWVcIjpcImNocm9ub19kZXNjZW5kaW5nXCJ9In0%3D"
                encoded_kw = urllib.parse.quote(full_search)
                search_url = f"https://www.facebook.com/groups/{group_id}/search/?q={encoded_kw}{magic_suffix}"
                
                with cols[i]:
                    st.link_button(f"Find '{kw}'", search_url)
    else:

        st.warning("No Facebook Groups added for this client yet.")
