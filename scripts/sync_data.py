import pandas as pd
import json
import os

def sync_data():
    # Ensure paths are correct regardless of where the script is called from
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    output_path = os.path.join(base_dir, 'src', 'data.json')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Syncing data from {data_dir}...")
    
    try:
        team_df = pd.read_excel(os.path.join(data_dir, 'team.xlsx')).fillna('')
        pubs_df = pd.read_excel(os.path.join(data_dir, 'publications.xlsx')).fillna('')
        
        team_records = team_df.to_dict(orient='records')
        pub_records = pubs_df.to_dict(orient='records')
        
        for member in team_records:
            if isinstance(member.get('groups'), str):
                member['groups'] = [g.strip() for g in member['groups'].split(',') if g.strip()]
            else:
                member['groups'] = []
                
        full_data = {
            "team": team_records,
            "publications": pub_records
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully synced data to {output_path}")
        
    except Exception as e:
        print(f"Fatal error during sync: {e}")
        exit(1)

if __name__ == "__main__":
    sync_data()
