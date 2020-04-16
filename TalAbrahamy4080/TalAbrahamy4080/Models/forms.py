from flask_wtf import FlaskForm

class ExpandForm(FlaskForm):
	submit1 = SubmitField('Expand')
	name="Expand"
	value="Expand"
 
class CollapseForm(FlaskForm):
	submit2 = SubmitField('Collapse')
	name="Collapse"
	value="Collapse"