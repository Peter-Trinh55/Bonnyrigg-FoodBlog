from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL

class RecipeForm(FlaskForm):
    title = StringField("Recipe Title", validators=[DataRequired(), Length(max=120)])
    summary = StringField("Short Summary", validators=[Optional(), Length(max=240)])
    cuisine = StringField("Cuisine", validators=[Optional(), Length(max=50)])
    difficulty = SelectField("Difficulty",
        choices=[("", "Choose..."), ("Easy","Easy"), ("Medium","Medium"), ("Hard","Hard")],
        validators=[Optional()]
    )
    cook_time_mins = IntegerField("Cook Time (mins)", validators=[Optional(), NumberRange(min=1, max=999)])
    ingredients = TextAreaField("Ingredients (one per line)", validators=[DataRequired(), Length(min=10)])
    instructions = TextAreaField("Instructions (one step per line)", validators=[DataRequired(), Length(min=10)])
    video_url = StringField("Video URL (optional)", validators=[Optional(), URL(), Length(max=255)])
    tags = StringField("Tags (comma separated)", validators=[Optional(), Length(max=200)])
    picture = FileField("Recipe Image", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp"])])
    submit = SubmitField("Publish Recipe")

class CommentForm(FlaskForm):
    body = StringField("Add a comment", validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField("Post")
