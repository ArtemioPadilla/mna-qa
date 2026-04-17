"""Compute total sales from a product catalogue and sales record."""
# Module name 'computeSales' is required by assignment (Req 4)
# pylint: disable=invalid-name

import json
import sys
import time


def load_json_file(file_path):
    """Load and parse a JSON file, exit on error."""
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: Invalid JSON in {file_path}: {exc}")
        sys.exit(1)
    return data


def build_price_catalogue(products):
    """Build a dict mapping product title to its price."""
    catalogue = {}
    for product in products:
        title = product.get("title")
        price = product.get("price")
        if title is not None and price is not None:
            catalogue[title] = price
    return catalogue


def compute_sales(catalogue, sales_data):
    """Process all sales and group results by sale ID."""
    grouped = {}
    errors = []

    for record in sales_data:
        sale_id = record.get("SALE_ID", "Unknown")
        product = record.get("Product", "Unknown")
        quantity = record.get("Quantity", 0)

        if product not in catalogue:
            errors.append(
                f"Error: Product '{product}' not in "
                f"catalogue (Sale {sale_id}). Skipping."
            )
            continue

        if not isinstance(quantity, (int, float)):
            errors.append(
                f"Error: Invalid quantity for "
                f"'{product}' (Sale {sale_id}). Skipping."
            )
            continue

        if quantity < 0:
            errors.append(
                f"Warning: Negative quantity ({quantity}) "
                f"for '{product}' (Sale {sale_id})."
            )

        price = catalogue[product]
        line_total = price * quantity

        if sale_id not in grouped:
            grouped[sale_id] = []
        grouped[sale_id].append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "line_total": line_total,
        })

    return grouped, errors


def calculate_grand_total(grouped_sales):
    """Sum all line totals across every sale."""
    total = 0.0
    for items in grouped_sales.values():
        for item in items:
            total += item["line_total"]
    return total


def format_report(grouped_sales, grand_total, elapsed):
    """Format sales results as a human-readable report."""
    lines = []
    sep = "=" * 60
    lines.append(sep)
    lines.append("SALES REPORT")
    lines.append(sep)

    for sale_id in sorted(grouped_sales.keys()):
        items = grouped_sales[sale_id]
        subtotal = sum(i["line_total"] for i in items)
        lines.append(f"\nSale {sale_id}:")
        lines.append("-" * 40)
        for item in items:
            name = item["product"]
            qty = item["quantity"]
            prc = item["price"]
            ltotal = item["line_total"]
            lines.append(
                f"  {name:<30} "
                f"{qty:>5} x ${prc:>8.2f}"
                f" = ${ltotal:>10.2f}"
            )
        lines.append(
            f"  {'Subtotal:':>49}"
            f" ${subtotal:>10.2f}"
        )

    lines.append("")
    lines.append(sep)
    lines.append(f"GRAND TOTAL: ${grand_total:,.2f}")
    lines.append(f"Elapsed time: {elapsed:.6f} seconds")
    lines.append(sep)

    return "\n".join(lines)


def main():
    """Execute the compute sales program."""
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    start_time = time.time()

    products = load_json_file(sys.argv[1])
    catalogue = build_price_catalogue(products)

    sales_data = load_json_file(sys.argv[2])
    grouped_sales, errors = compute_sales(catalogue, sales_data)

    for err in errors:
        print(err, file=sys.stderr)

    grand_total = calculate_grand_total(grouped_sales)
    elapsed = time.time() - start_time

    report = format_report(grouped_sales, grand_total, elapsed)
    print(report)

    output_path = "SalesResults.txt"
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(report + "\n")


if __name__ == "__main__":
    main()
