import pandas as pd

def load_datasets():
    try:
        dataset1 = pd.read_excel("/workspaces/bounce/Dataset 1 (Sustainability Research Results).xlsx")
        dataset2 = pd.read_excel("/workspaces/bounce/Dataset 2 (Christmas Research Results).xlsx")
        return dataset1, dataset2
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return None, None
