"""Flask blog application with storage in JSON file"""

import json
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = "andres_temporary_secret_key"

def load_blog_posts():
    """Load all blog posts from the JSON file."""
    with open('blog_posts.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def save_blog_posts(posts):
    """Save all blog posts to the JSON file."""
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)

def get_post_by_id(post_id):
    """Return a blog post by its ID - None if no post was found with that ID."""
    blog_posts = load_blog_posts()

    return next(
        (post for post in blog_posts if post['id'] == post_id),
        None
    )

@app.route('/')
def index():
    """Display all blog posts."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Create a new blog post or display the form to do so."""
    if request.method == 'POST':
        # Load all blog posts
        blog_posts = load_blog_posts()
        # get values from form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # get new ID
        new_id = max((post['id'] for post in blog_posts), default=0) + 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
        }

        # add new post to existing ones
        blog_posts.append(new_post)
        # save posts
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('post_form.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by ID and redirect to the index. Display success and error messages"""
    # Load all blog posts
    blog_posts = load_blog_posts()
    # look for post with specified ID
    post_to_delete = next(
        (post for post in blog_posts if post['id'] == post_id),
        None
    )

    if post_to_delete is None:
        # no post found: show error message
        flash(f'Error 404: Blog post with ID {post_id} was not found.', 'error')
    else:
        # post found: remove post from all posts
        blog_posts.remove(post_to_delete)
        # save posts
        save_blog_posts(blog_posts)
        # show success message
        flash(f'Blog post "{post_to_delete["title"]}" was deleted successfully.', 'success')

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post or display the form to do so."""
    # Get the blog post
    post = get_post_by_id(post_id)

    # return error if none found
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Load all blog posts
        blog_posts = load_blog_posts()

        # Get updated form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Update the selected post
        for blog_post in blog_posts:
            if blog_post['id'] == post_id:
                blog_post['author'] = author
                blog_post['title'] = title
                blog_post['content'] = content
                break

        # Save the updated posts
        save_blog_posts(blog_posts)

        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('index'))

    # GET request: display the pre-filled form
    return render_template('post_form.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """Increment the like count of a blog post."""
    # load all blog posts
    blog_posts = load_blog_posts()

    for post in blog_posts:
        # find post with ID
        if post['id'] == post_id:
            # increment 'likes' count by 1
            post['likes'] = post.get('likes', 0) + 1
            # save posts
            save_blog_posts(blog_posts)
            break

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
