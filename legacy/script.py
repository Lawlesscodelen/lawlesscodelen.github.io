from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from json import load

# Specify how you are going to load the file
template_env = Environment(loader=FileSystemLoader(searchpath='./env'))

with open('config.json', encoding="utf-8") as config_file:
    config = load(config_file)

######## INDEX
# tipo: portada, output:index
template = template_env.get_template('portada.html')

with open('index.html', 'w', encoding="utf-8") as output_file:
    output_file.write(
        template.render(
            config=config,
            page_name='index',
        )
    )

######## ARTICULOS
# tipo: lista, output:artículos
template = template_env.get_template('lista.html')

with open('articulos.html', 'w', encoding="utf-8") as output_file:
    output_file.write(
        template.render(
            config=config,
            page_name='articulos',
            items=config['articulos']
        )
    )

######## LIBROS
# tipo: lista, output:artículos
template = template_env.get_template('lista.html')

with open('libros.html', 'w', encoding="utf-8") as output_file:
    output_file.write(
        template.render(
            config=config,
            page_name='libros',
            items=config['libros']
        )
    )

######## VIDEOS
# tipo: lista, output:artículos
template = template_env.get_template('lista.html')

with open('videos.html', 'w', encoding="utf-8") as output_file:
    output_file.write(
        template.render(
            config=config,
            page_name='videos',
            items=config['videos']
        )
    )


######## SOBREMI
# tipo: cuadro, output:sobremi
template = template_env.get_template('cuadro.html')

with open('sobremi.html', 'w', encoding="utf-8") as output_file:
    output_file.write(
        template.render(
            config=config,
            page_name='sobremi',
        )
    )