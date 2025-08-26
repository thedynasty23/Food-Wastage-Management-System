import pandas as pd
import streamlit as st
from datetime import datetime

class SQLQueries:
    """Complete SQL queries covering all project requirements and additional analysis"""
    
    @staticmethod
    def execute_query(query):
        """Execute SQL query and return results"""
        try:
            with engine.connect() as conn:
                result = pd.read_sql(query, conn)
                return result
        except Exception as e:
            st.error(f"Query execution error: {e}")
            return pd.DataFrame()


    @staticmethod
    def get_items_expiring_next_3_days():
        """14. Items expiring in the next 3 days with provider & city"""
        query = """
        SELECT 
            f.food_id, f.food_name, f.quantity, f.expiry_date,
            p.provider_id, p.name AS provider_name, p.city
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        WHERE DATE(f.expiry_date) BETWEEN DATE('now') AND DATE('now','+3 days')
        ORDER BY f.expiry_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_reliability_pct():
        """15. Provider reliability = % completed claims"""
        query = """
        SELECT 
            p.provider_id, p.name AS provider_name, p.city,
            COUNT(c.claim_id) AS total_claims,
            SUM(CASE WHEN LOWER(c.status)='completed' THEN 1 ELSE 0 END) AS completed_claims,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status)='completed' THEN 1 ELSE 0 END) / NULLIF(COUNT(c.claim_id),0), 2) AS reliability_pct
        FROM providers p
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.provider_id
        ORDER BY reliability_pct DESC NULLS LAST, total_claims DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_food_type_wastage_pct():
        """16. Wastage % by food_type"""
        query = """
        SELECT 
            f.food_type,
            SUM(f.quantity) AS total_quantity,
            SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) AS wasted_quantity,
            ROUND(100.0 * SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity),0), 2) AS wastage_pct
        FROM food_listings f
        GROUP BY f.food_type
        ORDER BY wastage_pct DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_highest_demand_locations_by_claims():
        """20. Highest demand locations by claims (city)"""
        query = """
        SELECT 
            p.city AS location,
            COUNT(c.claim_id) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.city
        ORDER BY total_claims DESC
        LIMIT 10
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_frequent_providers_contributions():
        """19. Most frequent providers & their contributions"""
        query = """
        SELECT 
            p.name AS provider_name,
            COUNT(f.food_id) AS total_listings,
            COALESCE(SUM(f.quantity),0) AS total_quantity
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY p.name
        ORDER BY total_listings DESC
        LIMIT 10
        """
        return SQLQueries.execute_query(query)

    # ========== REQUESTED QUERIES 1-15 ==========
    @staticmethod
    def get_providers_receivers_per_city():
        """1. How many food providers and receivers are there in each city?"""
        query = """
        SELECT 
            COALESCE(p.city, r.city) as city,
            COUNT(DISTINCT p.provider_id) as total_providers,
            COUNT(DISTINCT r.receiver_id) as total_receivers,
            -- Provider type breakdown
            COUNT(DISTINCT CASE WHEN p.type = 'Restaurant' THEN p.provider_id END) as restaurants,
            COUNT(DISTINCT CASE WHEN p.type = 'Grocery Store' THEN p.provider_id END) as grocery_stores,
            COUNT(DISTINCT CASE WHEN p.type = 'Hotel' THEN p.provider_id END) as hotels,
            COUNT(DISTINCT CASE WHEN p.type = 'Supermarket' THEN p.provider_id END) as supermarkets,
            -- Receiver type breakdown
            COUNT(DISTINCT CASE WHEN r.type = 'NGO' THEN r.receiver_id END) as ngos,
            COUNT(DISTINCT CASE WHEN r.type = 'Food Bank' THEN r.receiver_id END) as food_banks,
            COUNT(DISTINCT CASE WHEN r.type = 'Shelter' THEN r.receiver_id END) as shelters,
            COUNT(DISTINCT CASE WHEN r.type = 'Charity' THEN r.receiver_id END) as charities,
            -- Total ecosystem strength
            (COUNT(DISTINCT p.provider_id) + COUNT(DISTINCT r.receiver_id)) as total_ecosystem_strength
        FROM providers p 
        LEFT JOIN receivers r ON p.city = r.city
        GROUP BY COALESCE(p.city, r.city)
        HAVING COUNT(DISTINCT p.provider_id) > 0 OR COUNT(DISTINCT r.receiver_id) > 0
        ORDER BY total_ecosystem_strength DESC, total_providers DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_type_contributions():
        """2. Which type of food provider contributes the most food?"""
        query = """
        SELECT 
            p.type as provider_type,
            COUNT(DISTINCT p.provider_id) as total_providers,
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity_contributed,
            AVG(f.quantity) as avg_quantity_per_listing,
            -- Diversity metrics
            COUNT(DISTINCT f.food_type) as food_types_offered,
            COUNT(DISTINCT f.meal_type) as meal_types_offered,
            -- Success metrics
            COUNT(c.claim_id) as total_claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_distributed,
            -- Impact per provider
            ROUND(SUM(f.quantity) / COUNT(DISTINCT p.provider_id), 2) as avg_contribution_per_provider,
            -- Ranking
            ROW_NUMBER() OVER (ORDER BY SUM(f.quantity) DESC) as contribution_rank
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.type
        HAVING COUNT(f.food_id) > 0
        ORDER BY total_quantity_contributed DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_contacts_by_city(city_name=None):
        """3. What is the contact information of food providers in a specific city?"""
        if city_name:
            where_clause = f"WHERE LOWER(p.city) = LOWER('{city_name}')"
        else:
            where_clause = ""
        
        query = f"""
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            COALESCE(p.address, 'N/A') as address,
            -- Activity metrics
            COUNT(f.food_id) as active_food_listings,
            SUM(f.quantity) as total_quantity_available,
            COUNT(DISTINCT f.food_type) as food_types_offered,
            -- Recent activity
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_items_available,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_items,
            -- Claims received
            COUNT(c.claim_id) as claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            -- Status indicator
            CASE 
                WHEN COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) > 0 THEN '🟢 Active'
                WHEN COUNT(f.food_id) > 0 THEN '🟡 Has Listings'
                ELSE '🔴 Inactive'
            END as status
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        {where_clause}
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact, p.address
        ORDER BY active_food_listings DESC, total_quantity_available DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_top_claiming_receivers():
        """4. Which receivers have claimed the most food?"""
        query = """
        SELECT 
            r.receiver_id,
            r.name as receiver_name,
            r.type as receiver_type,
            r.city,
            r.contact,
            -- Claiming activity
            COUNT(c.claim_id) as total_claims_made,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Food quantity metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_received,
            AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END) as avg_food_per_successful_claim,
            -- Food diversity
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.food_type END) as food_types_received,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.meal_type END) as meal_types_received,
            -- Recent activity (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            -- Performance rating
            CASE 
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 20 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 80 
                THEN '⭐⭐⭐ Excellent Receiver'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 10 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 60 
                THEN '⭐⭐ Good Receiver'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 1 
                THEN '⭐ Active Receiver'
                ELSE '❌ Inactive'
            END as receiver_rating
        FROM receivers r 
        LEFT JOIN claims c ON r.receiver_id = c.receiver_id
        LEFT JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY r.receiver_id, r.name, r.type, r.city, r.contact
        HAVING COUNT(c.claim_id) > 0
        ORDER BY total_food_received DESC, total_claims_made DESC
        LIMIT 25
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_total_food_quantity_available():
        """5. What is the total quantity of food available from all providers?"""
        query = """
        SELECT 
            'System-Wide Food Availability' as metric_category,
            -- Overall availability
            COUNT(f.food_id) as total_food_items,
            SUM(f.quantity) as total_quantity_available,
            AVG(f.quantity) as avg_quantity_per_item,
            -- By freshness
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_items,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN f.quantity ELSE 0 END) as fresh_quantity,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_items,
            SUM(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN f.quantity ELSE 0 END) as expired_quantity,
            -- By urgency
            COUNT(CASE WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN 1 END) as urgent_items,
            SUM(CASE WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN f.quantity ELSE 0 END) as urgent_quantity,
            COUNT(CASE WHEN julianday(f.expiry_date) - julianday('now') BETWEEN 1 AND 7 THEN 1 END) as soon_expiring_items,
            SUM(CASE WHEN julianday(f.expiry_date) - julianday('now') BETWEEN 1 AND 7 THEN f.quantity ELSE 0 END) as soon_expiring_quantity,
            -- Distribution metrics
            COUNT(DISTINCT p.provider_id) as contributing_providers,
            COUNT(DISTINCT p.city) as cities_covered,
            COUNT(DISTINCT f.food_type) as food_types_available,
            COUNT(DISTINCT f.meal_type) as meal_types_available,
            -- Claims impact
            COUNT(c.claim_id) as total_claims,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as distribution_rate,
            -- Efficiency metrics
            ROUND(SUM(f.quantity) / NULLIF(COUNT(DISTINCT p.provider_id), 0), 2) as avg_quantity_per_provider,
            ROUND(SUM(f.quantity) / NULLIF(COUNT(DISTINCT p.city), 0), 2) as avg_quantity_per_city
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_cities_by_food_listings():
        """6. Which city has the highest number of food listings?"""
        query = """
        SELECT 
            p.city,
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity,
            AVG(f.quantity) as avg_quantity_per_listing,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as unique_providers,
            COUNT(DISTINCT p.type) as provider_types,
            -- Food diversity
            COUNT(DISTINCT f.food_type) as food_types_available,
            COUNT(DISTINCT f.meal_type) as meal_types_available,
            -- Freshness analysis
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as fresh_listings,
            COUNT(CASE WHEN DATE(f.expiry_date) < DATE('now') THEN 1 END) as expired_listings,
            ROUND(100.0 * COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) / COUNT(f.food_id), 2) as freshness_rate,
            -- Claims activity
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- City ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(f.food_id) DESC) as listings_rank,
            ROW_NUMBER() OVER (ORDER BY SUM(f.quantity) DESC) as quantity_rank,
            -- City performance score (composite)
            ROUND(
                (COUNT(f.food_id) * 0.4) + 
                (SUM(f.quantity) * 0.3 / 100) + 
                (COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) * 0.3)
                , 2) as city_performance_score
        FROM providers p 
        JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.city
        ORDER BY total_food_listings DESC, total_quantity DESC
        LIMIT 20
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_common_food_types():
        """7. What are the most commonly available food types?"""
        query = """
        SELECT 
            f.food_type,
            COUNT(f.food_id) as total_items,
            SUM(f.quantity) as total_quantity,
            AVG(f.quantity) as avg_quantity_per_item,
            -- Availability metrics
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN 1 END) as available_items,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now') THEN f.quantity ELSE 0 END) as available_quantity,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as unique_providers,
            COUNT(DISTINCT p.type) as provider_types,
            COUNT(DISTINCT p.city) as cities_available,
            -- Meal type breakdown
            COUNT(DISTINCT f.meal_type) as meal_types,
            -- Demand analysis
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- Supply vs demand ratio
            ROUND(CAST(COUNT(f.food_id) AS FLOAT) / NULLIF(COUNT(c.claim_id), 0), 2) as supply_demand_ratio,
            -- Popularity ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(f.food_id) DESC) as popularity_rank,
            ROW_NUMBER() OVER (ORDER BY COUNT(c.claim_id) DESC) as demand_rank,
            -- Market share
            ROUND(100.0 * COUNT(f.food_id) / (SELECT COUNT(*) FROM food_listings), 2) as market_share_percentage
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_type
        ORDER BY total_items DESC, total_quantity DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_claims_per_food_item():
        """8. How many food claims have been made for each food item?"""
        query = """
        SELECT 
            f.food_id,
            f.food_name,
            f.food_type,
            f.meal_type,
            f.quantity,
            f.expiry_date,
            p.name as provider_name,
            p.type as provider_type,
            p.city as provider_city,
            -- Claims analysis
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            -- Success metrics
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Timing analysis
            ROUND(AVG(julianday(f.expiry_date) - julianday(c.timestamp)), 1) as avg_days_before_expiry_when_claimed,
            -- Competition analysis
            ROUND(CAST(COUNT(c.claim_id) AS FLOAT) / f.quantity, 2) as claims_per_unit,
            -- Status
            CASE 
                WHEN DATE(f.expiry_date) < DATE('now') THEN '🔴 Expired'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) > 0 THEN '🟢 Distributed'
                WHEN COUNT(c.claim_id) > 0 THEN '🟡 Has Claims'
                WHEN julianday(f.expiry_date) - julianday('now') <= 1 THEN '🟠 Urgent'
                ELSE '⚪ Available'
            END as item_status
        FROM food_listings f 
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_id, f.food_name, f.food_type, f.meal_type, f.quantity, f.expiry_date, p.name, p.type, p.city
        ORDER BY total_claims DESC, f.food_id
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_provider_highest_successful_claims():
        """9. Which provider has had the highest number of successful food claims?"""
        query = """
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            -- Food provision metrics
            COUNT(f.food_id) as total_food_listings,
            SUM(f.quantity) as total_quantity_provided,
            COUNT(DISTINCT f.food_type) as food_types_diversity,
            -- Claims success metrics
            COUNT(c.claim_id) as total_claims_received,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Impact metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_distributed,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN c.receiver_id END) as unique_receivers_served,
            -- Efficiency metrics
            ROUND(COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(f.food_id), 0), 2) as claims_per_listing,
            ROUND(SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(COUNT(f.food_id), 0), 2) as avg_distributed_per_listing,
            -- Time efficiency
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_distributed,
            -- Recent performance (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') AND LOWER(c.status) = 'completed' THEN 1 END) as recent_successful_claims,
            -- Awards/Recognition
            CASE 
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 50 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 85 
                THEN '🏆 Champion Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 25 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 75 
                THEN '⭐⭐⭐ Excellent Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 10 
                     AND (100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0)) >= 60 
                THEN '⭐⭐ Good Provider'
                WHEN COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) >= 1 
                THEN '⭐ Active Provider'
                ELSE '❌ Inactive'
            END as provider_recognition
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact
        HAVING COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) > 0
        ORDER BY successful_claims DESC, total_food_distributed DESC
        LIMIT 25
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_claims_completion_percentages():
        """10. What percentage of food claims are completed vs. pending vs. canceled?"""
        query = """
        SELECT 
            c.status,
            COUNT(*) as claim_count,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) as percentage,
            -- Quantity analysis
            SUM(f.quantity) as total_quantity_involved,
            AVG(f.quantity) as avg_quantity_per_claim,
            -- Geographic distribution
            COUNT(DISTINCT p.city) as cities_involved,
            COUNT(DISTINCT p.provider_id) as providers_involved,
            COUNT(DISTINCT r.receiver_id) as receivers_involved,
            -- Food type diversity
            COUNT(DISTINCT f.food_type) as food_types_in_status,
            COUNT(DISTINCT f.meal_type) as meal_types_in_status,
            -- Time analysis
            ROUND(AVG(julianday('now') - julianday(c.timestamp)), 1) as avg_days_since_claim,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_when_completed,
            -- Recent trends (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            ROUND(100.0 * COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) / 
                  NULLIF((SELECT COUNT(*) FROM claims WHERE DATE(timestamp) >= DATE('now', '-30 days')), 0), 2) as recent_percentage,
            -- Impact calculation
            CASE c.status 
                WHEN 'Completed' THEN SUM(f.quantity) 
                ELSE 0 
            END as food_impact_kg,
            -- Status insights
            CASE c.status 
                WHEN 'Completed' THEN '✅ Successfully distributed food to those in need'
                WHEN 'Pending' THEN '⏳ Awaiting pickup or processing'
                WHEN 'Cancelled' THEN '❌ Claims that did not proceed - investigate reasons'
                ELSE '❓ Unknown status'
            END as status_insight
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY c.status
        ORDER BY claim_count DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_avg_quantity_per_receiver():
        """11. What is the average quantity of food claimed per receiver?"""
        query = """
        SELECT 
            r.receiver_id,
            r.name as receiver_name,
            r.type as receiver_type,
            r.city,
            -- Claiming metrics
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_food_received,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END), 2) as avg_quantity_per_successful_claim,
            ROUND(SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(COUNT(c.claim_id), 0), 2) as avg_quantity_per_total_claim,
            -- Efficiency metrics
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as claim_success_rate,
            -- Food diversity received
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.food_type END) as food_types_received,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN f.meal_type END) as meal_types_received,
            -- Provider diversity
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN p.provider_id END) as providers_claimed_from,
            -- Time analysis
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_received,
            -- Recent activity
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            SUM(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') AND LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as recent_food_received,
            -- Receiver category based on activity
            CASE 
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 500 THEN '🏆 Major Recipient'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 200 THEN '⭐⭐⭐ High Volume'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 50 THEN '⭐⭐ Regular'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1 THEN '⭐ Occasional'
                ELSE '❌ No Success'
            END as receiver_category
        FROM receivers r 
        LEFT JOIN claims c ON r.receiver_id = c.receiver_id
        LEFT JOIN food_listings f ON c.food_id = f.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY r.receiver_id, r.name, r.type, r.city
        HAVING COUNT(c.claim_id) > 0
        ORDER BY total_food_received DESC, avg_quantity_per_successful_claim DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_most_claimed_meal_types():
        """12. Which meal type is claimed the most?"""
        query = """
        SELECT 
            f.meal_type,
            -- Claiming metrics
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / NULLIF(COUNT(c.claim_id), 0), 2) as success_rate,
            -- Quantity metrics
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as total_quantity_distributed,
            AVG(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity END) as avg_quantity_per_successful_claim,
            -- Supply vs demand analysis
            COUNT(DISTINCT f.food_id) as total_items_available,
            ROUND(CAST(COUNT(c.claim_id) AS FLOAT) / NULLIF(COUNT(DISTINCT f.food_id), 0), 2) as demand_supply_ratio,
            -- Provider and receiver diversity
            COUNT(DISTINCT p.provider_id) as providers_offering,
            COUNT(DISTINCT r.receiver_id) as receivers_claiming,
            COUNT(DISTINCT p.city) as cities_with_supply,
            -- Food type diversity within meal type
            COUNT(DISTINCT f.food_type) as food_types_in_meal,
            -- Time analysis
            ROUND(AVG(julianday(f.expiry_date) - julianday('now')), 1) as avg_shelf_life_days,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_claimed,
            -- Market share
            ROUND(100.0 * COUNT(c.claim_id) / (SELECT COUNT(*) FROM claims), 2) as claim_market_share,
            -- Popularity ranking
            ROW_NUMBER() OVER (ORDER BY COUNT(c.claim_id) DESC) as demand_rank,
            ROW_NUMBER() OVER (ORDER BY COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) DESC) as success_rank,
            -- Recent trends (last 30 days)
            COUNT(CASE WHEN DATE(c.timestamp) >= DATE('now', '-30 days') THEN 1 END) as recent_claims,
            -- Meal time insights
            CASE f.meal_type 
                WHEN 'Breakfast' THEN '🌅 Morning meals - typically fresh items needed'
                WHEN 'Lunch' THEN '🌞 Midday meals - highest volume period'
                WHEN 'Dinner' THEN '🌙 Evening meals - often hearty dishes'
                WHEN 'Snacks' THEN '🍪 Light items - good for quick distribution'
                WHEN 'Beverages' THEN '🥤 Drinks - long shelf life items'
                ELSE '🍽️ Mixed meal items'
            END as meal_type_insight
        FROM food_listings f 
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC, successful_claims DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_total_donations_per_provider():
        """13. What is the total quantity of food donated by each provider?"""
        query = """
        SELECT 
            p.provider_id,
            p.name as provider_name,
            p.type as provider_type,
            p.city,
            p.contact,
            -- Donation metrics
            COUNT(f.food_id) as total_food_items_listed,
            SUM(f.quantity) as total_quantity_donated,
            AVG(f.quantity) as avg_quantity_per_donation,
            -- Distribution success
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_successfully_distributed,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_successfully_distributed,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as distribution_success_rate,
            -- Wastage analysis
            COUNT(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN 1 END) as expired_items,
            SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) as wasted_quantity,
            ROUND(100.0 * SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0), 2) as wastage_rate,
            -- Food diversity
            COUNT(DISTINCT f.food_type) as food_types_donated,
            COUNT(DISTINCT f.meal_type) as meal_types_donated,
            -- Impact metrics
            COUNT(DISTINCT r.receiver_id) as unique_receivers_served,
            COUNT(DISTINCT CASE WHEN LOWER(c.status) = 'completed' THEN r.receiver_id END) as receivers_successfully_served,
            -- Time efficiency
            ROUND(AVG(julianday(f.expiry_date) - julianday('now')), 1) as avg_donation_shelf_life,
            ROUND(AVG(CASE WHEN LOWER(c.status) = 'completed' THEN julianday(f.expiry_date) - julianday(c.timestamp) END), 1) as avg_days_before_expiry_distributed,
            -- Recent activity (last 30 days)
            COUNT(CASE WHEN DATE(f.expiry_date) >= DATE('now', '-30 days') THEN 1 END) as recent_donations,
            SUM(CASE WHEN DATE(f.expiry_date) >= DATE('now', '-30 days') THEN f.quantity ELSE 0 END) as recent_donation_quantity,
            -- Provider impact score
            ROUND(
                (SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) * 0.6) +
                (COUNT(DISTINCT r.receiver_id) * 10 * 0.2) +
                (COUNT(DISTINCT f.food_type) * 5 * 0.2)
                , 2) as provider_impact_score,
            -- Recognition level
            CASE 
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1000 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 80 
                THEN '🏆 Champion Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 500 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 70 
                THEN '⭐⭐⭐ Excellent Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 200 
                     AND (100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) / NULLIF(SUM(f.quantity), 0)) >= 60 
                THEN '⭐⭐ Good Donor'
                WHEN SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) >= 1 
                THEN '⭐ Active Donor'
                ELSE '❌ Inactive'
            END as donor_recognition
        FROM providers p 
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        GROUP BY p.provider_id, p.name, p.type, p.city, p.contact
        HAVING COUNT(f.food_id) > 0
        ORDER BY total_quantity_donated DESC, quantity_successfully_distributed DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_food_wastage_trends_comprehensive():
        """14. Enhanced food wastage trends with all insights"""
        query = """
        SELECT 
            food_type,
            COUNT(*) as total_listings,
            SUM(quantity) as total_quantity,
            AVG(quantity) as avg_quantity_per_listing,
            -- Wastage calculations
            COUNT(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN 1 END) as expired_items,
            SUM(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN quantity ELSE 0 END) as wasted_quantity,
            ROUND(100.0 * COUNT(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN 1 END) / COUNT(*), 2) as wastage_percentage,
            ROUND(100.0 * SUM(CASE WHEN julianday('now') - julianday(expiry_date) > 0 THEN quantity ELSE 0 END) / SUM(quantity), 2) as quantity_wastage_percentage,
            -- Urgency analysis
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 0 AND 1 THEN 1 END) as critical_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 1 AND 3 THEN 1 END) as urgent_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') BETWEEN 3 AND 7 THEN 1 END) as soon_items,
            COUNT(CASE WHEN julianday(expiry_date) - julianday('now') > 7 THEN 1 END) as safe_items,
            -- Claims impact
            COUNT(c.claim_id) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN quantity ELSE 0 END) as quantity_saved_through_claims,
            ROUND(100.0 * SUM(CASE WHEN LOWER(c.status) = 'completed' THEN quantity ELSE 0 END) / SUM(quantity), 2) as saved_percentage,
            -- Provider diversity
            COUNT(DISTINCT p.provider_id) as contributing_providers,
            COUNT(DISTINCT p.city) as cities_offering
        FROM food_listings f 
        LEFT JOIN claims c ON f.food_id = c.food_id
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY food_type
        ORDER BY wasted_quantity DESC, total_quantity DESC
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_comprehensive_system_analysis():
        """15. Comprehensive analysis with all outputs and insights"""
        query = """
        WITH provider_stats AS (
            SELECT 
                p.type as provider_type,
                COUNT(DISTINCT p.provider_id) as provider_count,
                SUM(f.quantity) as total_contribution,
                COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as successful_distributions
            FROM providers p 
            LEFT JOIN food_listings f ON p.provider_id = f.provider_id
            LEFT JOIN claims c ON f.food_id = c.food_id
            GROUP BY p.type
        ),
        city_stats AS (
            SELECT 
                p.city,
                COUNT(DISTINCT p.provider_id) as providers,
                COUNT(DISTINCT r.receiver_id) as receivers,
                COUNT(c.claim_id) as total_claims,
                SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as food_distributed
            FROM providers p 
            LEFT JOIN receivers r ON p.city = r.city
            LEFT JOIN food_listings f ON p.provider_id = f.provider_id
            LEFT JOIN claims c ON f.food_id = c.food_id
            GROUP BY p.city
        ),
        food_stats AS (
            SELECT 
                f.food_type,
                COUNT(f.food_id) as total_items,
                SUM(f.quantity) as total_quantity,
                COUNT(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN 1 END) as wasted_items,
                SUM(CASE WHEN julianday('now') - julianday(f.expiry_date) > 0 THEN f.quantity ELSE 0 END) as wasted_quantity
            FROM food_listings f 
            GROUP BY f.food_type
        )
        SELECT 
            'COMPREHENSIVE SYSTEM ANALYSIS' as analysis_category,
            -- Overall metrics
            (SELECT COUNT(*) FROM providers) as total_providers,
            (SELECT COUNT(*) FROM receivers) as total_receivers,
            (SELECT COUNT(*) FROM food_listings) as total_food_items,
            (SELECT SUM(quantity) FROM food_listings) as total_food_quantity,
            (SELECT COUNT(*) FROM claims) as total_claims,
            -- Performance metrics
            (SELECT COUNT(*) FROM claims WHERE LOWER(status) = 'completed') as successful_distributions,
            (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') as success_rate,
            -- Top provider type
            (SELECT provider_type FROM provider_stats ORDER BY total_contribution DESC LIMIT 1) as top_provider_type_by_contribution,
            (SELECT total_contribution FROM provider_stats ORDER BY total_contribution DESC LIMIT 1) as top_provider_contribution,
            -- Top city
            (SELECT city FROM city_stats ORDER BY food_distributed DESC LIMIT 1) as top_city_by_distribution,
            (SELECT food_distributed FROM city_stats ORDER BY food_distributed DESC LIMIT 1) as top_city_distribution,
            -- Most wasted food type
            (SELECT food_type FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) as most_wasted_food_type,
            (SELECT wasted_quantity FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) as highest_waste_quantity,
            -- System health indicators
            (SELECT ROUND(100.0 * SUM(wasted_quantity) / SUM(total_quantity), 2) FROM food_stats) as overall_wastage_rate,
            (SELECT COUNT(*) FROM city_stats WHERE providers > 0 AND receivers > 0) as cities_with_complete_ecosystem,
            -- Key insights
            CASE 
                WHEN (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') >= 80 
                THEN 'System performing excellently'
                WHEN (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) FROM claims WHERE LOWER(status) = 'completed') >= 60 
                THEN 'System performing well with room for improvement'
                ELSE 'System needs significant optimization'
            END as overall_system_health,
            -- Action recommendations
            'Focus on ' || (SELECT food_type FROM food_stats ORDER BY wasted_quantity DESC LIMIT 1) || ' wastage reduction' as primary_action_needed,
            'Expand operations in ' || (SELECT city FROM city_stats ORDER BY (providers + receivers) ASC LIMIT 1) || ' for better coverage' as expansion_recommendation
        """
        return SQLQueries.execute_query(query)

    # ========== NEW: TIME SERIES ANALYSIS QUERIES ==========
    @staticmethod
    def get_time_series_claims_trends():
        """NEW: Time series analysis of claims trends"""
        query = """
        SELECT 
            DATE(c.timestamp) as claim_date,
            COUNT(*) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'pending' THEN 1 END) as pending_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'cancelled' THEN 1 END) as cancelled_claims,
            SUM(f.quantity) as total_quantity_claimed,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as daily_success_rate,
            -- Day of week analysis
            CASE strftime('%w', c.timestamp)
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END as day_of_week,
            -- Month analysis
            strftime('%Y-%m', c.timestamp) as year_month
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.timestamp IS NOT NULL
        GROUP BY DATE(c.timestamp)
        ORDER BY claim_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_time_series_food_listings_trends():
        """NEW: Time series analysis of food listings by expiry trends"""
        query = """
        SELECT 
            DATE(f.expiry_date) as expiry_date,
            COUNT(*) as items_expiring,
            SUM(f.quantity) as quantity_expiring,
            COUNT(DISTINCT f.food_type) as food_types_expiring,
            COUNT(DISTINCT p.provider_id) as providers_affected,
            -- Claims before expiry
            COUNT(c.claim_id) as claims_made,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_saved,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_saved,
            -- Wastage calculation
            COUNT(*) - COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as items_wasted,
            SUM(f.quantity) - SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_wasted,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as save_rate,
            -- Week analysis
            strftime('%Y-W%W', f.expiry_date) as year_week,
            strftime('%Y-%m', f.expiry_date) as year_month
        FROM food_listings f 
        LEFT JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN claims c ON f.food_id = c.food_id
        WHERE f.expiry_date IS NOT NULL
        GROUP BY DATE(f.expiry_date)
        ORDER BY expiry_date
        """
        return SQLQueries.execute_query(query)

    @staticmethod
    def get_monthly_performance_trends():
        """NEW: Monthly performance trends analysis"""
        query = """
        SELECT 
            strftime('%Y-%m', c.timestamp) as month,
            COUNT(*) as total_claims,
            COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) as completed_claims,
            SUM(f.quantity) as total_quantity_involved,
            SUM(CASE WHEN LOWER(c.status) = 'completed' THEN f.quantity ELSE 0 END) as quantity_distributed,
            COUNT(DISTINCT p.provider_id) as active_providers,
            COUNT(DISTINCT r.receiver_id) as active_receivers,
            COUNT(DISTINCT p.city) as cities_involved,
            ROUND(100.0 * COUNT(CASE WHEN LOWER(c.status) = 'completed' THEN 1 END) / COUNT(*), 2) as monthly_success_rate,
            ROUND(AVG(julianday(f.expiry_date) - julianday(c.timestamp)), 1) as avg_days_before_expiry,
            -- Growth metrics
            LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp)) as prev_month_claims,
            ROUND(100.0 * (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp))) / 
                  NULLIF(LAG(COUNT(*)) OVER (ORDER BY strftime('%Y-%m', c.timestamp)), 0), 2) as claims_growth_rate
        FROM claims c 
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        LEFT JOIN receivers r ON c.receiver_id = r.receiver_id
        WHERE c.timestamp IS NOT NULL
        GROUP BY strftime('%Y-%m', c.timestamp)
        ORDER BY month
        """
        return SQLQueries.execute_query(query)

# ========== ENHANCED CHART STYLING FUNCTION ==========
def apply_readable_chart_style(fig, title, x_label=None, y_label=None):
    """Apply consistent readable styling to all charts"""
    fig.update_layout(
        # Title styling
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {
                'size': 20,
                'color': '#1f2937',
                'family': 'Arial, sans-serif'
            }
        },
        
        # Plot area styling
        plot_bgcolor='white',
        paper_bgcolor='white',
        
        # Font styling
        font={
            'size': 12,
            'color': '#374151',
            'family': 'Arial, sans-serif'
        },
        
        # Margins
        margin=dict(l=80, r=80, t=100, b=80),
        
        # Grid
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            title=dict(
                text=x_label if x_label else "",
                font=dict(size=14, color='#1f2937')
            ),
            tickfont=dict(size=11, color='#374151')
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e5e7eb',
            title=dict(
                text=y_label if y_label else "",
                font=dict(size=14, color='#1f2937')
            ),
            tickfont=dict(size=11, color='#374151')
        ),
        
        # Legend styling
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#d1d5db',
            borderwidth=1,
            font=dict(size=11, color='#374151')
        ),
        
        # Hover styling
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor='#d1d5db'
        )
    )
    
    # Update traces for better visibility
    fig.update_traces(
        textfont=dict(size=11, color='#1f2937'),
        hoverlabel=dict(
            bgcolor="white",
            font=dict(color='#1f2937')
        )
    )
    
    return fig

# ========== ENHANCED VISUALIZATION FUNCTIONS ==========
def create_project_required_charts():
    """Create all charts required by the project with enhanced readability"""
    charts = {}
    try:
        # 1. Food Wastage Trends by Category - ENHANCED
        category_data = SQLQueries.get_food_wastage_trends_comprehensive()
        if not category_data.empty:
            fig = px.bar(category_data.head(10), 
                        x='food_type', 
                        y='total_quantity',
                        color='wasted_quantity',
                        hover_data=['total_listings', 'wastage_percentage', 'critical_items', 'wasted_quantity'],
                        color_continuous_scale='Reds',
                        labels={
                            'food_type': 'Food Type',
                            'total_quantity': 'Total Quantity (kg)',
                            'wasted_quantity': 'Wasted Quantity (kg)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 Food Wastage Analysis by Category", 
                                           "Food Type", 
                                           "Total Quantity (kg)")
            charts['category_trends'] = fig

        # 2. Provider Type Contributions - ENHANCED
        provider_type_data = SQLQueries.get_provider_type_contributions()
        if not provider_type_data.empty:
            fig = px.bar(provider_type_data, 
                        x='provider_type', 
                        y='total_quantity_contributed',
                        color='success_rate',
                        hover_data=['total_providers', 'food_types_offered', 'successful_distributions', 'success_rate'],
                        color_continuous_scale='Blues',
                        labels={
                            'provider_type': 'Provider Type',
                            'total_quantity_contributed': 'Total Contribution (kg)',
                            'success_rate': 'Success Rate (%)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "🏢 Food Contributions by Provider Type", 
                                           "Provider Type", 
                                           "Total Contribution (kg)")
            charts['provider_type_contributions'] = fig

        # 3. Cities by Food Listings - ENHANCED
        city_data = SQLQueries.get_cities_by_food_listings()
        if not city_data.empty:
            fig = px.bar(city_data.head(10), 
                        x='city', 
                        y='total_food_listings',
                        color='city_performance_score',
                        hover_data=['total_quantity', 'unique_providers', 'claim_success_rate', 'freshness_rate'],
                        color_continuous_scale='Viridis',
                        labels={
                            'city': 'City',
                            'total_food_listings': 'Number of Food Listings',
                            'city_performance_score': 'Performance Score'
                        })
            
            fig.update_layout(xaxis={'categoryorder':'total descending'})
            fig = apply_readable_chart_style(fig, 
                                           "🌍 Top Cities by Food Availability", 
                                           "City", 
                                           "Number of Food Listings")
            charts['city_listings'] = fig

        # 4. Food Types Distribution - ENHANCED
        food_type_data = SQLQueries.get_most_common_food_types()
        if not food_type_data.empty:
            fig = px.pie(food_type_data.head(8), 
                        values='total_items', 
                        names='food_type',
                        hover_data=['total_quantity', 'claim_success_rate', 'supply_demand_ratio'],
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12
            )
            
            fig = apply_readable_chart_style(fig, "🍽️ Food Types Distribution")
            charts['food_type_distribution'] = fig

        # 5. Claims Status Analysis - ENHANCED
        claims_data = SQLQueries.get_claims_completion_percentages()
        if not claims_data.empty:
            colors = {
                'Completed': '#10b981',    # Green
                'Pending': '#f59e0b',      # Orange  
                'Cancelled': '#ef4444'     # Red
            }
            
            fig = px.pie(claims_data, 
                        values='claim_count', 
                        names='status',
                        hover_data=['percentage', 'total_quantity_involved', 'avg_quantity_per_claim'],
                        color='status',
                        color_discrete_map=colors)
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=14,
                textfont_color='white'
            )
            
            fig = apply_readable_chart_style(fig, "📈 Food Claims Status Distribution")
            charts['claims_analysis'] = fig

        # 6. Meal Type Demand - ENHANCED
        meal_data = SQLQueries.get_most_claimed_meal_types()
        if not meal_data.empty:
            fig = px.bar(meal_data.head(8), 
                        x='meal_type', 
                        y='total_claims',
                        color='success_rate',
                        hover_data=['total_quantity_distributed', 'demand_supply_ratio', 'success_rate'],
                        color_continuous_scale='Greens',
                        labels={
                            'meal_type': 'Meal Type',
                            'total_claims': 'Total Claims',
                            'success_rate': 'Success Rate (%)'
                        })
            
            fig = apply_readable_chart_style(fig, 
                                           "🍴 Most Demanded Meal Types", 
                                           "Meal Type", 
                                           "Number of Claims")
            charts['meal_claims'] = fig

        # 7. System Overview - ENHANCED
        system_data = SQLQueries.get_comprehensive_system_analysis()
        if not system_data.empty:
            metrics = ['total_providers', 'total_receivers', 'total_food_items', 'successful_distributions']
            values = [system_data.iloc[0][metric] for metric in metrics]
            labels = ['Food Providers', 'Food Receivers', 'Food Items Listed', 'Successful Distributions']
            
            fig = px.bar(x=labels, y=values,
                        color=values,
                        color_continuous_scale='RdYlBu_r',
                        labels={
                            'x': 'System Components',
                            'y': 'Count'
                        })
            
            # Add value labels on bars
            fig.update_traces(
                text=values,
                texttemplate='%{text:,}',
                textposition='outside',
                textfont=dict(size=14, color='#1f2937')
            )
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 System Overview Dashboard", 
                                           "System Components", 
                                           "Count")
            charts['system_overview'] = fig

    except Exception as e:
        st.error(f"Error creating enhanced charts: {e}")
        charts['error'] = str(e)
    
    return charts

# ========== NEW: ENHANCED TIME SERIES CHARTS ==========
def create_time_series_charts():
    """Create enhanced time series trend charts with improved readability"""
    charts = {}
    try:
        # 1. Claims Trends Over Time - ENHANCED
        claims_trends = SQLQueries.get_time_series_claims_trends()
        if not claims_trends.empty:
            fig = go.Figure()
            
            # Total claims line
            fig.add_trace(go.Scatter(
                x=claims_trends['claim_date'],
                y=claims_trends['total_claims'],
                mode='lines+markers',
                name='Total Claims',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=6, color='#3b82f6'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Total Claims:</b> %{y}<extra></extra>'
            ))
            
            # Completed claims line
            fig.add_trace(go.Scatter(
                x=claims_trends['claim_date'],
                y=claims_trends['completed_claims'],
                mode='lines+markers',
                name='Completed Claims',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6, color='#10b981'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Completed:</b> %{y}<extra></extra>'
            ))
            
            fig = apply_readable_chart_style(fig, 
                                           "📈 Food Claims Trends Over Time", 
                                           "Date", 
                                           "Number of Claims")
            charts['claims_time_series'] = fig

        # 2. Food Wastage vs Savings Timeline - ENHANCED
        food_trends = SQLQueries.get_time_series_food_listings_trends()
        if not food_trends.empty:
            fig = go.Figure()
            
            # Quantity saved (positive impact)
            fig.add_trace(go.Scatter(
                x=food_trends['expiry_date'],
                y=food_trends['quantity_saved'],
                mode='lines+markers',
                name='Food Saved (kg)',
                line=dict(color='#10b981', width=3),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.2)',
                marker=dict(size=5, color='#10b981'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Food Saved:</b> %{y} kg<extra></extra>'
            ))
            
            # Quantity wasted (negative impact)
            fig.add_trace(go.Scatter(
                x=food_trends['expiry_date'],
                y=food_trends['quantity_wasted'],
                mode='lines+markers',
                name='Food Wasted (kg)',
                line=dict(color='#ef4444', width=3),
                marker=dict(size=5, color='#ef4444'),
                hovertemplate='<b>Date:</b> %{x}<br><b>Food Wasted:</b> %{y} kg<extra></extra>'
            ))
            
            fig = apply_readable_chart_style(fig, 
                                           "🗑️ Food Wastage vs Savings Timeline", 
                                           "Expiry Date", 
                                           "Quantity (kg)")
            charts['wastage_timeline'] = fig

        # 3. Monthly Performance Dashboard - ENHANCED
        monthly_data = SQLQueries.get_monthly_performance_trends()
        if not monthly_data.empty:
            fig = go.Figure()
            
            # Claims bar chart
            fig.add_trace(go.Bar(
                x=monthly_data['month'],
                y=monthly_data['total_claims'],
                name='Total Claims',
                marker_color='rgba(59, 130, 246, 0.7)',
                marker_line=dict(color='#3b82f6', width=1),
                yaxis='y',
                hovertemplate='<b>Month:</b> %{x}<br><b>Claims:</b> %{y}<extra></extra>'
            ))
            
            # Success rate line
            fig.add_trace(go.Scatter(
                x=monthly_data['month'],
                y=monthly_data['monthly_success_rate'],
                mode='lines+markers',
                name='Success Rate (%)',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8, color='#10b981'),
                yaxis='y2',
                hovertemplate='<b>Month:</b> %{x}<br><b>Success Rate:</b> %{y}%<extra></extra>'
            ))
            
            fig.update_layout(
                yaxis=dict(
                    title='Number of Claims',
                    side='left',
                    showgrid=True,
                    gridcolor='#e5e7eb'
                ),
                yaxis2=dict(
                    title='Success Rate (%)',
                    side='right',
                    overlaying='y',
                    showgrid=False,
                    range=[0, 100]
                )
            )
            
            fig = apply_readable_chart_style(fig, 
                                           "📊 Monthly Performance & Success Trends", 
                                           "Month", 
                                           "Claims / Success Rate")
            charts['monthly_trends'] = fig

    except Exception as e:
        st.error(f"Error creating time series charts: {e}")
        charts['error'] = str(e)
    
    return charts

# ========== MAIN HEADER ==========
st.markdown("""
<div class="main-header">
    <h1>🌍 Food Wastage Management System</h1>
    <p>Connecting food providers with those in need • Reducing waste • Building community</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR NAVIGATION (FIXED) ==========
with st.sidebar:
    st.title("🧭 Navigation")
    current_page = st.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "🏢 Providers", "🤝 Receivers", "🥗 Food Listings", "📦 Claims", "📈 Analytics", "⏰ Time Series"]
    )

# ========== MAIN CONTENT ROUTER (FIXED) ==========
if current_page == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Display key metrics with enhanced visibility
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        system_data = SQLQueries.get_total_food_quantity_available()
        if not system_data.empty:
            row = system_data.iloc[0]
            
            with col1:
                st.metric("Total Food Items", f"{row['total_food_items']:,}")
            with col2:
                st.metric("Fresh Items", f"{row['fresh_items']:,}")
            with col3:
                st.metric("Total Providers", f"{row['contributing_providers']:,}")
            with col4:
                st.metric("Cities Covered", f"{row['cities_covered']:,}")
    except Exception as e:
        st.warning("Loading dashboard metrics...")
    
    # Display enhanced charts
    st.subheader("📈 Analytics Overview")
    charts = create_project_required_charts()
    
    for chart_name, chart in charts.items():
        if chart_name != 'error' and chart is not None:
            try:
                st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Error displaying chart {chart_name}: {e}")