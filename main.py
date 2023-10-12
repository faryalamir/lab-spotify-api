from functions import songs_ids, search_song, add_audio_features, get_audio_features
import pandas as pd

billboard_top_100 = pd.read_csv('./hot100.csv')
print(billboard_top_100.head())

billboard_top_100 = songs_ids(billboard_top_100)
print(billboard_top_100.head())

print(billboard_top_100.isnull().sum())

audio_features_df = get_audio_features(list(billboard_top_100['ids']))
audio_features_df = audio_features_df.reset_index(drop=True)
audio_features_df.head()

billboard_top_100_features = add_audio_features(billboard_top_100,audio_features_df)
print(billboard_top_100_features.head())
print(billboard_top_100_features.columns)

print(billboard_top_100_features.isnull().sum())

billboard_top_100_features.to_csv('top_100_extended.csv', index=False)
