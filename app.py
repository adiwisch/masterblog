from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts():
    with open('blog_posts.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
@app.route('/')
def index():
    with open('blog_posts.json', 'r', encoding='utf-8') as file:
        blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        blog_posts = load_blog_posts()
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_id = max((post['id'] for post in blog_posts), default=0) + 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)