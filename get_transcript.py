from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract


def get_youtube_transcript(video_url):
    video_id = extract.video_id(video_url)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([item['text'] for item in transcript_list])
        return full_transcript, video_id
    except Exception as e:
        return f"Error retrieving transcript: {e}"



if __name__ == "__main__":
    video_url = "https://youtu.be/W4tqbEmplug?si=oZBykixw62l6_E0N"
    transcript = get_youtube_transcript(video_url)
    print(transcript)
