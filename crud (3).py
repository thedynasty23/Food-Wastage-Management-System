import pandas as pd
from datetime import datetime
import streamlit as st

class CRUDOperations:
    """CRUD operations for all entities"""
    
    @staticmethod
    def add_provider(name, provider_type, city, contact, address=""):
        """Add new provider"""
        try:
            new_id = len(data['providers']) + 1
            new_provider = pd.DataFrame({
                'provider_id': [new_id],
                'name': [name],
                'type': [provider_type],
                'city': [city],
                'contact': [contact],
                'address': [address]
            })
            new_provider.to_sql('providers', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Provider added successfully!"
        except Exception as e:
            return False, f"Error adding provider: {e}"

    @staticmethod
    def add_receiver(name, receiver_type, city, contact):
        """Add new receiver"""
        try:
            new_id = len(data['receivers']) + 1
            new_receiver = pd.DataFrame({
                'receiver_id': [new_id],
                'name': [name],
                'type': [receiver_type],
                'city': [city],
                'contact': [contact]
            })
            new_receiver.to_sql('receivers', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Receiver added successfully!"
        except Exception as e:
            return False, f"Error adding receiver: {e}"

    @staticmethod
    def add_food_listing(food_name, quantity, expiry_date, provider_id, food_type, meal_type):
        """Add new food listing"""
        try:
            new_id = len(data['food_listings']) + 1
            new_food = pd.DataFrame({
                'food_id': [new_id],
                'food_name': [food_name],
                'quantity': [quantity],
                'expiry_date': [expiry_date],
                'provider_id': [provider_id],
                'food_type': [food_type],
                'meal_type': [meal_type]
            })
            new_food.to_sql('food_listings', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Food listing added successfully!"
        except Exception as e:
            return False, f"Error adding food listing: {e}"

    @staticmethod
    def add_claim(food_id, receiver_id, status="Pending"):
        """Add new claim"""
        try:
            new_id = len(data['claims']) + 1
            new_claim = pd.DataFrame({
                'claim_id': [new_id],
                'food_id': [food_id],
                'receiver_id': [receiver_id],
                'status': [status],
                'timestamp': [datetime.now()]
            })
            new_claim.to_sql('claims', engine, if_exists='append', index=False)
            st.cache_data.clear()
            return True, "Claim added successfully!"
        except Exception as e:
            return False, f"Error adding claim: {e}"
