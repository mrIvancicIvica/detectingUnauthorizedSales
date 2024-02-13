from flask import Flask, jsonify, request

app = Flask(__name__)


def identify_unauthorized_sales(product_listings, sales_transactions):
  unauthorized_sales = []
  product_listing_dict = {
      listing["productID"]: listing["authorizedSellerID"]
      for listing in product_listings
  }

  for transaction in sales_transactions:
    product_id = transaction["productID"]
    seller_id = transaction["sellerID"]

    if product_id in product_listing_dict and seller_id != product_listing_dict[
        product_id]:
      unauthorized_sales.append({
          "productID": product_id,
          "unauthorizedSellerID": seller_id
      })

  return unauthorized_sales


@app.route('/detect_unauthorized_sales', methods=['POST'])
def detect_unauthorized_sales():
    data = request.json

    if not data or "productListings" not in data or "salesTransactions" not in data:
        return jsonify({"error": "Invalid input data format"}), 400

    product_listings = data["productListings"]
    sales_transactions = data["salesTransactions"]

    unauthorized_sales = identify_unauthorized_sales(product_listings,
                                                     sales_transactions)

    return jsonify({"unauthorizedSales": unauthorized_sales}), 200



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
