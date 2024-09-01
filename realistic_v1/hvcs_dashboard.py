import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import base64

HCVS_API_URL = "http://localhost:8000/v1"

def get_logo_svg():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <rect width="100" height="100" fill="#f0f0f0"/>
      <g transform="translate(50,50) scale(0.7)">
        <path d="M0 -40 L-20 -15 L-10 -15 L-20 5 L-10 5 L-30 30 L-10 30 L-20 60 L20 60 L10 30 L30 30 L10 5 L20 5 L10 -15 L20 -15 Z" fill="black"/>
        <rect x="-5" y="60" width="10" height="20" fill="black"/>
      </g>
    </svg>
    """

def main():
    st.set_page_config(page_title="DarkForest Admin Dashboard", layout="wide")
    # Convert SVG to a data URL
    icon_svg = get_logo_svg()
    icon_base64 = base64.b64encode(icon_svg.encode('utf-8')).decode('utf-8')
    icon_url = f"data:image/svg+xml;base64,{icon_base64}"

    # Display the logo in the sidebar
    st.sidebar.image(icon_url, width=100)
    st.title("Human Content Verification System Dashboard")

    st.sidebar.title("DarkForest Admin")
    page = st.sidebar.radio("Go to", ["Overview", "Content Analysis", "User Management", "Blockchain Explorer"])

    if page == "Overview":
        st.header("System Overview")
        
        response = requests.get(f"{HCVS_API_URL}/posts")
        if response.status_code == 200:
            posts = response.json()
            total_posts = len(posts)
            human_posts = sum(1 for post in posts if post['human_score'] > 0.7)
            ai_posts = total_posts - human_posts

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Posts", total_posts)
            col2.metric("Human-Generated", f"{human_posts} ({human_posts/total_posts*100:.1f}%)")
            col3.metric("AI-Generated", f"{ai_posts} ({ai_posts/total_posts*100:.1f}%)")

            st.subheader("Content Verification Trend")
            df = pd.DataFrame(posts)
            df['date'] = pd.to_datetime(df['timestamp'])
            df = df.set_index('date')
            df_daily = df.resample('D').agg({
                'id': 'count',
                'human_score': lambda x: sum(x > 0.7)
            }).rename(columns={'id': 'total_posts', 'human_score': 'human_posts'})
            df_daily['ai_posts'] = df_daily['total_posts'] - df_daily['human_posts']

            fig = px.area(df_daily, y=['human_posts', 'ai_posts'],
                        labels={"value": "Number of Posts", "variable": "Post Type"},
                        title="Content Verification Over Time")
            st.plotly_chart(fig)
        else:
            st.error("Failed to fetch posts. Please try again later.")

    elif page == "Content Analysis":
        st.header("Content Analysis")

        response = requests.get(f"{HCVS_API_URL}/posts")
        if response.status_code == 200:
            posts = response.json()
            
            st.subheader("Recent Posts")
            for post in reversed(posts[-5:]):  # Get last 5 posts
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{post['title']}** by {post['author']}")
                with col2:
                    st.progress(post['human_score'])
                    st.write(f"Human Score: {post['human_score']:.2f}")

            st.subheader("Human Score Distribution")
            scores = [post['human_score'] for post in posts]
            fig = px.histogram(scores, nbins=20, labels={'value': 'Human Score', 'count': 'Number of Posts'},
                            title="Distribution of Human Scores")
            st.plotly_chart(fig)
        else:
            st.error("Failed to fetch posts. Please try again later.")

    elif page == "User Management":
        st.header("User Management")

        response = requests.get(f"{HCVS_API_URL}/creators")
        if response.status_code == 200:
            users = response.json()
            
            st.subheader("Top Contributors")
            top_users = sorted(users, key=lambda x: x['posts_count'], reverse=True)[:5]
            for user in top_users:
                st.write(f"**{user['username']}** - Posts: {user['posts_count']}, Trust Score: {user['trust_score']:.2f}")

            st.subheader("User Trust Scores")
            trust_scores = [user['trust_score'] for user in users]
            fig = px.histogram(trust_scores, nbins=20, labels={'value': 'Trust Score', 'count': 'Number of Users'},
                            title="Distribution of User Trust Scores")
            st.plotly_chart(fig)
        else:
            st.error("Failed to fetch users. Please try again later.")

    elif page == "Blockchain Explorer":
        st.header("Blockchain Explorer")

        response = requests.get(f"{HCVS_API_URL}/blockchain/explore")
        if response.status_code == 200:
            blockchain_data = response.json()
            
            st.subheader("Recent Blocks")
            for block in reversed(blockchain_data['blocks'][-5:]):  # Show last 5 blocks
                with st.expander(f"Block #{block['index']}"):
                    st.json(block)

            st.subheader("Blockchain Health")
            col1, col2, col3 = st.columns(3)
            col1.metric("Chain Length", blockchain_data['chain_length'])
            col2.metric("Last Block Hash", blockchain_data['last_block_hash'][:10] + "...")
            col3.metric("Chain Valid", "Yes" if blockchain_data['is_valid'] else "No")
        else:
            st.error("Failed to fetch blockchain data. Please try again later.")

    st.sidebar.info("This dashboard provides an overview of the Human Content Verification System's performance and data.")

if __name__ == "__main__":
    main()