# rag_pipeline.py - SIMPLE WORKING VERSION
import pandas as pd
from typing import Tuple, Optional, Dict, Any
import warnings
warnings.filterwarnings('ignore')

class FinRAG:
    """Simple financial RAG system without complex dependencies"""
    
    def __init__(self):
        """Initialize the FinRAG system"""
        print("✓ FinRAG Financial Assistant Initialized")
    
    def query(self, question: str, df, chart_type: str = None) -> Tuple[str, Optional[Dict]]:
        """
        Query the financial data with a question and return answer + optional chart
        """
        try:
            # Check input
            if df is None or df.empty:
                return "No data available. Please upload transaction data first.", None
            
            # Helper for financial number formatting
            def format_currency(value):
                return f"₹{value:,.2f}"
            
            # Question analysis
            q = question.lower().strip()
            
            # Common questions and their responses
            if any(word in q for word in ["total", "spent", "spending", "reduce"]):
                # Calculate total spending
                if 'amount' in df.columns:
                    # Compute if this is net spending based on categories
                    # Income usually positive, expenses negative
                    try:
                        total_spent = df[df['amount'] < 0]['amount'].sum()
                        income = df[df['amount'] > 0]['amount'].sum()
                        net = total_spent + income  # total_spent is negative if it's expenses
                        
                        # For response, we want positive expense number
                        spending_amount = abs(total_spent)
                        income_amount = abs(income)
                        
                        if "spent on food" in q or "food" in q:
                            # Calculate food spending
                            food_df = df[df['category'].str.contains('food|dining|restaurant', case=False, na=False)]
                            if not food_df.empty and 'amount' in food_df.columns:
                                food_spent = food_df['amount'].sum()
                                response = f"Food spending: {format_currency(-food_spent)}" if food_spent < 0 else f"{format_currency(food_spent)}"
                            else:
                                response = f"You've spent ₹{spending:,.2f} on food/dining."
                            return response, None
                        else:
                            response = f"**Spending Summary:**\n"
                            response += f"• Total Spending: ₹{spending_amount:,.2f}\n"
                            response += f"• Total Income: ₹{income_amount:,.2f}\n"
                            response += f"• Net Change: ₹{(income_amount - spending_amount):,.2f}"
                            
                            # Add balance if column exists
                            if 'balance' in df.columns and not df.empty:
                                current_balance = df.iloc[-1]['balance'] if 'balance' in df.columns else 0
                                response += f"\n• Current Balance: ₹{current_balance:,.2f}"
                            
                            # Category breakdown
                            if 'category' in df.columns:
                                categories = df.groupby('category')['amount'].sum().sort_values()
                                if len(categories) > 0:
                                    response += f"\n\n**Spending by Category:**\n"
                                    for cat, amt in categories.items():
                                        response += f"  • {cat}: ₹{abs(amt):.0f}\n"
                            
                            return response, None
                    except Exception as e:
                        print(f"Error calculating amounts: {e}")
        
            elif "help" in q or "help" in q or "options" in q:
                help_text = "I can help you: (1) See spending by category, (2) Calculate total expenses, (3) Show balance trends, (4) Provide spending breakdowns, (5) Check if you can afford something"
                return help_text, None
                
            elif "balance" in q or "how much?" in q or "left" in q:
                if 'balance' in df.columns:
                    balance = df['balance'].iloc[-1] if not df.empty else 0
                    response = f"Current balance: ₹{balance:,.2f}"
                    
                    # Add simple line chart data
                    if 'date' in df.columns and 'balance' in df.columns:
                        chart_config = {
                            "type": "line",
                            "x": df['date'][-20:].tolist(),  # Last 20 points
                            "y": df['balance'][-20:].tolist(),
                            "title": "Balance Over Time",
                            "labels": {
                                "x": "Date",
                                "y": "Balance (₹)"
                            }
                        }
                        return f"Your current balance is ₹{balance:,.2f}", chart_config
                    
                    return response, None
                else:
                    return "Balance information not available in your data.", None
            
            # If no specific handler, default response
            response = f"I've analyzed your transaction data with {len(df)} records. "
            if 'category' in df.columns:
                categories = df['category'].unique()
                response += f"Categories found: {', '.join(categories[:5])}"  # Show first 5
                
                # Create expense breakdown chart data
                expense_df = df.copy()
                if 'amount' in expense_df.columns and 'category' in expense_df.columns:
                    expense_df = expense_df[expense_df['amount'] < 0]  # Negative amounts are expenses
                    category_totals = expense_df.groupby('category')['amount'].sum().abs()
                    
                    chart_config = {
                        "type": "pie",
                        "values": category_totals.values.tolist(),
                        "names": category_totals.index.tolist(),
                        "title": "Spending by Category"
                    }
                else:
                    chart_config = None
            else:
                chart_config = None

            response += "\n\nHow else can I help with your financial data?"

            return response, chart_config

        except Exception as e:
            return f"Analysis error: {str(e)[:200]}...", None
    
    def get_summary_statistics(self, df):
        """
        Calculate summary statistics
        """
        stats = {}
        
        if 'amount' in df.columns:
            stats['total_income'] = df[df['amount'] > 0]['amount'].sum()
            stats['total_expenses'] = abs(df[df['amount'] < 0]['amount'].sum())
            
        if 'balance' in df.columns and not df.empty:
            stats['current_balance'] = df['balance'].iloc[-1] if not df.empty else 0
            
        if 'category' in df.columns and df['category'].nunique() < 20:  # Limit for reasonable chart
            stats['top_categories'] = df.groupby('category').size().head(5).sort_values(ascending=False).index.tolist()
            
        return stats

    def suggest_budget(self, df):
        """Provide basic budget suggestions"""
        if df.empty:
            return "Upload data to get budgeting tips."
            
        suggestions = []
        
        if 'category' in df.columns and 'amount' in df.columns:
            # Find top spending categories
            expenses = df[df['category'] != 'Income']
            top_spending = expenses.groupby('category')['amount'].apply(lambda x: abs(x.sum()))
            top_categories = top_spending.nlargest(3).index.tolist()
            
            for cat in top_categories:
                suggestions.append(f"Review {cat} spending")
        
        return suggestions[:3]
    
    def detect_anomalies(self, df, amount_col='amount', method='iqr'):
        """Simple anomaly detection"""
        if df.empty or amount_col not in df.columns:
            return []
        
        # Simple IQR method for anomaly detection
        Q1 = df[amount_col].apply(pd.Series).quantile(0.25)
        Q3 = df[amount_col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalies = df[(df[amount_col] < lower_bound) | (df[amount_col] > upper_bound)]
        return anomalies.to_dict('records')