import pandas as pd
import json
import os

def sync_data():
    print("Reading Excel files from 'data/' directory...")
    
    try:
        # Read Excel files and replace NaN (empty cells) with empty strings
        team_df = pd.read_excel('data/team.xlsx').fillna('')
        pubs_df = pd.read_excel('data/publications.xlsx').fillna('')
        
        # Convert DataFrames to lists of dictionaries
        team_records = team_df.to_dict(orient='records')
        pub_records = pubs_df.to_dict(orient='records')
        
        # Process team groups (convert comma-separated string to a list)
        for member in team_records:
            if isinstance(member.get('groups'), str):
                member['groups'] = [g.strip() for g in member['groups'].split(',') if g.strip()]
            else:
                member['groups'] = []
                
        # Prepare the final JSON structure
        full_data = {
            "team": team_records,
            "publications": pub_records
        }
        
        # Ensure the src directory exists
        os.makedirs('src', exist_ok=True)
        
        # Save to JSON
        with open('src/data.json', 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully synced {len(team_records)} team members and {len(pub_records)} publications to src/data.json")
        
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure 'team.xlsx' and 'publications.xlsx' exist in the 'data' folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sync_data()
