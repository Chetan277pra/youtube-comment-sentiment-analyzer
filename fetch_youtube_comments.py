from googleapiclient.discovery import build

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


# Example usage:
if __name__ == "__main__":
    VIDEO_ID = "JgDNFQ2RaLQ"
    API_KEY = "AIzaSyBIRKeeHFhobSvDQPZLipHn3Qpv-FA7xVU"
    
    comments = get_comments(VIDEO_ID, API_KEY)
    for i, comment in enumerate(comments, start=1):
        print(f"{i}. {comment}")
