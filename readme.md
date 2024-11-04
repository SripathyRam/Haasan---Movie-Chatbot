# Chat with MySQL

This project is a simple chat application that allows users to interact with a MySQL database using natural language queries. The application is built using **Streamlit** for the front-end interface, **MySQL** for the database, and **LangChain** with **GroqCloud API** for natural language processing and query generation.

## Features

- **Natural Language Queries**: Allows users to ask questions in natural language and generates SQL queries to fetch the corresponding data from a MySQL database.
- **Database Interaction**: Connects to any MySQL database using user-provided credentials and interacts with the schema to query and retrieve results.
- **Streamlit UI**: Provides a user-friendly interface built with Streamlit for easy interaction.

## Running the Application

- To run this project, you need to install the required packages. You can do this by running:
pip install -r requirements.txt
- Create a .env File: Make sure to create a .env file in the root directory of the project and add your GroqCloud API key in the following format:
GROQ_API_KEY=your_groqcloud_api_key
- Start the Streamlit application by executing the following command:
streamlit run app.py


## Usage

- When the application starts, enter your MySQL database credentials accordingly. For example, you can use the classicmodels database for testing.
- Once the application is running, you can type your questions into the chat interface.
- The assistant will respond with natural language answers based on the SQL queries executed against the connected database.


## Acknowledgments

- Streamlit - for building the web application.
- LangChain - for integrating language models.
- GroqCloud - for natural language processing capabilities.