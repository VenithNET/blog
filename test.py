import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
import datetime  # Import the datetime module

app = Flask(__name__)

# Folder to store blog HTML files
blog_folder = "blogs"
if not os.path.exists(blog_folder):
    os.makedirs(blog_folder)

# Initialize an empty list to store blog data
blogs = []

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        author_name = request.form['author']

        # Check if the date is provided in the form data
        if 'date' in request.form:
            blog_date = request.form['date']
        else:
            # If no date is provided, use the default date "01/01/2023"
            blog_date = '01/01/2023'

        # Store the blog in the JSON database along with the date
        blog = {
            'title': blog_title,
            'content': blog_content,
            'author': author_name,
            'date': blog_date  # Use the provided date or the default date
        }
        blogs.append(blog)

        # Create a unique HTML filename based on the title
        html_filename = f"{len(blogs)}_{blog_title.replace(' ', '_')}.html"
        html_path = os.path.join(blog_folder, html_filename)

        # Generate the HTML content and save it to the file
        rendered_html = render_template('blog_template.html', blog_title=blog_title, author_name=author_name, blog_content=blog_content, date=blog_date)
        with open(html_path, 'w') as html_file:
            html_file.write(rendered_html)

        # Redirect to the view blog page for the newly created blog
        return redirect(url_for('blog', filename=html_filename))

    return render_template('create_blog.html')

@app.route('/blog/<filename>')
def blog(filename):
    file_path = os.path.join(blog_folder, filename)

    if os.path.exists(file_path):
        with open(file_path, 'r') as html_file:
            return html_file.read()
    else:
        return "Blog not found", 404

@app.route('/blogquest')
def blogquest():
    blog_entries = []

    # Iterate through files in the "blogs" folder
    for filename in os.listdir(blog_folder):
        if filename.endswith(".html"):
            file_path = os.path.join(blog_folder, filename)

            # Extract title and author from the HTML file
            with open(file_path, 'r') as html_file:
                html_content = html_file.read()
                title_start = html_content.find('<h1>') + len('<h1>')
                title_end = html_content.find('</h1>')
                author_start = html_content.find('<h2>') + len('<h2>')
                author_end = html_content.find('</h2>')

                if title_start != -1 and title_end != -1 and author_start != -1 and author_end != -1:
                    blog_title = html_content[title_start:title_end]
                    author_name = html_content[author_start:author_end]

                    # Extract the date from the blog content (assuming a specific format)
                    date_start = html_content.find('<div class="date">') + len('<div class="date">')
                    date_end = html_content.find('</div>', date_start)
                    if date_start != -1 and date_end != -1:
                        blog_date = html_content[date_start:date_end]
                    else:
                        # Use the default date if no date is found
                        blog_date = '01/01/2023'

                    # Generate the HTML structure for each blog entry
                    entry_html = f"""
                    <div class="zebra">
                        <img class="rating left" src="http://venith.net/TDKHome/TDKPaint/images/rating_e32.png" alt="E" />
                        <div class="blog_right">
                            <div style="background:#8f0; border:1px solid #8f0">6</div>
                            <img src="http://venith.net/TDKHome/TDKPaint/images/new.png" alt="New!" />
                        </div>
                        <a href="/blog/{filename}">{blog_title}</a><br />
                        In Gaming<br />
                        By <a href="/member?id=137730">{author_name}</a><br />
                    </div>
                    """

                    blog_entries.append(entry_html)

    return render_template('blogquest_template.html', blog_entries=blog_entries)

if __name__ == '__main__':
    app.run(debug=True, port=8162)
