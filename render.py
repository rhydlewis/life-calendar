import jinja2
import os


def html(cal):
    loader = jinja2.FileSystemLoader(searchpath=".")
    env = jinja2.Environment(loader=loader)
    template = env.get_template("template/index.html")
    result = template.render(dict(title="Life Calendar", years=cal.years(),
                                  headers=['Yr'] + range(1, 54)))

    path = os.path.join(os.getcwd(), "html/index.html")

    with open(path, 'w') as f:
        f.write(result.encode('utf-8'))
