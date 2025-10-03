from flask import Flask, render_template, request, redirect, url_for
import time

# Initialize the Flask application
app = Flask(__name__)

# Simple in-memory list to simulate a database for posts
posts = [
    {
        'id': 1,
        'author': 'Gemini',
        'text': 'Welcome to the MicroBlog MVP! This simple app demonstrates basic Flask routing, form handling, and template rendering. Start typing your own posts below!',
        'timestamp': time.time()
    },
    {
        'id': 2,
        'author': 'User 1',
        'text': 'Just testing out this new microblog. Flask makes getting started so easy!',
        'timestamp': time.time() - 3600
    }
]
# Initialize a counter for unique post IDs
post_id_counter = 3

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles both displaying the post feed (GET) and adding new posts (POST).
    """
    global post_id_counter

    if request.method == 'POST':
        # Get data from the submitted form
        author = request.form.get('author', 'Anonymous').strip() or 'Anonymous'
        text = request.form.get('text', '').strip()

        if text:
            # Create a new post object
            new_post = {
                'id': post_id_counter,
                'author': author,
                'text': text,
                'timestamp': time.time()
            }
            # Add the new post to the list (in-memory storage)
            posts.insert(0, new_post) # Insert at the beginning to show newest first
            post_id_counter += 1
            
            # Redirect to the homepage to prevent form re-submission on refresh
            return redirect(url_for('index'))

    # Sort posts by timestamp (newest first) for consistent display
    sorted_posts = sorted(posts, key=lambda p: p['timestamp'], reverse=True)
    
    # Render the HTML template, passing the sorted list of posts
    return render_template('index.html', posts=sorted_posts)

# Helper function to format the timestamp
@app.template_filter('datetimeformat')
def datetimeformat(timestamp):
    """Formats a UNIX timestamp into a human-readable string."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # Run the application in debug mode for development
    # Accessible via http://127.0.0.1:5000/
    app.run(debug=True)
