import pandas as pd
import datetime
import schedule
import time
from twittering import post_on_twitter
from zipfile import ZipFile


SPREADSHEET_PATH = "Blog_Schedule.csv"


def create_spreadsheet(post_data):
    df = pd.DataFrame(post_data)
    datetime_list = []

    start_date = datetime.date.today()
    for i in range(len(post_data)):
        date = start_date + datetime.timedelta(days=i * 2)
        datetime_list.append(str(date))

    df['date to post'] = datetime_list
    df['posted'] = False
    df = df.reindex(columns=['date to post', 'posted', 'content', 'image'])

    df.to_csv(SPREADSHEET_PATH, index=False)
    with ZipFile('output.zip', 'a') as myzip:
        myzip.write(SPREADSHEET_PATH)

    return df


def post_scheduled_blogs():
    df = pd.read_csv(SPREADSHEET_PATH)
    today = str(datetime.date.today())
    response = ""

    for index, row in df.iterrows():
        if row["posted"] == False and row["date to post"] == today:
            try:
                response = post_on_twitter(row['content'], row['image'])
                df.at[index, "posted"] = True

            except Exception as e:
                response = f"Error posting: {e}"

    df.to_csv(SPREADSHEET_PATH, index=False)
    return response


def run_schedule(time_to_post):
    schedule.every().day.at(time_to_post).do(post_scheduled_blogs)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    post_dict = [
        {'content': "Simon Sinek on a YouTube podcast highlights the irony of AI job displacement",
         'image': 'Post Images\\image_0.png'},
        {'content': "Simon Sinek perfectly captures the AI paradox (YouTube podcast)",
         'image': 'Post Images\\image_1.png'},
        {'content': "Simon Sinek on a YouTube podcast nails the problem with perfect AI responses",
         'image': 'Post Images\\image_2.png'}]

    create_spreadsheet(post_dict)
    run_schedule("01:13")
