import os
import jinja2
import requests
template_loader = jinja2.Template("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename,**context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to,subject,body,html=render_template("email.html",username="teste@gmail.com")):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api",os.getenv("MAILGUN_API_KEY")),
        data={
            "from":"YOUR MAIL FROM THE MAILGUN",
            "to":[to],
            "subject":subject,
            "text":body,
            "html":html
        }
    )
