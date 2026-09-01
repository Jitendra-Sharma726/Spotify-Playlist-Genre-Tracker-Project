import pandas as pd


# 1. Load Playlist Data
def load_playlist(filename):
    """
    Load CSV playlist data into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return pd.DataFrame()


# 2. Remove Duplicate Tracks
def remove_duplicates(df):
    """
    Remove duplicate songs based on Title + Artist combination.
    """
    cleaned_df = df.drop_duplicates(subset=["Track", "Artist"])
    return cleaned_df


# 3. Count Genre Popularity
def count_genre_frequency(df):
    """
    Count total songs in each genre.
    """
    return df["Genre"].value_counts()


# 4. Analyze Artist Performance by Genre
def group_by_genre_and_artist(df):
    """
    Group by Genre + Artist and count tracks per artist.
    """
    grouped = df.groupby(["Genre", "Artist"])["Track"].count()
    return grouped


# 5. Multi-Aggregation Summary
def compute_genre_stats(df):
    """
    Calculate:
      - Total Songs per genre
      - Average Popularity (0-100)
    """
    stats = df.groupby("Genre").agg({
        # Count of songs
        "Track": "count",      

        # Average popularity score
        "Popularity": "mean"   
    })
    
    # Renaming columns for cleaner output
    if not stats.empty:
        # Rename columns for cleaner output
        stats.columns = ["Total_Songs", "Avg_Popularity"]
        return stats.round(2)
    return stats


# 6. Sort Results for Insights
def sort_top_artists(grouped_series):
    """
    Sort grouped Series (Genre + Artist track counts) in descending order.
    """
    return grouped_series.sort_values(ascending=False)


if __name__ == "__main__":

    filename = 'spotify_playlist.csv'
    df = load_playlist(filename)

    if not df.empty:
        # Check initial count
        print(f"\nSongs Loaded: {len(df)}")

        # Remove duplicates
        df_clean = remove_duplicates(df)
        print(f"After Cleaning Duplicates: {len(df_clean)}")

        # Genre frequency
        genre_counts = count_genre_frequency(df_clean)
        print("\nSongs Per Genre:")
        print(genre_counts)

        # Artist performance per genre
        artist_grouped = group_by_genre_and_artist(df_clean)
        print("\nArtist Track Counts (Grouped):")
        # Show top 10 to save space
        print(artist_grouped.head(10)) 

        # Genre summary statistics
        genre_stats = compute_genre_stats(df_clean)
        print("\nGenre Performance Stats:")
        print(genre_stats)

        # Most active artists overall
        sorted_artists = sort_top_artists(artist_grouped)
        print("\nTop 5 Most Active Artists:")
        print(sorted_artists.head(5))


