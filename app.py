from flask import Flask, render_template, redirect, url_for, request, jsonify

import csv

app = Flask(__name__)

# Load quotes from CSV into a list
def load_quotes(filename):
    quotes = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes.append(row)
    return quotes


# Call the function and store the result in a variable
quotes = load_quotes('quotes.csv')

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html', quotes=quotes)

@app.route('/data-table')
def list_view():
    # You may need to pass any necessary data to the template here
    return render_template('data-table.html', quotes=quotes)



@app.route('/search_quotes', methods=['GET'])
def search_quotes():
    search_query = request.args.get('query', '')  # Get search query from URL parameter
    if not search_query:
        return jsonify([])  # Return empty list if no query

    # Filter quotes that match the search query
    # This is a basic example; you might want to make it more sophisticated
    filtered_quotes = [quote for quote in quotes if search_query.lower() in quote['quote_en'].lower()]

    return jsonify(filtered_quotes)  # Return filtered quotes as JSON
    
@app.route('/quote/<int:quote_id>')
@app.route('/quote/<int:quote_id>/page/<int:page>')
def quote(quote_id, page=1):
    # Convert quote_id to 0-based index
    index = quote_id - 1

    # Check if the quote_id is valid
    if index < 0 or index >= len(quotes):
        abort(404)

    # Get the quote
    quote = quotes[index]

    per_page = 10  # Number of quotes per page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    total_pages = (len(quotes) + per_page - 1) // per_page

    paginated_quotes = quotes[start_index:end_index]

    # Calculate next and previous quote IDs
    next_quote_id = quote_id + 1 if quote_id < len(quotes) else None
    prev_quote_id = quote_id - 1 if quote_id > 1 else None

    # Render the template with quote, list of all quotes, and pagination information
    return render_template('blog-list.html', quote=quote, quotes=paginated_quotes,
                           next_quote_id=next_quote_id, prev_quote_id=prev_quote_id,
                           page=page, total_pages=total_pages,
                           quote_id=quote_id)  # Pass quote_id to the template context

if __name__ == '__main__':
    app.run(debug=True)
