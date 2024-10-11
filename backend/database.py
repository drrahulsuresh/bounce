from sqlalchemy.orm import sessionmaker
from app.models import SurveyData, engine
from app.data_processing import load_and_save_datasets

# Create a session for database operations
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    # Load cleaned datasets
    sustainability_cleaned, christmas_cleaned = load_and_save_datasets()

    # Insert sustainability data into the database
    for _, row in sustainability_cleaned.iterrows():
        new_data = SurveyData(
            question="Sustainability",  # Assuming this is a placeholder column
            demographic=row.get('Demographics', None),  # Adjust column name
            response_type="Survey Response",  # This can be customized
            response_value=row.get('Male', None)  # Sample response; adjust based on dataset
        )
        session.add(new_data)

    # Insert Christmas data into the database
    for _, row in christmas_cleaned.iterrows():
        new_data = SurveyData(
            question="Christmas",  # Assuming this is a placeholder column
            demographic=row.get('Demographics', None),  # Adjust column name
            response_type="Survey Response",  # This can be customized
            response_value=row.get('Female', None)  # Sample response; adjust based on dataset
        )
        session.add(new_data)

    # Commit the session to save data
    session.commit()
    print("Survey data has been loaded into the database.")

if __name__ == '__main__':
    init_db()
