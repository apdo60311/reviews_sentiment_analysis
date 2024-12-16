import requests
import json
import csv
import re

def get_deals():
    total_deals = []
    deals_url = "https://real-time-amazon-data.p.rapidapi.com/deals-v2"
    headers = {
        "x-rapidapi-key": "0f4cd697afmsh49efbfd224e4e0ap154fc6jsnc70902ede395",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }
    for i in range(1, 21):

        querystring = {"country":"US",
                       "min_product_star_rating":"ALL",
                       "price_range":"ALL",
                       "discount_range":"ALL",
                       "num_pages":i}



        response = requests.get(deals_url, headers=headers, params=querystring)
        deals = response.json()["data"]["deals"]
        total_deals.extend(deals)

    return total_deals


    

def get_reviews():
    total_asins = []
    
    data = {}
 
    with open('data.json') as json_file:
        data = json.load(json_file)
        deals = data["data"]["deals"]
        for deal in deals:
            asin = deal["product_asin"]
            total_asins.append(asin)

    url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
    procutUrl = "https://real-time-amazon-data.p.rapidapi.com/product-details"

    headers = {
        "x-rapidapi-key": "2a43b8abdbmsh00563875ee762f9p1a2d9bjsna5e2d899c1e2",
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }


    total_reviews = []

    for asin in total_asins:
        querystring = {
            "asin":asin,
            "country":"US",
            "sort_by":"TOP_REVIEWS",
            "star_rating":"ALL",
            "verified_purchases_only":"false",
            "images_or_videos_only":"false",
            "current_format_only":"false",
            "page":"1"}
        

        querystringProduct = {"asin":asin,"country":"US"}

        
        productD = requests.get(procutUrl, headers=headers, params=querystringProduct)

        
        productDetails = productD.json()["data"]["product_details"]
        product_title = productDetails.get("product_title", "")
        product_price = productDetails.get("product_price", "")
        product_total_rating = productDetails.get("product_star_rating", "")
        product_description = productDetails.get("product_description", "")
        product_brand = productDetails.get("product_details", {}).get("Brand", "")
        product_category = productDetails.get("category", {}).get("name", "")
    

        reviews = requests.get(url, headers=headers, params=querystring).json()["data"]["reviews"]
        
        for review in reviews:
            review["product_title"] = product_title
            review["product_price"] = product_price
            review["product_total_rating"] = product_total_rating
            review["product_description"] = product_description
            review["product_brand"] = product_brand
            review["product_category"] = product_category

    data[asin] = reviews
    with open('data-reviews.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=2))

    return data


def clean_text(text):
    if text is None:
        return ""
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace(',', '')
    text = re.sub(r'[^\w\s]', '', text)

    return text.strip()


get_reviews()

with open('data-reviews.json') as json_file:
    data = json.load(json_file)

    with open('reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['asin', 'title', 'comment', 'rate', 'helpful_votes', 'review_date', 'is_verified_purchase'])
        for asin, reviews in data.items():
            for review in reviews:
                title = clean_text(review["review_title"])
                comment = clean_text(review["review_comment"])
                rate = review["review_star_rating"]
                review_date = review["review_date"]

                product_title = review["product_title"] 
                product_price = review["product_price"] 
                product_total_rating = review["product_total_rating"] 
                product_description = clean_text(review["product_description"]) 
                product_brand = review["product_brand"] 
                product_category = review["product_category"] 


                is_verified_purchase = ""
                helpful_votes = ""
                
                if "is_verified_purchase" in review.keys(): 
                    is_verified_purchase = review["is_verified_purchase"]
                if "helpful_vote_statement" in review.keys():
                    helpful_votes = review["helpful_vote_statement"]                

                writer.writerow([asin, title, comment, rate, helpful_votes, review_date, is_verified_purchase])

