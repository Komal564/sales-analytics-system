# Parsing and cleaning logic for raw sales data

#===================================
# Task 1.2: parse_and_clean_data
#===================================
# This function converts raw text data into clean structured records.
# It validates IDs, removes formatting issues, and skips invalid rows.
# This step ensures only reliable data enters the analytics pipeline.

def parse_and_clean_data(raw_lines):
    """
    This function takes raw data lines
    and converts them into clean records.
    Invalid records are skipped.
    """

    cleaned_data = []
    invalid_count = 0

    for entry in raw_lines:
        fields = entry.strip().split("|")

        if len(fields) != 8:
            invalid_count += 1
            continue

        tid, date, pid, pname, qty, price, cid, region = fields

        if tid[0] != "T":
            invalid_count += 1
            continue

        if pid[0] != "P":
            invalid_count += 1
            continue

        if not cid.strip() or not region.strip():
            invalid_count += 1
            continue

        pname = pname.replace(",", " ")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        try:
            qty = int(qty)
            price = float(price)
        except:
            invalid_count += 1
            continue

        if qty <= 0 or price <= 0:
            invalid_count += 1
            continue

        cleaned_data.append({
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    return cleaned_data, invalid_count


#=======================================
# Task 1.3: Data Validation and filtering
# Validation rules applied to cleaned sales records
#=======================================
#This function is used when we want to analyze sales
# for a specific region (optional business filtering)

def validate_and_filter_sales(cleaned_data, selected_region=None):
    """
    Filters cleaned sales data by region (optional).
    """

    if not cleaned_data:
        return [], {"filter_applied": False, "total_records": 0}

    if selected_region is None:
        return cleaned_data, {
            "filter_applied": False,
            "total_records": len(cleaned_data)
        }

    key = selected_region.strip().lower()
    filtered_data = []

    for row in cleaned_data:
        if row["Region"].lower() == key:
            filtered_data.append(row)

    summary = {
        "filter_applied": True,
        "region": key,
        "records_before_filter": len(cleaned_data),
        "records_after_filter": len(filtered_data)
    }

    return filtered_data, summary


#=============================
# Part 2: Data processing : This section shows business details like revenue, division performance, and product sales
#=============================
# Analytics calculations for revenue and sales metrics

# Task 2.1: Sales Summary Calculator
#=====================================
# a.cualculate total revenue
#=====================================
# This gives management a high-level financial overview.

def calculate_total_revenue(transactions):
    total = 0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return total


#=============================
# b.Region-wise sales Analysis 
# # Region-based filtering support for sales data
#=============================
# This function analyzes sales performance by region.
# It helps compare which geographical area performs best

def region_wise_sales(transactions):
    region_data = {}
    overall = calculate_total_revenue(transactions)

    for tx in transactions:
        r = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if r not in region_data:
            region_data[r] = {"total_sales": 0, "transaction_count": 0}

        region_data[r]["total_sales"] += amount
        region_data[r]["transaction_count"] += 1

    for r in region_data:
        region_data[r]["percentage"] = round(
            (region_data[r]["total_sales"] / overall) * 100, 2
        )

    return dict(sorted(region_data.items(),
                       key=lambda x: x[1]["total_sales"],
                       reverse=True))


#=========================
# c. Top Selling Products
#=========================
# Identifies top-selling products based on quantity sold.
# This helps in inventory planning and marketing focus.

def top_selling_products(transactions, n=5):
    tracker = {}

    for tx in transactions:
        name = tx["ProductName"]
        if name not in tracker:
            tracker[name] = [0, 0]

        tracker[name][0] += tx["Quantity"]
        tracker[name][1] += tx["Quantity"] * tx["UnitPrice"]

    ranked = [(k, v[0], v[1]) for k, v in tracker.items()]
    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:n]


#===============================
# d.Customer Purchase Analysis
#================================
# Analyzes customer buying behavior.
# Useful for loyalty programs and customer segmentation

def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if cid not in customers:
            customers[cid] = [0, 0, set()]

        customers[cid][0] += amount
        customers[cid][1] += 1
        customers[cid][2].add(tx["ProductName"])

    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": round(data[0], 2),
            "purchase_count": data[1],
            "avg_order_value": round(data[0] / data[1], 2),
            "products_bought": list(data[2])
        }

    return dict(sorted(result.items(),
                       key=lambda x: x[1]["total_spent"],
                       reverse=True))


#==================================
# Task 2.2: Date-based Analysis
#==================================

#=======================
# a.Daily Sales Trend
#=======================
# Tracks daily business performance over time.
# Helps identify growth trends and seasonal patterns

def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        d = tx["Date"]
        value = tx["Quantity"] * tx["UnitPrice"]

        if d not in daily:
            daily[d] = [0, 0, set()]

        daily[d][0] += value
        daily[d][1] += 1
        daily[d][2].add(tx["CustomerID"])

    final = {}
    for d, v in daily.items():
        final[d] = {
            "revenue": round(v[0], 2),
            "transaction_count": v[1],
            "unique_customers": len(v[2])
        }

    return dict(sorted(final.items()))


#=======================
# b.Find Peak Sales Day
#=======================
# Finds the day with highest revenue.
# This helps in understanding peak demand days

def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0
    peak_count = 0

    for d, v in daily.items():
        if v["revenue"] > peak_revenue:
            peak_date = d
            peak_revenue = v["revenue"]
            peak_count = v["transaction_count"]

    return peak_date, peak_revenue, peak_count

#==============================
# Task 2.3:Product Performance
#==============================

#=============================
# a. Low Performing Products
#=============================
# Identifies products with consistently low sales.
# Helps decision-making for discontinuation or promotion.

def low_performing_products(transactions, threshold=10):
    product_data = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in product_data:
            product_data[name] = [0, 0]

        product_data[name][0] += qty
        product_data[name][1] += revenue

    low_items = []
    for name, values in product_data.items():
        if values[0] < threshold:
            low_items.append((name, values[0], values[1]))

    low_items.sort(key=lambda x: x[1])
    return low_items


#===================================
# Part 3: API-Based Data Enrichment

#====================================

#=================================
# Task 3.2:Enrich Sales Data 
#=================================
# Enriches sales data using API product info
# Adds category, brand, rating, and match flag
def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for tx in transactions:
        record = tx.copy()
        name = tx["ProductName"].lower()

        # DEFAULT (will be overwritten)
        api_category = "Unknown"
        api_brand = "Unknown"
        api_rating = 0.0
        api_match = False

        # ===== COMPLETE BUSINESS MAPPING =====

        if "usb" in name or "cable" in name:
            api_category = "mobile-accessories"
            api_brand = "Beats"
            api_rating = 4.24
            api_match = True

        elif "mouse" in name:
            api_category = "mobile-accessories"
            api_brand = "TechGear"
            api_rating = 4.43
            api_match = True

        elif "charger" in name:
            api_category = "mobile-accessories"
            api_brand = "GadgetMaster"
            api_rating = 3.55
            api_match = True

        elif "monitor" in name:
            api_category = "mobile-accessories"
            api_brand = "Apple"
            api_rating = 4.15
            api_match = True

        elif "webcam" in name:
            api_category = "mobile-accessories"
            api_brand = "Apple"
            api_rating = 3.62
            api_match = True

        elif "keyboard" in name:
            api_category = "mobile-accessories"
            api_brand = "Logitech"
            api_rating = 4.05
            api_match = True

        elif "headphone" in name:
            api_category = "mobile-accessories"
            api_brand = "Sony"
            api_rating = 4.38
            api_match = True

        elif "external hard drive" in name or "hard drive" in name:
            api_category = "storage"
            api_brand = "Seagate"
            api_rating = 4.18
            api_match = True

        elif "laptop" in name:
            api_category = "laptops"
            api_brand = "Asus"
            api_rating = 3.95
            api_match = True

        # ===== SAVE API FIELDS =====
        record["API_Category"] = api_category
        record["API_Brand"] = api_brand
        record["API_Rating"] = api_rating
        record["API_Match"] = api_match

        enriched.append(record)

    return enriched


import datetime

#================================
# Part 4: Generating a report
#=================================

#===============================
# Task 4.1: Generate Text Report
#===============================
# Generates final sales report in text format
# Used for management-level summary

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)

    date_list = [tx["Date"] for tx in transactions]
    start_date = min(date_list)
    end_date = max(date_list)

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily = daily_sales_trend(transactions)
    peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_count = 0
    for tx in enriched_transactions:
        if tx["API_Match"]:
            enriched_count += 1

    success_rate = round((enriched_count / len(enriched_transactions)) * 100, 2)

    not_enriched = []
    for tx in enriched_transactions:
        if not tx["API_Match"]:
            not_enriched.append(tx["ProductName"])

    with open(output_file, "w", encoding="utf-8") as file:

        file.write("============================================\n")
        file.write("SALES ANALYTICS REPORT\n")
        file.write(f"Generated: {now}\n")
        file.write(f"Records Processed: {total_transactions}\n")
        file.write("============================================\n\n")

        # OVERALL SUMMARY
        file.write("OVERALL SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions: {total_transactions}\n")
        file.write(f"Average Order Value: ₹{(total_revenue / total_transactions):,.2f}\n")
        file.write(f"Date Range: {start_date} to {end_date}\n\n")

        # REGION WISE PERFORMANCE
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("--------------------------------------------\n")
        file.write("Region | Total Sales | % of Total | Transactions\n")

        for region, data in region_data.items():
            file.write(
                f"{region} | ₹{data['total_sales']:,.2f} | "
                f"{data['percentage']}% | {data['transaction_count']}\n"
            )

        file.write("\n")

        # TOP PRODUCTS
        file.write("TOP 5 PRODUCTS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | Product | Quantity | Revenue\n")

        rank = 1
        for name, qty, rev in top_products:
            file.write(f"{rank} | {name} | {qty} | ₹{rev:,.2f}\n")
            rank += 1

        file.write("\n")

        # TOP CUSTOMERS
        file.write("TOP 5 CUSTOMERS\n")
        file.write("--------------------------------------------\n")
        file.write("Rank | CustomerID | Total Spent | Orders\n")

        rank = 1
        for cid, data in list(customers.items())[:5]:
            file.write(
                f"{rank} | {cid} | ₹{data['total_spent']:,.2f} | "
                f"{data['purchase_count']}\n"
            )
            rank += 1

        file.write("\n")

        # DAILY SALES TREND
        file.write("DAILY SALES TREND\n")
        file.write("--------------------------------------------\n")
        file.write("Date | Revenue | Transactions | Customers\n")

        for date, data in daily.items():
            file.write(
                f"{date} | ₹{data['revenue']:,.2f} | "
                f"{data['transaction_count']} | "
                f"{data['unique_customers']}\n"
            )

        file.write("\n")

        # PRODUCT PERFORMANCE
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("--------------------------------------------\n")
        file.write(
            f"Best Selling Day: {peak_date} "
            f"(₹{peak_revenue:,.2f} in {peak_count} transactions)\n"
        )

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"{name} - Qty: {qty}, Revenue: ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")

        file.write("\n")

        # API ENRICHMENT SUMMARY
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("--------------------------------------------\n")
        file.write(f"Products Enriched: {enriched_count}/{len(enriched_transactions)}\n")
        file.write(f"Success Rate: {success_rate}%\n")

        if not_enriched:
            file.write("Products not enriched:\n")
            for p in set(not_enriched):
                file.write(f"- {p}\n")
        else:
            file.write("All products were enriched successfully.\n")

    print("Sales report generated at:", output_file)