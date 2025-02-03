import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}

def run_queries_from_file(file_path):
    try:
        # Connect to the PostgreSQL database
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Read and execute queries from the file
                with open(file_path, "r") as sql_file:
                    sql_queries = sql_file.read().split(";")  # Split the file content into individual queries

                    for idx, query in enumerate(sql_queries):
                        if query.strip():  # Ignore empty queries
                            cursor.execute(query)  # Execute the query
                            result = cursor.fetchall()  # Fetch the result

                            # Write the result to a text file (result_query_n.txt)
                            result_file_path = f"/home/result_query_{idx + 1}.txt"
                            with open(result_file_path, "w") as result_file:
                                for row in result:
                                    result_file.write(str(row) + "\n")  # Write each row to the file

                            print(f"Query {idx + 1} executed and result saved to {result_file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    queries_file_path = "/home/queries.txt"  # Full path to your queries file in the container
    run_queries_from_file(queries_file_path)

