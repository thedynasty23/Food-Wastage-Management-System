import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
