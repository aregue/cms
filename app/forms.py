from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm (FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    

class EditForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    submit = SubmitField('Save changes')
    
class EditSettingsForm (FlaskForm):
    description = StringField('Site description', validators=[DataRequired()])
    title = StringField('Home page title', validators=[DataRequired()])
    content = TextAreaField('Home page content', validators=[DataRequired()])
    submit = SubmitField('Save changes')
    
    
class NewPostForm (FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('New')
   
    
class DeleteForm (FlaskForm):
    object_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('🗑 Delete')
    
    
class DeleteFileForm (FlaskForm):
    object_id = HiddenField(validators=[DataRequired()])
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('🗑 Delete')
    
    
class PublishForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Publish')


class UnpublishForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Unpublish')


class UpdatePostForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Update')
    
    
class UpdateSettingsForm (FlaskForm):
    submit = SubmitField('Update')
    

class PinForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Pin to homepage')
    
    
class UnpinForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Remove from homepage')
    
    
class UploadForm (FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    
    
