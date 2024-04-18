import streamlit as st
import os
import pandas as pd
import unicodedata
import matplotlib.pyplot as plt
import base64

# Adjusting the function to handle Turkish-specific case conversion
def turkish_lower(s):
    return unicodedata.normalize('NFKC', s).replace('İ', 'i').replace('Ş', 'ş').lower()

# Function to categorize each expense based on the Turkish operation description
def categorize_expense_tr(operation):
    operation = turkish_lower(operation)
    for category, category_keywords in keywords.items():
        if any(keyword in operation for keyword in category_keywords):
            return category
    return "Other"

# Define keywords and color map
keywords = {
    "Food & Drink": ["a.ç.t. dürüm ve meze", "arkestra", "bakery", "bakes", "bakkal", "bim","bordel", "cagrim", "dondurma", "ebsm et balik", "firin", "gida","gozde sarkuteri", "harman firin", "kafe", "kahve", "lokanta", "market","cafe","marmaris büfe", "migros", "mill cafe", "minimal kahve mutfak", "mopas", "mudavim", "müdavim lokantasi", "narbakery", "nicel bakes scoops", "parantez panayir yerigida", "perakende", "pinar dondurma", "rest", "restaurant", "restoran", "salipazari", "salipazari yavuzun y", "sarkuteri","şarküteri","su urunleri", "süpermarket", "tove gida", "unlu mamüller", "unlumamüller", "mc donalds", "çağrım unlu mamuller", "çağrım unlu mamüller","sour","sweet","benazio","kahve","mutfak","village","şok","haci bekir","kafe","yemek","burger","caffe","happy center","tekel","ekşihane","gelato","sorbet","kuruyemis","kuruyemiş","haribo","kimyon","kuruyemiş"],
    "Home+Health": ["eczane", "sağlık", "fatura", "ev", "kira", "iski su", "enerjisa ayesaş","ikea","bauhaus","türk telekom mobil", "turkcell superonline","carrefour","kozmetik"],
    "Clothes+Beauty+Utilities": ["giyim", "kıyafet", "moda", "güzellik", "kuaför","beymen","vakko","zorlu","atasun","kuvars","brooks brothers","barcin","h&m","cos","spor","ralph lauren","decathlon","tekstil","massimo","zara","sportive","mudo","mango","apple store","levis","oysho","trendyol","gratis","benetton"],
    "Entertainment": ["sinema", "film", "eğlence", "oyun", "konser","etkinlik","passo","müzik","muzik"],
    "Travel": ["ita","fr","prt","seyahat", "uçuş", "otel", "tren", "otobüs","uber","airbnb","moov","belbim","booking","bitaksi","takside","lisboa","sabiha gökçen"],
    "Subscription": ["spotify", "netflix", "prime", "hbo", "patreon","apple.com/bill","google"],
    "Tax": ["vergi","v.d."],
    "Other": []  # No specific keywords for 'Other'; it's a default category
}

color_map = {
    "Food & Drink": 'blue',
    "Home+Health": 'green',
    "Clothes+Beauty+Utilities": 'red',
    "Entertainment":"orange",
    "Travel": "purple",
    "Subscription": "yellow",
    "Tax": "brown",
    "Other": "grey",
    "Skipped": "lightblue"
}

def process_expense_file(file_path):
    expenses_df = pd.read_excel(file_path)
    expenses_df.columns = ['operation', 'amount', 'currency', 'date', 'points', 'description']
    expenses_df = expenses_df.drop(expenses_df.index[0])
    expenses_df = expenses_df.drop('points', axis=1)
    expenses_df['category'] = expenses_df['operation'].apply(categorize_expense_tr)
    return expenses_df

def plot_expense_categories(expenses_df):
     # Calculate category percentages
    category_percentages = expenses_df['category'].value_counts(normalize=True) * 100
    colors = [color_map[category] for category in category_percentages.index]
    
    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(category_percentages, labels=category_percentages.index, autopct='%1.1f%%', colors=colors)
    ax.set_title('Expense Categories')
    
    # Display the plot using st.pyplot()
    st.pyplot(fig)

def main():
    st.title('Expense Categorization App')
    st.write("This app helps you to see which categories your expenses fall under by uploading an Excel file with transaction data. 🕵️")

    st.markdown("## VIEW RESULTS OF SAMPLE DATA")
    st.write("Click below to see results with sample data")

    if st.button("Show Sample Data Results"):
        sample_data_path = "expense_template_filled.xlsx"
        sample_expenses_df = process_expense_file(sample_data_path)

        st.subheader("Sample Data")
        st.write(sample_expenses_df)

        st.subheader("Sample Expense Categories")
        plot_expense_categories(sample_expenses_df)

    # Add horizontal separator
    st.markdown("<hr>", unsafe_allow_html=True)

    # Provide Excel template for user to download
    st.markdown("## TRY WITH YOUR DATA")
    st.markdown("### Step 1: Create your expense data in the template")
    st.write("Download the Excel template to enter your expense data:")
    excel_template_path = "expense_template.xlsx"    
    # Display a download button for the Excel template
    with open(excel_template_path, 'rb') as f:
        excel_template_bytes = f.read()

    # Create a download link for the Excel template
    b64 = base64.b64encode(excel_template_bytes).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="excel_template.xlsx">Download Excel Template</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Allow user to upload their expense file
    st.markdown("### Step 2: Upload your filled expense spreadsheet")
    uploaded_file = st.file_uploader("Choose a file", type="xlsx")
 
    if uploaded_file is not None:
        # Process uploaded file
        st.write("### Uploaded File Details:")
        st.write(uploaded_file.name)
        expenses_df = process_expense_file(uploaded_file)

        # Display raw data
        st.subheader("Raw Data")
        st.write(expenses_df)

        # Plot expense categories
        st.subheader("Expense Categories")
        plot_expense_categories(expenses_df)


    

if __name__ == "__main__":
    main()
