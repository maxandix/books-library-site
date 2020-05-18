from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from more_itertools import chunked
import os
from os.path import join

PAGES_DIR = 'pages'


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open("media/books_info.json", "r") as my_file:
        books_info = json.loads(my_file.read())

    template = env.get_template('template.html')
    for index, books_info_chunk in enumerate(chunked(books_info, 10)):
        rendered_page = template.render(chunks=chunked(books_info_chunk, 2))
        with open(join(PAGES_DIR, f'index{index}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs(PAGES_DIR, exist_ok=True)

    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
