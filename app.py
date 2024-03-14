from flask import Flask, render_template, redirect, url_for
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

@app.route('/quote/<int:quote_id>')
def quote(quote_id):
    # Convert quote_id to 0-based index
    index = quote_id - 1

    # Check if the quote_id is valid
    if index < 0 or index >= len(quotes):
        abort(404)

    # Get the quote
    quote = quotes[index]

    # Calculate next and previous quote IDs
    next_quote_id = quote_id + 1 if quote_id < len(quotes) else None
    prev_quote_id = quote_id - 1 if quote_id > 1 else None
    # Render the template with quote and navigation information
    return render_template('blog-list.html', quote=quote, quotes=quotes, next_quote_id=next_quote_id, prev_quote_id=prev_quote_id)


if __name__ == '__main__':
    app.run(debug=True)
