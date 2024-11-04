import requests
from bs4 import BeautifulSoup
import mysql.connector

def scrape_bollywood_movies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing movie data
    table = soup.find('table')  # Assuming the data is in a table

    movies = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        columns = row.find_all('td')
        if len(columns) >= 7:  # Ensure there are enough columns
            sn = columns[0].text.strip()  # Serial number
            title = columns[1].text.strip()  # Movie title
            
            # Function to safely convert strings to floats or return None
            def safe_float(value):
                if value.strip() == '-' or value.strip() == '':
                    return None  # or you could use 0.0
                return float(value.strip().replace(',', ''))

            worldwide = safe_float(columns[2].text)  # Worldwide gross
            india_net = safe_float(columns[3].text)  # India Net
            india_gross = safe_float(columns[4].text)  # India Gross
            overseas = safe_float(columns[5].text)  # Overseas
            budget = safe_float(columns[6].text)  # Budget
            verdict = columns[7].text.strip()  # Verdict
            
            # Append movie data as a tuple
            movies.append((sn, title, worldwide, india_net, india_gross, overseas, budget, verdict))
    return movies

def insert_movies_to_mysql(movies, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create a table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bollywood_movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sn INT,
                title VARCHAR(255),
                worldwide FLOAT,
                india_net FLOAT,
                india_gross FLOAT,
                overseas FLOAT,
                budget FLOAT,
                verdict VARCHAR(255)
            )
        """)

        # Insert scraped movies into the table
        for movie in movies:
            cursor.execute("""
                INSERT INTO bollywood_movies (sn, title, worldwide, india_net, india_gross, overseas, budget, verdict)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, movie)

        connection.commit()
        print(f"{cursor.rowcount} movies inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
url = 'https://www.sacnilk.com/entertainmenttopbar/Top_500_Bollywood_Movies_Of_All_Time'
db_config = {
    'user': 'root',
    'password': 'sri2003inmysql',
    'host': 'localhost',
    'database': 'movie'
}

movies_data = scrape_bollywood_movies(url)
insert_movies_to_mysql(movies_data, db_config)
