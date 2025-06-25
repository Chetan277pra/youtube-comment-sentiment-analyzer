import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

# Fetch comments from YouTube
def get_comments(video_id, api_key, max_results=50):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results,
        textFormat='plainText'
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

# Analyze sentiments using VADER
def analyze_sentiments(comments):
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    for comment in comments:
        score = analyzer.polarity_scores(comment)
        compound = score['compound']
        sentiment = (
            'Positive' if compound >= 0.05 else
            'Negative' if compound <= -0.05 else
            'Neutral'
        )
        results.append((comment, sentiment, compound))
    
    return results

# Streamlit UI
st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="centered")
st.title("🎥 YouTube Comment Sentiment Analyzer")

api_key = st.text_input("🔑 Enter your YouTube API Key", type="password")
video_id = st.text_input("📺 Enter YouTube Video ID")

if st.button("Analyze Comments"):
    if not api_key or not video_id:
        st.warning("Please enter both API Key and Video ID.")
    else:
        try:
            with st.spinner("Fetching comments..."):
                comments = get_comments(video_id, api_key)
                results = analyze_sentiments(comments)
            
            st.success(f"Fetched and analyzed {len(results)} comments!")

            for i, (comment, sentiment, score) in enumerate(results, 1):
                st.markdown(f"**{i}. [{sentiment}]** — _Score: {score:.2f}_")
                st.write(comment)
                st.markdown("---")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
