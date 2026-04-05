import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\hp\Desktop\Data analysis\Projects\customer_transactions_project2.csv")
df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"])
print(f"✅ Loaded {len(df)} transactions from {df['Customer_ID'].nunique()} customers")


analysis_Date = pd.to_datetime('2024-09-01')

rfm = df.groupby('Customer_ID').agg({
    'Purchase_Date':lambda x:(analysis_Date-x.max()).days,
    'Transaction_ID':'count',
    'Amount':'sum'
}).reset_index()
rfm.columns = ['Customer_ID','Recency','Frequency','Monetary']  
customer_info = df.groupby('Customer_ID')[['Customer_Name','City','Region']].first().reset_index()
rfm = rfm.merge(customer_info,on=['Customer_ID'])



print("Segment Customers")
def segment_customer(row):
    if row["Frequency"]>=5 and row["Monetary"]>=1200:
        return "VIP"
    elif row["Frequency"]>=3 and row["Monetary"]>=300:
        return 'Loyal'
    elif row['Recency']>90:
        return"At Risk"
    elif row['Frequency'] ==1:
        return "One-Time"
    else :
        return"Regular"
rfm['Segment'] = rfm.apply(segment_customer,axis=1)
print(rfm.head(10))
print("✅ Customer segmentation complete")


print('\n'+'='*30)
print("Key matrics: \n")
total_customers = len(rfm)
total_revenue = rfm['Monetary'].sum()
avg_customer_value = rfm['Monetary'].mean()
total_transactions = len(df)
print(f" Total Customers: {total_customers}")
print(f" Total Revenue: {total_revenue}")
print(f" Avg Customer Value: {avg_customer_value}")
print(f" Total Transactions: {total_transactions}")
print("="*50)
print("\n Top 5 Customers: ")
print(rfm.nlargest(5,"Monetary")[["Customer_Name","Frequency","Recency","Monetary","Segment"]])

print("\n customer segments: ")
segment_summary=rfm.groupby("Segment").agg({
    "Customer_ID":"count",
    "Monetary":['sum','mean'],
    "Frequency":"mean"
}).round(2)
segment_summary.columns=['customer_count','Total_revenue','avg_spend','avg_frequancy']
print(segment_summary)

print("="*50)

print('Customer Retention:')
one_time = len(rfm[rfm["Frequency"]==1])
repeat = len(rfm[rfm['Frequency']>1])
print(f"One-Time Customer: {one_time} ")
print(f"Rpeat Customer: {repeat} ")
print("="*50)
print("additional analysis:")

print("\n Top Regions:")
top_regions = df.groupby("Region").agg({
    'Customer_ID':'nunique',
    'Transaction_ID':'count',
    'Amount':'sum'
}).sort_values('Amount', ascending=False)
top_regions.columns = ['Unique_Customers', 'Transactions', 'Revenue']
print(top_regions)

print(f"\n PRODUCT CATEGORIES:")
categories = df.groupby('Product_Category').agg({
    'Transaction_ID': 'count',
    'Amount': ['sum', 'mean']
}).round(2)
categories.columns = ['Transactions', 'Total_Revenue', 'Avg_Order_Value']
print(categories)

print(f"\n TOP 10 CITIES:")
cities = df.groupby('City').agg({
    'Customer_ID': 'nunique',
    'Amount': 'sum'
}).sort_values('Amount', ascending=False).head(10)
cities.columns = ['Customers', 'Revenue']
print(cities)



fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Customer Segmentation Analysis', fontsize=16, fontweight='bold')


segment_counts = rfm['Segment'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
ax1.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
ax1.set_title('Customer Distribution by Segment')


segment_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)
ax2.bar(segment_revenue.index, segment_revenue.values, color=colors[:len(segment_revenue)])
ax2.set_title('Total Revenue by Customer Segment')
ax2.set_ylabel('Revenue ($)')
ax2.set_xlabel('Segment')
for i, v in enumerate(segment_revenue.values):
    ax2.text(i, v, f'${v:,.0f}', ha='center', va='bottom')


top10 = rfm.nlargest(10, 'Monetary')
ax3.barh(range(len(top10)), top10['Monetary'].values, color='#4ECDC4')
ax3.set_yticks(range(len(top10)))
ax3.set_yticklabels(top10['Customer_Name'].values)
ax3.set_xlabel('Total Spent ($)')
ax3.set_title('Top 10 Customers by Spending')
ax3.invert_yaxis()


colors_map = {'VIP': '#FF6B6B', 'Loyal': '#4ECDC4', 'At-Risk': '#45B7D1', 
              'One-Time': '#FFA07A', 'Regular': '#98D8C8'}
for segment in rfm['Segment'].unique():
    segment_data = rfm[rfm['Segment'] == segment]
    ax4.scatter(segment_data['Frequency'], segment_data['Monetary'], 
                label=segment, alpha=0.6, s=100, color=colors_map.get(segment, 'gray'))
ax4.set_xlabel('Purchase Frequency (# of purchases)')
ax4.set_ylabel('Total Spent ($)')
ax4.set_title('Customer Segments: Frequency vs Spending')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('customer_analysis_charts.png', dpi=300, bbox_inches='tight')
print("✅ Charts saved: 'customer_analysis_charts.png'")
plt.close()


with pd.ExcelWriter('customer_analysis_data.xlsx', engine='openpyxl') as writer:
    rfm.to_excel(writer, sheet_name='RFM Analysis', index=False)
    segment_summary.to_excel(writer, sheet_name='Segment Summary')
    top_regions.to_excel(writer, sheet_name='Regional Analysis')
    categories.to_excel(writer, sheet_name='Category Analysis')
    cities.to_excel(writer, sheet_name='Top Cities')
    df.to_excel(writer, sheet_name='All Transactions', index=False)


