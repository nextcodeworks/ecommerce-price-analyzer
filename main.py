"""
Web Scraping and Data Visualization Dashboard

This application scrapes product data from webscraper.io test e-commerce site,
analyzes price trends, and displays visualizations in a Tkinter GUI.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ====================== FIXED VARIABLES ======================
SCRAPING_URL = "https://webscraper.io/test-sites/e-commerce/allinone"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# CSS Selectors for the target website
PRODUCT_CARD_CLASS = "product-wrapper"
PRODUCT_NAME_CLASS = "title"
PRODUCT_PRICE_CLASS = "price"
PRODUCT_RATING_ATTR = "data-rating"
# =============================================================

class WebScraperApp:
    def __init__(self, root):
        """
        Initialize the main application window
        """
        self.root = root
        self.root.title("E-Commerce Data Analyzer | github.com/isthorius")
        self.root.geometry("1000x800")
        
        # Store scraped data
        self.data = None
        
        # Create GUI components
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create and arrange all GUI components
        """
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Control panel frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Scrape button
        self.scrape_btn = ttk.Button(
            control_frame, 
            text="Scrape Data", 
            command=self.scrape_data
        )
        self.scrape_btn.pack(side=tk.LEFT, padx=5)
        
        # Analysis options
        self.analysis_var = tk.StringVar()
        analysis_options = [
            "Price Distribution",
            "Price Over Time",
            "Top Rated Products",
            "Category Distribution"
        ]
        
        self.analysis_menu = ttk.Combobox(
            control_frame,
            textvariable=self.analysis_var,
            values=analysis_options,
            state="readonly"
        )
        self.analysis_menu.set("Select Analysis")
        self.analysis_menu.pack(side=tk.LEFT, padx=5)
        self.analysis_menu.bind("<<ComboboxSelected>>", self.update_visualization)
        
        # Refresh button
        refresh_btn = ttk.Button(
            control_frame,
            text="Refresh",
            command=self.update_visualization
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Data display frame
        data_frame = ttk.LabelFrame(main_frame, text="Data", padding="10")
        data_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for data display
        self.tree = ttk.Treeview(data_frame)
        
        # Vertical Scrollbar
        y_scroll = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal Scrollbar
        x_scroll = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Visualization frame
        vis_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        vis_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Matplotlib figure
        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=vis_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def scrape_data(self):
        """
        Scrape product data from the e-commerce website
        """
        try:
            self.status_var.set("Scraping data... Please wait")
            self.root.update_idletasks()
            
            # Send HTTP request
            response = requests.get(SCRAPING_URL, headers=HEADERS)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract product data using the fixed selectors
            product_cards = soup.find_all('div', class_=PRODUCT_CARD_CLASS)
            
            data = []
            for product in product_cards:
                try:
                    name = product.find('a', class_=PRODUCT_NAME_CLASS).text.strip()
                    price = float(product.find('h4', class_=PRODUCT_PRICE_CLASS).text.replace('$', ''))
                    rating = float(product.find('div', class_='ratings').get(PRODUCT_RATING_ATTR, 0))
                    # Since the test site doesn't have categories, we'll use a placeholder
                    category = "Electronics"  # Placeholder as the test site doesn't have categories
                    date_added = datetime.now().strftime('%Y-%m-%d')
                    
                    data.append({
                        'Name': name,
                        'Price': price,
                        'Rating': rating,
                        'Category': category,
                        'Date': date_added
                    })
                except Exception as e:
                    print(f"Error parsing product: {e}")
                    continue
            
            # Create DataFrame
            self.data = pd.DataFrame(data)
            
            # Update data display
            self.update_data_display()
            
            self.status_var.set(f"Successfully scraped {len(self.data)} products")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scrape data: {str(e)}")
            self.status_var.set("Scraping failed")
    
    def update_data_display(self):
        """
        Update the Treeview with the scraped data
        """
        if self.data is None:
            return
            
        # Clear existing data and columns
        self.tree.delete(*self.tree.get_children())
        
        # Remove all existing columns
        for col in self.tree["columns"]:
            self.tree.column(col, width=0, minwidth=0)
            self.tree.heading(col, text="")
        
        # Set up columns
        self.tree["columns"] = list(self.data.columns)
        
        # Create the first column (tree column) with empty text
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="")
        
        # Configure the rest of the columns
        for col in self.data.columns:
            self.tree.column(col, anchor=tk.W, width=150)
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # Add data rows
        for _, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=list(row))
    
    def update_visualization(self, event=None):
        """
        Update the visualization based on selected analysis type
        """
        if self.data is None or self.data.empty:
            messagebox.showwarning("No Data", "Please scrape data first")
            return
            
        selected_analysis = self.analysis_var.get()
        
        # Clear previous figure
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        
        try:
            if selected_analysis == "Price Distribution":
                self.data['Price'].plot(kind='hist', bins=20, ax=ax, edgecolor='black')
                ax.set_title('Price Distribution')
                ax.set_xlabel('Price ($)')
                ax.set_ylabel('Number of Products')
                
            elif selected_analysis == "Price Over Time":
                # Group by date and calculate average price
                price_over_time = self.data.groupby('Date')['Price'].mean()
                price_over_time.plot(kind='line', marker='o', ax=ax)
                ax.set_title('Average Price Over Time')
                ax.set_xlabel('Date')
                ax.set_ylabel('Average Price ($)')
                ax.grid(True)
                
            elif selected_analysis == "Top Rated Products":
                # Get top 10 rated products
                top_rated = self.data.nlargest(10, 'Rating')
                top_rated.plot(kind='bar', x='Name', y='Rating', ax=ax)
                ax.set_title('Top Rated Products')
                ax.set_xlabel('Product Name')
                ax.set_ylabel('Rating')
                ax.tick_params(axis='x', rotation=45)
                
            elif selected_analysis == "Category Distribution":
                # Since we're using a placeholder category, this will show all as Electronics
                category_counts = self.data['Category'].value_counts()
                category_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
                ax.set_title('Product Categories Distribution')
                ax.set_ylabel('')
                
            else:
                return
                
            # Adjust layout and redraw
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create visualization: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
