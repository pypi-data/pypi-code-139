import os
from rich import print
from sparrow import rel_to_abs
import shutil
import pandas as pd


def convert():
    input_dir = rel_to_abs('./input', return_str=False)
    output_dir = rel_to_abs('./output', return_str=False)
    for input_i in input_dir.iterdir():
        if input_i.name.endswith((".mp3", ".flac")):
            shutil.move(input_i, os.path.join(output_dir, input_i.name))
    os.system(f"./um-linux-amd64 -i {str(input_dir)} -o {str(output_dir)}")


def get_meta_df():
    from tinytag import TinyTag
    file_dir = rel_to_abs('./output-all', return_str=False)
    artist, title, album, duration, year = [], [], [], [], []
    comment = []
    for i in file_dir.iterdir():
        tag = TinyTag.get(i)
        artist.append(tag.artist)
        title.append(tag.title)
        album.append(tag.album)
        duration.append(tag.duration)
        year.append(tag.year)
        comment.append(tag.comment)
    for idx, i in enumerate(file_dir.iterdir()):
        if not artist[idx] or not title[idx]:
            try:
                title_list = i.name.split(" - ")
                singer, song_name = title_list[0], "".join(title_list[1:])
            except:
                print("----------------")
                print(i)
                print("----------------")
                raise i
            if not artist[idx]:
                artist[idx] = singer
            if not title[idx]:
                title[idx] = song_name
    file_path = [str(i) for i in file_dir.iterdir()]
    meta_df = pd.DataFrame(data={
        "artist": artist,
        "title": title,
        "file_path": file_path,
        "album": album,
        "duration": duration,
        "year": year,
    })
    return meta_df


if __name__ == "__main__":
    # convert()
    meta_df = get_meta_df()
