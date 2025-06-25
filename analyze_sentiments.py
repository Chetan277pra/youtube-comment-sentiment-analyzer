from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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


# Example test run:
if __name__ == "__main__":
    
    from fetch_youtube_comments import get_comments
    
    VIDEO_ID = "JgDNFQ2RaLQ"
    API_KEY = "AIzaSyBIRKeeHFhobSvDQPZLipHn3Qpv-FA7xVU"
    
    comments = get_comments(VIDEO_ID, API_KEY)
    analyzed = analyze_sentiments(comments)
    
    for i, (comment, sentiment, score) in enumerate(analyzed, 1):
        print(f"{i}. [{sentiment} | Score: {score:.2f}] → {comment}")
