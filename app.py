from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/detect-unauthorized-sales", methods=["POST"])
def detect_unauthorized_sales():
  """
  This endpoint detects unauthorized sales from provided product listings and sales 
  transactions.

  Returns:
      JSON: A dictionary containing "unauthorizedSales" with identified unauthorized 
      transactions.
  """
  try:
    data = request.get_json()
    product_listings = data["productListings"]
    sales_transactions = data["salesTransactions"]

    # Validate input data
    if not product_listings or not sales_transactions:
      return jsonify(
          {"error": "Missing product listings or sales transactions"}), 400

    # Create a dictionary for authorized sellers per product
    authorized_sellers = {
        listing["productID"]: listing["authorizedSellerID"]
        for listing in product_listings
    }

    # Identify unauthorized sales transactions
    unauthorized_sales = []
    for transaction in sales_transactions:
      product_id = transaction["productID"]
      seller_id = transaction["sellerID"]

      if seller_id != authorized_sellers.get(product_id):
        unauthorized_sales.append({
            "productID": product_id,
            "unauthorizedSellerID": seller_id
        })

    return jsonify({"unauthorizedSales": unauthorized_sales}), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True)
