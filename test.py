from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import streamlit as st
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Set up Selenium WebDriver
def init_driver():
    service = webdriver.chrome.service.Service('D:\\chromedriver-win64\\chromedriver.exe')  # Update with your path
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Fetch product details from Amazon
def fetch_product_amazon(product_name):
    driver = init_driver()
    driver.get("https://www.amazon.in")
    
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    
    products = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
    product_list = []
    
    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, ".a-size-medium").text
            price = product.find_element(By.CSS_SELECTOR, ".a-price-whole").text
            product_list.append({"name": name, "price": price})
        except Exception:
            continue
    
    driver.quit()
    return product_list

# LLM-powered product matching using Mistral AI
# LLM-powered product matching using Mistral AI
def match_product_with_llm(input_product_name, product_list):
    # Converting the list into a string for easier processing by the LLM
    product_list_str = "\n".join([f"{i+1}: {product['name']}, Price: ₹{product['price']}, Weight: {product['weight']}" for i, product in enumerate(product_list)])
    
    prompt_template = """
    You are an intelligent assistant helping a user match the queried product with actual products listed on Amazon.
    
    The user is searching for "{input_product_name}". Here are the details of available products:
    
    {product_list_str}
    
    Please match the closest product that contains the same product type (e.g., tomato) and matches or is close to the requested weight. If no weight is specified, focus on the product type.
    
    Based on the list of products, match the closest product to "{input_product_name}".
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
    
    llm_chain = (
        prompt.format(
            input_product_name=input_product_name,
            product_list_str=product_list_str
        )
        | llm
        | StrOutputParser()
    )
    
    response = llm_chain.invoke({})
    
    return response

# Streamlit app
load_dotenv()
st.set_page_config(page_title="Price Comparison", page_icon=":shopping_cart:")
st.title("Product Price Comparison")

# Initialize product_list as empty
product_list = []

with st.sidebar:
    st.subheader("Enter Product Details")
    product_name = st.text_input("Product Name", value="")

    if st.button("Fetch Price"):
        with st.spinner("Scraping Amazon..."):
            product_list = fetch_product_amazon(product_name)
            if not product_list:
                st.error("No products found.")
            else:
                st.success("Products fetched successfully!")
                st.write(product_list)

        with st.spinner("Matching product using LLM..."):
            matched_product = match_product_with_llm(product_name, product_list)
            st.write(f"Matched Product: {matched_product}")

# Display fetched products
if product_list:  # Check if product_list is populated
    st.write("Available Products on Amazon:")
    for product in product_list:
        st.write(f"Product: {product['name']}, Price: ₹{product['price']}")
