import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

# Function to sort data by score
def sort_by_score(dataframe, ascending=False):
    return dataframe.sort_values(by='Score', ascending=ascending)

# Function to sort data by total orders
def sort_by_total_orders(dataframe, ascending=False):
    dataframe['Total Orders so far'] = pd.to_numeric(dataframe['Total Orders so far'], errors='coerce')
    return dataframe.sort_values(by='Total Orders so far', ascending=ascending)

# Function to sort data by on-time delivery rate
def sort_by_delivery_rate(dataframe, ascending=False):
    dataframe['On time Delivery Rate'] = dataframe['On time Delivery Rate'].str.rstrip('%')
    dataframe['On time Delivery Rate'] = pd.to_numeric(dataframe['On time Delivery Rate'], errors='coerce')
    return dataframe.sort_values(by='On time Delivery Rate', ascending=ascending)

# Function to filter data by location
def filter_by_location(dataframe, location):
    return dataframe[dataframe['Location'].fillna('').str.contains(location, case=False)]

# Function to filter data by minimum score
def filter_by_min_score(dataframe, min_score):
    return dataframe[dataframe['Score'] >= min_score]

# Function to get manufacturers with reviews greater than a specified number
def filter_by_reviews(dataframe, min_reviews):
    dataframe['Reviews'] = dataframe['Reviews'].str.replace(' reviews', '').replace(' review', '').fillna(0).astype('int')
    return dataframe[dataframe['Reviews'] > min_reviews]

# Function to plot bar graph of scores
def plot_scores(dataframe, top_n=20):
    plt.figure(figsize=(10, 6))
    top_scores = dataframe.nlargest(top_n, 'Score')
    sns.barplot(x='Score', y='Name', data=top_scores.sort_values(by='Score', ascending=False))
    plt.title('Top Manufacturer Scores')
    plt.xlabel('Score')
    plt.ylabel('Manufacturer')
    plt.tight_layout()
    plt.show()

# Function to plot pie chart of locations
def plot_locations(dataframe, threshold=0.02):
    location_counts = dataframe['Location'].value_counts(normalize=True)
    other_locations = location_counts[location_counts < threshold].sum()
    main_locations = location_counts[location_counts >= threshold]
    main_locations['Others'] = other_locations
    plt.figure(figsize=(10, 6))
    plt.pie(main_locations, labels=main_locations.index, autopct='%1.1f%%')
    plt.title('Manufacturer Locations')
    plt.tight_layout()
    plt.show()

# Function to plot scatter plot of scores vs. reviews
def plot_scores_vs_reviews(dataframe):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Reviews', y='Score', data=dataframe, alpha=0.6)
    plt.title('Scores vs. Reviews')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process and visualize manufacturer data.')
    parser.add_argument('manufacturers_data_06_12', type=str, help='Path to the CSV file containing the data')
    args = parser.parse_args()

    # Verify the file path
    if not os.path.isfile(args.file_path):
        print(f"Error: The file {args.file_path} does not exist.")
        exit(1)

    # Load the data
    print("loading the data...")
    df = pd.read_csv(args.file_path)

    # Sort by score
    sorted_by_score = sort_by_score(df)
    print("Top manufacturers by score:")
    print(sorted_by_score.head())

    # Sort by total orders
    sorted_by_orders = sort_by_total_orders(df)
    print("\nTop manufacturers by total orders:")
    print(sorted_by_orders.head())

    # Sort by on-time delivery rate
    sorted_by_delivery_rate = sort_by_delivery_rate(df)
    print("\nTop manufacturers by on-time delivery rate:")
    print(sorted_by_delivery_rate.head())

    # Filter by location
    filtered_by_location = filter_by_location(df, 'Guangdong')
    print("\nManufacturers in Guangdong:")
    print(filtered_by_location)

    # Filter by minimum score
    filtered_by_score = filter_by_min_score(df, 4.8)
    print("\nManufacturers with a score of at least 4.8:")
    print(filtered_by_score)

    # Filter by minimum reviews
    filtered_by_reviews = filter_by_reviews(df, 10)
    print("\nManufacturers with more than 10 reviews:")
    print(filtered_by_reviews)

    # Plot graphs
    plot_scores(df)
    plot_locations(df)
    plot_scores_vs_reviews(df)