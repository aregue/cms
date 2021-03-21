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

Change directory into cms and install dependencies 

    $ cd cms
    $ pip install -r requirements.txt

Create folder for uploads and make it writable by the web server

    $ mkdir app/static/files
    $ chgrp web app/static/files
    $ chmod g+w app/static/files

If you choose to place the uploads folder in another location or give it another name, make sure to update the `UPLOADS_FOLDER` variable in `app/config.py` with your folder name. 

Setup blog database and user. It will also create a .env file with a random SECRET_KEY used in the app.

    $ python setup_blog.py

I run CMS with Gunicorn behind a reverse proxy. CMS is a Flask app. Although Gunicorn is included in the dependencies, CMS can be run with many different servers. The script `run-blog.sh` is provided for convenience. It is just one line to start the Gunicorn server. On my hosting provider, you can add a daemon that runs this script, a proxy that listens to the port specified on the script (8000) and you are done. 

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

Se under folder licenses to read the full licenses.



