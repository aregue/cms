from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user, logout_user, LoginManager

from app import app
from app import db
from app.models import User, Post, Upload, Site
from app.forms import LoginForm, EditForm, NewPostForm, DeleteForm, PublishForm, UnpublishForm, EditSettingsForm, UpdatePostForm, UpdateSettingsForm, PinForm, UnpinForm, DeleteFileForm, UploadForm
import datetime
import markdown
import os
from werkzeug.utils import secure_filename


# Log in and log out
# ------------------

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

    
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", error=False, form=form)
        
    user = load_user(request.form["username"])
    if user is None:
        return render_template("login.html", error=True, form=form)
    
    if not user.check_password(request.form["password"]):
        return render_template("login.html", error=True, form=form)
        
    login_user(user)
    return redirect(url_for('overview'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



## Public site 
## -----------

@app.route('/<post_url>')
@app.route('/')
def home(post_url=None):
    # get list of title and url of pages
    pages = Post.query.filter_by(pinned=True).filter_by(published=True).all()
    
    # get blog description and footer from Site configuration table
    description = Site.query.filter_by(name='desc').first()
    
    if not post_url:
        # Show home page. Get data from Site configuration table
        title_h1 = Site.query.filter_by(name='title').first()
        html = Site.query.filter_by(name='home_html').first()
        last_updated =Site.query.filter_by(name='updated_date').first()
        
        #get list of title and url of pages
        pages = Post.query.filter_by(pinned=True).filter_by(published=True).all()
        
        return render_template(
            'public/home.html', 
            title = 'Home',
            title_h1 = title_h1.value,
            description = description.value,
            html = markdown.markdown(html.value),
            last_updated = last_updated.value,
            pages = pages,
            )
        
    post = Post.query.filter_by(url=post_url).first()
    
    if post is None:
        return redirect(url_for('home'))
        
    elif not post.published:
        return redirect(url_for('home'))
        
    else:
        return render_template(
            'public/post.html', 
            title = post.title, 
            description = description.value,
            html = markdown.markdown(post.content),
            last_updated = post.date_updated,
            pages = pages,
            post_url = post_url,
            )
    
    
    
@app.route('/blog')
def blog():
    description = Site.query.filter_by(name='desc').first()
    
    pages = Post.query.filter_by(
            pinned=True
        ).filter_by(
            published=True
        ).all()
        
    posts = Post.query.filter_by(
            pinned=False
        ).filter_by(
            published=True
        ).order_by(
            Post.date_published.desc()
        ).order_by(
            Post.id.desc()
        ).all()
        
    
    return render_template(
        'public/blog.html', 
        title='Blog',
        description=description.value,
        posts = posts,
        pages = pages,
        )
    
    

## Site settings
## -------------

@app.route('/edit_settings')
@login_required
def edit_settings():
    form = EditSettingsForm()
    
    description = Site.query.filter_by(name='draft_desc').first()
    title_site = Site.query.filter_by(name='draft_title').first()
    home_html = Site.query.filter_by(name='draft_home_html').first()
    
    form.description.data = description.value
    form.title.data = title_site.value
    form.content.data = home_html.value
    
    return render_template(
        'private/edit_settings.html',
        title = 'Edit settings',
        form = form,
        )
        
        
        
@app.route('/preview_settings')
@login_required
def preview_settings():
    
    description = Site.query.filter_by(name='draft_desc').first()
    pages = Post.query.filter_by(pinned=True).all()
    title_site = Site.query.filter_by(name='draft_title').first()
    home_html = Site.query.filter_by(name='draft_home_html').first()
    
    current_description = Site.query.filter_by(name='desc').first()
    current_title_site = Site.query.filter_by(name='title').first()
    current_home_html = Site.query.filter_by(name='home_html').first()
    
    draft_updated = (current_description.value != description.value) or \
        (current_title_site.value != title_site.value) or \
        (current_home_html.value != home_html.value)
            
    form_update = UpdateSettingsForm()
            
    html = '<h1>' + title_site.value + '</h1>'
    html = html + markdown.markdown(home_html.value)
    
                
    return render_template(
        'private/preview_settings.html',
        title='Preview',
        html = html,
        form_update = form_update,
        pages = pages,
        description = description.value,
        last_updated = datetime.date.today(),
        draft_updated = draft_updated,
        )
                
    

@app.route('/uploads_home')
@login_required
def uploads_home():
    '''Displays uploads form and a list of uploaded files'''
    
    #add WTForm for file upload
    form_upload = UploadForm()
    form_upload.post_id.data = 'home'
    
    # get list of already uploaded files
    files = os.listdir('app/static/files/home')
    forms = []
    for f in files:
        form = DeleteForm()
        form.object_id.data = f
        forms.append(form)
    
    return render_template(
        'private/uploads_home.html',
        files = zip(files,forms),
        title = 'Uploads for home page',
        form_upload = form_upload,
        )



## Post management
## ---------------

@app.route('/overview')
@login_required
def overview():
    form = NewPostForm()
    pages = Post.query.filter_by(pinned=True)
    posts = Post.query.filter_by(pinned=False).order_by(Post.id.desc()) 
        
    return render_template(
        'private/overview.html', 
        title='Overview',
        form=form,
        pages=pages,
        posts=posts,
        )


@app.route('/edit')
@login_required
def edit():
    if 'post' in request.args:
        post_id = request.args.get('post')
        post = Post.query.filter_by(id=post_id).first()
        
        if post != None:
    
            form = EditForm()
            form.post_id.data = post.id
            form.title.data = post.draft_title
            form.content.data = post.draft_content
    
            return render_template(
                'private/edit.html', 
                title='Edit', 
                form=form,
                post_id = post.id,
                )
                
    return redirect(url_for('overview'))



@app.route('/preview')
@login_required
def preview():
    if 'post' in request.args:
        post_id = request.args.get('post')
        post = Post.query.filter_by(id=post_id).first()
        
        if post != None:
            description = Site.query.filter_by(name='desc').first()
            pages = Post.query.filter_by(pinned=True).all()
            
            form_pin = PinForm()
            form_pin.post_id.data = post.id
            
            form_unpin = UnpinForm()
            form_unpin.post_id.data = post.id
            
            form_publish = PublishForm()
            form_publish.post_id.data = post.id
            
            form_unpublish = UnpublishForm()
            form_unpublish.post_id.data = post.id
            
            form_update = UpdatePostForm()
            form_update.post_id.data = post.id
            
            form_delete = DeleteForm()
            form_delete.object_id.data = post.id
            
            html = markdown.markdown(post.draft_content) 
            
            draft_updated = (post.draft_title != post.title) or (post.draft_content != post.content)
                
            return render_template(
                'private/preview.html',
                title='Preview',
                post = post,
                html = html,
                form_pin = form_pin,
                form_unpin = form_unpin,
                form_publish = form_publish,
                form_unpublish = form_unpublish,
                form_update = form_update,
                form_delete = form_delete,
                pages = pages,
                description = description.value,
                last_updated = datetime.date.today(),
                draft_updated = draft_updated,
                )
                
    return redirect(url_for('overview'))
       
    
    
@app.route('/uploads')
@login_required
def uploads():
    '''Displays uploads form and a list of uploaded files'''
    
    if 'post' in request.args:
        post_id = request.args.get('post')
    
        #add WTForm for file upload
        form_upload = UploadForm()
        form_upload.post_id.data = post_id
        
        # get list of already uploaded files
        directory = os.path.join('app/static/files', str(int(post_id)))
        
        if os.path.isdir (directory):
            files = os.listdir(directory)
            forms = []
            for f in files:
                form = DeleteFileForm()
                form.object_id.data = f
                form.post_id.data = post_id
                forms.append(form)
        else:
            files = []
            forms = []
    
        return render_template(
            'private/uploads.html',
            files = zip(files,forms),
            title = 'Uploads',
            post_id = post_id,
            form_upload = form_upload,
            )
    
    return redirect(url_for('overview'))



## Actions - Site settings
## -----------------------

@app.route('/save_settings', methods=["POST"]) 
@login_required
def save_settings():
    '''Saves new settings as draft. Visible site is not updated.'''
    form = EditSettingsForm()
    if form.validate_on_submit():
        description = Site.query.filter_by(name='draft_desc').first()
        title_site = Site.query.filter_by(name='draft_title').first()
        home_html = Site.query.filter_by(name='draft_home_html').first()
        
        
        description.value = form.description.data
        title_site.value = form.title.data
        home_html.value = form.content.data
            
        db.session.commit()
        
    return redirect(url_for('edit_settings'))
    


@app.route('/update_settings', methods=["POST"]) 
@login_required
def update_settings():
    '''Updates site with last saved draft settings.'''
    form = UpdateSettingsForm()
    if form.validate_on_submit():
        description = Site.query.filter_by(name='desc').first()
        title_site = Site.query.filter_by(name='title').first()
        home_html = Site.query.filter_by(name='home_html').first()
        
        
        draft_description = Site.query.filter_by(name='draft_desc').first()
        draft_title_site = Site.query.filter_by(name='draft_title').first()
        draft_home_html = Site.query.filter_by(name='draft_home_html').first()
        
        last_updated = Site.query.filter_by(name='updated_date').first()
        
        description.value = draft_description.value
        title_site.value = draft_title_site.value
        home_html.value = draft_home_html.value
        
        last_updated.value = datetime.date.today()
            
        db.session.commit()
        
    return redirect(url_for('overview'))



@app.route('/save_upload_home', methods=["POST"]) 
@login_required
def save_upload_home():
    '''Saves a file upload in the directory for the home page'''
    form = UploadForm()
    if form.validate_on_submit():
        #TODO: define uploads directory in a config variable
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('app/static/files/home', secure_filename(uploaded_file.filename)))
    return redirect(url_for('uploads_home'))



@app.route('/delete_file_home', methods=["POST"])
@login_required
def delete_file_home():
    '''Deletes a file attached to the home page'''
    form = DeleteForm() # the value of object_id in the form is the filename
    if form.validate_on_submit():
        os.remove(os.path.join('app/static/files/home', secure_filename(form.object_id.data)))
    return redirect(url_for('uploads_home'))




## Actions - Post management
## -------------------------


def make_url(title):
    '''Converts a title into a string suitable for beeing used as url'''
    
    # replace spaces with '-', make lowercase and remove non ascii characters
    # and punctuation. Leave only lowercase ascii and numbers.
    words = title.split()
    url = '-'.join(words)
    url = url.lower()
    #TODO: remove exclamation signs (!) and other things that won't be recognized
    
    # check that url is not an existing route
    if url in [blog, edit, preview, overview] :
        url = url + '-i'
    
    #TODO: check that url does not exist already in another post
    unique = True
    
    #call make_url recursively with the proposal for the new  
    #url to avoid conflict with another also existing url
    if not unique:
        url = make_url (url+'-i')
    
    return url
    
 
    
@app.route('/new_page', methods=["POST"]) 
@login_required
def new_page():
    '''Creates a new page. A page is a normal post accessible from the 
    home page via a link in the navigation bar (it is 'pinned' to the
    home page). It does not show in the list of post under blog.'''
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post (
            draft_title = form.title.data, 
            pinned = True, 
            published = False,
            )
        db.session.add(new_post)
        # flush session to get id of new invoice to use in line data
        db.session.flush()
        db.session.commit()
        return redirect(url_for('edit', post=new_post.id))
    return redirect(url_for('overview'))


@app.route('/new_post', methods=["POST"]) 
@login_required
def new_post():
    '''Creates a new post.'''
    form = NewPostForm()
    if form.validate_on_submit():
        new_post = Post (
            draft_title = form.title.data,
            pinned = False, 
            published = False,
            )
        db.session.add(new_post)
        # flush session to get id of new invoice to use in line data
        db.session.flush()
        db.session.commit()
        return redirect(url_for('edit', post=new_post.id))
    return redirect(url_for('overview'))


@app.route('/save', methods=["POST"]) 
@login_required
def save():
    '''Saves changes to post/page as draft'''
    form = EditForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        post.draft_title = form.title.data
        post.draft_content = form.content.data
                   
        db.session.commit()
        
        return redirect(url_for('edit', post=post.id))
    return redirect(url_for('overview'))
    
    
@app.route('/publish', methods=["POST"])
@login_required
def publish():
    '''Publishes a post/page. Makes it publicly accessible'''
    form = PublishForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        post.title = post.draft_title
        post.content = post.draft_content
        post.published = True
        
        # if the post is published for the first time, set published date and last updated date
        # if the post has been publisehd, unpublished and publisehd anew, set only last updated date
        # post url needs to be generated only if post has not been published before
        if not post.date_published:
            post.date_published = datetime.date.today()
            post.url = make_url(post.title)
        post.date_updated = datetime.date.today()
        
        db.session.commit()
    return redirect(url_for('preview', post=post.id))
    
    
@app.route('/update', methods=["POST"])
@login_required
def update():
    '''Updates an already published post/page'''
    form = UpdatePostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        
        post.title = post.draft_title
        post.content = post.draft_content
        
        # update last updated date
        post.date_updated = datetime.date.today()
        
        db.session.commit()
    return redirect(url_for('preview', post=post.id))


@app.route('/unpublish', methods=["POST"])
@login_required
def unpublish():
    '''Sets status for post/page back to draft. It is no longer publicly accessible'''
    form = UnpublishForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        post.published = False
        db.session.commit()
    return redirect(url_for('preview', post=post.id))



@app.route('/pin', methods=["POST"])
@login_required
def pin():
    '''Pin post to home page'''
    form = PinForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        post.pinned = True
        db.session.commit()
    return redirect(url_for('preview', post=post.id))
    
    

@app.route('/unpin', methods=["POST"])
@login_required
def unpin():
    '''Remove post from home page'''
    form = UnpinForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.post_id.data).first()
        post.pinned = False
        db.session.commit()
    return redirect(url_for('preview', post=post.id))


    
@app.route('/delete_post', methods=["POST"]) 
@login_required
def delete_post():
    '''Deletes a post/page and associated files. Cannot be undone'''
    form = DeleteForm()
    if form.validate_on_submit():
        post_id = form.object_id.data
                
        # Delete post
        post= Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        
        # Delete files belonging to post
        
        # get list of uploaded files (if any)
        directory = os.path.join('app/static/files', str(int(post_id)))
        
        if os.path.isdir (directory):
            files = os.listdir(directory)
            
            for f in files:
                # remove file from directory
                os.remove(os.path.join('app/static/files', str(int(post_id)), f))
            
            # remove file record from the database
            if len(files)>0:
                upload_records = Upload.query.filter_by(post_id=post_id).delete()
        
        db.session.commit()
        
    return redirect(url_for('overview'))



@app.route('/save_upload', methods=["POST"]) 
@login_required
def save_upload():
    '''Saves a file upload in the directory for the post to which it is attached'''
    #TODO: define uploads directory in a config variable
    
    form = UploadForm()
    if form.validate_on_submit():
        post_id = form.post_id.data
    
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # check if directory for post exists and create if it doesn't
            directory = os.path.join('app/static/files', str(int(post_id)))
            
            if not os.path.isdir(directory):
                os.mkdir(directory)
    
            # save file to directory for post
            uploaded_file.save(
                os.path.join(directory,
                secure_filename(uploaded_file.filename)),
                )
            
            # keep a record of the uploaded file in the database
            upload_record = Upload(post_id=post_id, filename=secure_filename(uploaded_file.filename))
            db.session.add(upload_record)
            db.session.commit()
        
        return redirect(url_for('uploads', post=post_id))
    return redirect(url_for('overview'))



@app.route('/delete_file', methods=["POST"])
@login_required
def delete_file():
    '''Deletes a file attached to a post'''

    form = DeleteFileForm() # the value of object_id in the form is the filename
    if form.validate_on_submit():
        post_id = form.post_id.data
        filename = secure_filename(form.object_id.data)
        
        # remove file from directory
        os.remove(os.path.join('app/static/files', str(int(post_id)), filename))
            
        # remove file record from the database
        upload_record = Upload.query.filter_by(post_id=post_id).filter_by(filename=filename).first()
        db.session.delete(upload_record)
        db.session.commit()
        
    return redirect(url_for('uploads', post=post_id))


















    
    
