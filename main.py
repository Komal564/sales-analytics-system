# Entry point for running the sales analytics workflow
#===========================
# Part 5: Main Application:
# The main workflow manages the processing, analysis, and reporting of data.
#===========================

#===============================
# Task 5.1: Create Main Script
#===============================

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_and_clean_data,
    validate_and_filter_sales,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data,
    generate_sales_report
)
from utils.api_handler import fetch_all_products, create_product_mapping


def main():
    """
    This is the main execution function.
    It controls the complete flow of the application
    from reading the file till generating the final report.
    """

    try:
        print("========================================")
        print("SALES ANALYTICS SYSTEM")
        print("========================================")

        # Step 1 - Read file
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print("Successfully read " + str(len(raw_lines)) + " transactions")

        # Step 2 - Parse & clean
        print("[2/10] Parsing and cleaning data...")
        cleaned_data, invalid_count = parse_and_clean_data(raw_lines)
        print("Parsed records: " + str(len(cleaned_data)))
        print("Invalid records removed: " + str(invalid_count))

        # Step 3 - Show filter options
        print("[3/10] Filter Options Available:")
        cleaned_data, filter_summary = validate_and_filter_sales(cleaned_data)
        print("Filter Summary:", filter_summary)
        transactions = cleaned_data
        # Step 4 - Validation done
        print("[4/10] Validating transactions...")
        print("Valid records: " + str(len(cleaned_data)))

        # Step 5 - Sales analysis
        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(cleaned_data)
        region_wise_sales(cleaned_data)
        top_selling_products(cleaned_data)
        customer_analysis(cleaned_data)
        daily_sales_trend(cleaned_data)
        find_peak_sales_day(cleaned_data)
        low_performing_products(cleaned_data)
        print("Analysis complete")

        # Step 6 - Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        enriched_count = enrich_sales_data (transactions, product_mapping)

        # Step 7 - Enrich data
        print("[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(cleaned_data, product_mapping)

        enriched_count = 0
        for t in enriched_data:
            if t["API_Match"]:
                enriched_count += 1

        print(
            "Enriched " +
            str(enriched_count) + "/" +
            str(len(enriched_data)) +
            " transactions"
        )

        # Step 8 - Save enriched data
        print("[8/10] Saving enriched data...")
        file = open("data/enriched_sales_data.txt", "w", encoding="utf-8")

        header = (
            "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
            "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        )
        file.write(header)

        for t in enriched_data:
            line = (
                t["TransactionID"] + "|" +
                t["Date"] + "|" +
                t["ProductID"] + "|" +
                t["ProductName"] + "|" +
                str(t["Quantity"]) + "|" +
                str(t["UnitPrice"]) + "|" +
                t["CustomerID"] + "|" +
                t["Region"] + "|" +
                str(t["API_Category"]) + "|" +
                str(t["API_Brand"]) + "|" +
                str(t["API_Rating"]) + "|" +
                str(t["API_Match"]) + "\n"
            )
            file.write(line)

        file.close()
        print("Saved to: data/enriched_sales_data.txt")

        # Step 9 - Generate report
        print("[9/10] Generating report...")
        generate_sales_report(
            cleaned_data,
            enriched_data,
            "output/sales_report.txt"
        )
        print("Report saved to: output/sales_report.txt")

        # Step 10 - Done
        print("[10/10] Process Complete!")
        print("========================================")

    except Exception as e:
        print("An error occurred:", e)


# Run the program
if __name__ == "__main__":
    main()