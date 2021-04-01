# CMS readme

Content management system (CMS) for a self hosted blog. MIT license.

Inspired by [Bear Blog](https://bearblog.dev). Main differences:

 - CMS is meant to be self hosted
 - Allows file uploads
 - Ads post/page preview
 - Publish/unpublish post/page from preview tab
 - Update post from preview tab (edits are not visible if post/page is not explicitly updated or published)
 - Delete post/page from preview tab
 - Convert a post into a page and vice versa from preview tab
 - No tag functionality
 - No canonical url. Url is generated automatically from title when post/page is published
 - No analytics. You need to connect to your preferred analytics provider by adding code to the `base_public.html` template
 
## Install

Clone repository

    $ git clone https://github.com/aregue/cms.git

Change directory into cms, create virtual environment and install dependencies 

    $ cd cms
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Create folder for uploads and make it writable by the web server

    $ mkdir app/static/files
    $ chgrp web app/static/files
    $ chmod g+w app/static/files

Setup blog database and user by running `setup_blog.py` script. It will also create a .env file with a random SECRET_KEY used in the app.

    $ python setup_blog.py
    
The database will be created in `./database/content.db`. Make sure that the `database/` folder and the `content.db` file are writeable by the web server. 
    
    $ chgrp web database/
    $ chmod g+w database/
    $ chgrp web content.db
    $ chmod g+w content.db

CMS is a Flask app. It can be run with many different servers, such as [Gunicorn](https://www.gunicorn.org) or [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/index.html). Install any of them with pip. The script `run-blog.sh` is provided for convenience. It is just one line to activate the virtual environment and another to start the server. It comes with examples for both Gunicorn and Waitress. Edit the file to suit your needs. On my hosting provider, you can add a daemon that runs this script, a proxy that listens to the port specified on the script (8000) and you are done. 

CMS uses SQLite and therefore cannot run on Heroku and similar services with an ephemeral filesystem.

For more information on how to deploy Flask apps on Linux servers, I recommend [this post](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux) by Miguel Grinberg.

## HOWTOs

### How do I log in?

Once you have installed CMS, go to the url where you are serving your blog from and append `/login` on the navigation bar of your browser. Login with the username and password that you have just created.

### How do I reset my password?
If you forget your username or password, run the script `change_password.py` it will output the name of the blog user and will prompt you to enter a new password. For security only a hash of your password is stored in the database.

### What is the difference between pages and posts?

The only difference between pages and posts is that pages are always accessible from the top navigation bar. Posts can be converted into pages (pinned to the homepage) and pages into regular posts (removed from homepage).

### How do file uploads work?

Uploaded files are tied to specific posts. If a post is deleted, associated files will be deleted too. If you want to keep them, unpublish the post instead of deleting it. The post won't be publicly visible, but the files will still be accessible.

Files are accessible the moment they are uploaded, even if they are uploaded to a post that is not published yet. To make files unavailable, you have to delete them.

The system assumes that there is only one user of the blog and therefore does not put any restrictions on the kind of content that can be uploaded. You can crash your own server by doing stupid things and CMS will not try to prevent it.

### How do I link to a document/image that I have just uploaded? 

Link to a document by copying the url displayed on the list of uploaded files and creating a link in Markdown in the edit view like so: `[link text](link url)`. For images use `![Alt image text](image url)`.

## License

CMS is copyright 2021 Andreu Regué Barrufet and licensed under MIT.

CMS includes Dropzone which is also licensed under MIT. Dropzone is copyright 2012 Matias Meno. 

CMS uses Barlow font by Jeremy Tribby licensed under [SIL Open Font License v1.1](https://scripts.sil.org/ofl).

Se under folder licenses to read the full licenses.



