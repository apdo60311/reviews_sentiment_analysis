from bs4 import BeautifulSoup
import requests
import json
import re


def validate_url(url):
    if "amazon" in url:
        return True
    else:
        return False    


def scrape(url):
    if validate_url(url):
        try:
            print("scraping")
            return scrape_amazon_reviews(url) 
        except Exception as e:
            print(f"Error scraping URL: {url}")
            print(f"Error message: {str(e)}")
            return None
    else:
        return None
    

# def parse_date(obj):
#     if 'Date' in obj:
#         # October 8, 2024
#         date_match = re.search(r'(\w+ \d+, \d{4})', obj['Date'])
#         return date_match.group(1) if date_match else None
#     else: 
#         return None

def scrape_amazon_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        review_containers = soup.find_all('div', {'data-hook': 'review'})
        if not review_containers:
            review_containers = soup.find_all('li', {'class': 'review'})

        reviews = []
        
        print(f"Number of reviews found: {len(review_containers)}")

        for review in review_containers:
            try:
                reviewer_element = review.find('span', class_='a-profile-name')
                reviewer = reviewer_element.text.strip() if reviewer_element else 'Anonymous'
                
                title_element = review.find('a', {'data-hook': 'review-title'})
                title = title_element.text.strip() if title_element else 'No Title'
                
                rating_element = review.find('i', {'data-hook': 'review-star-rating'})
                if rating_element:
                    rating = rating_element.text.split()[0]
                else:
                    rating_element = review.find('i', {'class': 'a-icon-star'})
                    rating = rating_element.text.split()[0] if rating_element else 'N/A'
                
                date_element = review.find('span', {'data-hook': 'review-date'})
                date = date_element.text.strip() if date_element else 'No Date'
                
                review_text_element = review.find('span', {'data-hook': 'review-body'})
                if review_text_element:
                    review_text = review_text_element.text.strip()
                else:
                    review_text_element = review.find('div', {'class': 'reviewText'})
                    review_text = review_text_element.text.strip() if review_text_element else 'No Review Text'
                
                verified_element = review.find('span', {'data-hook': 'avp-badge-linkless'})
                verified = True if verified_element else False
                
                helpful_element = review.find('span', {'data-hook': 'helpful-vote-statement'})
                if helpful_element:
                    helpful_text = helpful_element.text.strip()
                    helpful_votes = ''.join(filter(str.isdigit, helpful_text)) or '0'
                else:
                    helpful_votes = '0'
                
                review_dict = {
                    'Reviewer': reviewer,
                    'Title': title,
                    'Rating': rating,
                    'Date': date,
                    'Review': review_text,
                    'Verified Purchase': verified,
                    'Helpful Votes': helpful_votes
                }
                
                reviews.append(review_dict)
                
            except Exception as e:
                print(f"Error extracting individual review: {e}")
                continue
        
        return reviews
    
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

url = "https://www.amazon.com/Gaming-Keyboard-Headset-Backlight-Bundle/dp/B07TVK8WJP/ref=sr_1_2?_encoding=UTF8&content-id=amzn1.sym.12129333-2117-4490-9c17-6d31baf0582a&dib=eyJ2IjoiMSJ9.POKqznyD1Ofh52-SMozP4an1VlCT4al4bu9bHNy3MdJme6Bkepdy3R4ATqtH8rFsarjpbYU7FPjFVpbzzkJRw9A96-GRjlfkWRK-YfL4rBCZAsRAJiGPeJuGAUHpSKk4vRXH61IVT4qYvDv8768JMwLOHX5gJIB6hhY0zJWXcEjPG8yNNcNU8_QIEZ3J59vGCG8nFar5u9vXFD25yXUz6-pqEIU9ha3hOk_WO99KUFs.7dZW-GyaJzYGvYiSz0nqGoAwJzB0f1iUCmPLkZ7nBRw&dib_tag=se&keywords=gaming%2Bkeyboard&pd_rd_r=4ac527d4-3cf3-4c07-ada4-c3f213b12529&pd_rd_w=MIPZr&pd_rd_wg=bXbbf&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=V4E67CG7ZNV6TK5J64N5&qid=1734471771&sr=8-2&th=1"

all = scrape(url)

print(all)

# reviews = {"reviews": all}

# for review in reviews['reviews']:
#     print(review)

# with open('reviews.json', 'w') as json_file:
#     json_file.write(json.dump(reviews, json_file, indent=4))




