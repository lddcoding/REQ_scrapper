import streamlit as st
import pandas as pd
import requests

# Function to find the company website using Google Custom Search API
def find_company_website(company_name, api_key):
    """
    Finds the website of a company using the Google Custom Search JSON API.

    Args:
        company_name (str): The name of the company (e.g., "Club Piscine").
        api_key (str): Your Google API key.

    Returns:
        str: The website URL of the company, if found; otherwise, None.
    """ 
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": company_name,
        "key": api_key,
        "cx": "845c0833a412b4955",  # Your Custom Search Engine ID
        "num": 1  # Number of results to return (1 for the first result)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]
        else:
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"Error while searching for company website: {e}")
        return None

# Streamlit App
def main():
    st.title("Company Website Finder")

    # Upload file section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Process the DataFrame
        if 'NOM_ASSUJ' in df.columns and 'DAT_FIN_NOM_ASSUJ' in df.columns:
            # Remove rows where NOM_ASSUJ contains "QUÉBEC INC"
            df = df[~df['NOM_ASSUJ'].str.contains("QUÉBEC INC", case=False, na=False)]

            # Use regex to remove rows where 'DAT_FIN_NOM_ASSUJ' contains a date in the format YYYY-MM-DD
            df = df[~df['DAT_FIN_NOM_ASSUJ'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)]

            # Add a button to start filtering and adding websites
            if st.button('Filter and Add Websites'):
                # API key for Google Custom Search API (your existing key)
                api_key = "AIzaSyARVaR1T5s8mTf7I6YBsgkKwm7HZdI7-1k"
                
                # Apply the function to each company in the NOM_ASSUJ column and create a new 'Website' column
                df['Website'] = df['NOM_ASSUJ'].apply(lambda x: find_company_website(x, api_key))

                # Display the updated DataFrame
                st.write("Filtered DataFrame with Website Links:")
                st.dataframe(df[['NOM_ASSUJ', 'Website']])

        else:
            st.error("The uploaded CSV does not contain the required columns: 'NOM_ASSUJ' and 'DAT_FIN_NOM_ASSUJ'")

if __name__ == "__main__":
    main()
