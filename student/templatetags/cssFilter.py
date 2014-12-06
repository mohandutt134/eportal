from django import template
register = template.Library()
 
@register.filter(name='add_attributes')
def add_attributes(field, css):
    attrs = {}
    definition = css.split(',')
 
    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v
 
    return field.as_widget(attrs=attrs)


@register.filter(name='get_nic')
def get_nic(fullname):
	words = fullname.split()
	if len(words) > 1:
		nic = ""
		for word in words:
			word = word.upper()
			if not word in ['AND','&']:
				nic = nic + word[0]
		return nic
	else:
		return fullname