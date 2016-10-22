# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask.ext.script import server, Server
from app import app
from app.models import Post

server = server(app)
server.add_command("runserver", 
        Server(host="127.0.0.1", port=5000, use_debugger=True))

@server.command
def save_post():
    post = Post(author="Andrew liu", 
        title="Hello World",
        tags="test",
        content="This is the First Post")
    post.save()

if __name__ == '__main__':
    server.run()
