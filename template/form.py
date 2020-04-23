#coding: utf8
from collections import OrderedDict as oDict
from datetime import datetime, date


class Form(object):
    
    def __init__(self, action='', model=None, method="GET", _id="", multipart=False, remote=False, charset="UTF8", html=None):
        self.action = action
        self.model = model
        self.method = method
        self.multipart = multipart
        self.remote = remote
        self.charset = (charset or "UTF8").upper()
        self.id = _id
        self.html = html or {}

    def begin_render(self):
        d = oDict()
        if self.id: d['id'] = self.id
        d['action'] = self.action
        d['method'] = self.method
        d['accept-charset'] = self.charset
        if self.method.upper() == 'POST' and self.multipart:
            d['enctype'] = "multipart/form-data"

        d.update(self.html)
        return '<form %s>' % ' '.join([ '%s="%s"' % (k, v) for k, v in d.items() ]) 

    def end_render(self):
        return '</form>'

    def button(self, value=None, name="button", tp="submit", disabled=False, html=None):
        html = html or {}
        d = oDict()
        d['name'] = name or "button"
        d['type'] = tp or 'submit'
        if disabled: d['disabled'] = 'disabled'

        d.update(html)
        return '<button %s>%s</button>' % \
                    (' '.join([ '%s="%s"' % (k, v) for k, v in d.items() ]), 
                        value or "Button"
                    )

    def text(self, name, value=None, _id='', tp='text', placeholder='', size='', maxlength='', disabled=False, _class='', html=None, autoid=True):
        html = html or {}
        d = oDict()
        if _id:
            d['id'] = _id
        elif autoid:
            d['id'] = name
        d['name'] = name
        d['type'] = tp or 'text'
        if value or value == '':
            d['value'] = value
        if placeholder:
            d['placeholder'] = placeholder
        if size or size == 0:
            d['size'] = size
        if maxlength or maxlength == 0:
            d['maxlength'] = maxlength

        if disabled:
            d['disabled'] = "disabled"
        if _class:
            d['class'] = _class
        d.update(html)

        return '<input %s />' % ' '.join([ '%s="%s"' % (k, v) for k, v in d.items() ])

    def password(self, name, value=None, _id='', placeholder='', size='', maxlength='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="password", size=size, maxlength=maxlength, disabled=disabled, _class=_class, html=html)

    def tel(self, name, value=None, _id='', placeholder='', size='', maxlength='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="tel", size=size, maxlength=maxlength, disabled=disabled, _class=_class, html=html)

    def search(self, name, value=None, _id='', placeholder='', size='', maxlength='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="search", size=size, maxlength=maxlength, disabled=disabled, _class=_class, html=html)

    def email(self, name, value=None, _id='', placeholder='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="email", disabled=disabled, _class=_class, html=html)

    def color(self, name, value=None, _id='', placeholder='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="color", disabled=disabled, _class=_class, html=html)

    def url(self, name, value=None, _id='', placeholder='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="url", disabled=disabled, _class=_class, html=html)

    def file(self, name, value=None, _id='', placeholder='', accept=None, multiple=False, disabled=False, _class='', html=None):
        html = html or {}
        if accept and 'accept' not in html:
            html['accept'] = accept
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="file", disabled=disabled, _class=_class, html=html)

    def hidden(self, name, value=None, _id='', tp='text', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, tp="hidden", disabled=disabled, _class=_class, html=html)

    def label(self, name, value='Name', _class='', html=None):
        html = html or {}
        d = oDict()
        d['for'] = name
        if _class:
            d['class'] = _class
        d.update(html)
        return '<label %s>%s</label>' % (
                    ' '.join([ '%s="%s"' % (k, v) for k, v in d.items() ]),
                    value
                )

    def number(self, name, value=None, _id='', placeholder='', tp='', _min='', _max='', step='', disabled=False, _class='', html=None):
        html = html or {}
        tp = tp or 'number'
        if _min and 'min' not in html: html['min'] = _min
        if _max and 'max' not in html: html['max'] = _max
        if step and 'step' not in html: html['step'] = step
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp=tp, disabled=disabled, _class=_class, html=html)

    def month(self, name, value=None, _id='', placeholder='', _min='', _max='', step='', disabled=False, _class='', html=None):
        return self.number(name=name, value=value, _id=_id, placeholder=placeholder, _min=_min, _max=_max, step=step, tp="month", disabled=disabled, _class=_class, html=html)

    def week(self, name, value=None, _id='', placeholder='', _min='', _max='', step='', disabled=False, _class='', html=None):
        return self.number(name=name, value=value, _id=_id, placeholder=placeholder, _min=_min, _max=_max, step=step, tp="week", disabled=disabled, _class=_class, html=html)

    def date(self, name, value=None, _id='', placeholder='', disabled=False, _class='', html=None):
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="date", disabled=disabled, _class=_class, html=html)

    def time(self, name, value=None, _id='', placeholder='', _min='', _max='', step='', disabled=False, _class='', html=None):
        return self.number(name=name, value=value, _id=_id, placeholder=placeholder, _min=_min, _max=_max, step=step, tp="time", disabled=disabled, _class=_class, html=html)

    def datetime(self, name, value=None, placeholder='', _min='', _max='', _id='', step='', disabled=False, _class='', html=None):
        def _(v):
            if isinstance(v, datetime):
                return datetime.strftime(v, '%Y-%m-%dT%H:%M:%S')
            elif isinstance(v, date):
                return date.strftime(v, '%Y-%m-%dT00:00:00')

        html = html or {}
        if value: value = _(value)
        if _min and 'min' not in html: html['min'] = _(_min)
        if _max and 'max' not in html: html['max'] = _(_max)
        if step and 'step' not in html: html['step'] = step
        return self.text(name=name, value=value, _id=_id, placeholder=placeholder, tp="datetime-local", disabled=disabled, _class=_class, html=html)

    def radio(self, name, value, _id='', checked=False, disabled=False, _class='', html=None):
        html = html or {}
        if not _id:
            _id = '%s_%s' % (name, value.replace(' ', '_'))

        if disabled:
            html['disabled'] = 'disabled'
        elif checked is True and 'checked' not in html:
            html['checked'] = 'checked'

        return self.text(name=name, value=value, _id=_id, tp="radio", disabled=disabled, _class=_class, html=html)

    def checkbox(self, name="checkbox", value="1", _id="", checked=False, disabled=False, _class='', html=None):
        html = html or {}
        d = oDict()
        name = name or "checkbox"
        if checked is True and 'checked' not in html: 
            d['checked'] = "checked"
        d.update(html)
        return self.text(name=name, value=value, _id=_id, tp="checkbox", disabled=disabled, _class=_class, html=d)

    def range(self, name, value=None, _id='', _in=None, step='', disabled=False, _class='', html=None):
        html = html or {}
        if _in and len(_in) >= 2:
            if 'min' not in html: html['min'] = _in[0]
            if 'max' not in html: html['max'] = _in[1]
        if step and 'step' not in html: html['step'] = step
        return self.text(name=name, value=value, _id=_id, tp="range", disabled=disabled, _class=_class, html=html)

    def submit(self, value='Save changes', disabled=False, _class='', html=None):
        html = html or {}
        if 'data-disable-with' not in html:
            html['data-disable-with'] = value
        return self.text(name='commit', value=value, tp="submit", disabled=disabled, _class=_class, html=html, autoid=False)

    def textarea(self, name, value=None, _id='', placeholder='', size=None, rows=None, cols=None, escape=True, disabled=False, _class='', html=None):
        html = html or {}
        d = oDict()
        d['id'] = _id or name
        d['name'] = name
        if placeholder:
            d['placeholder'] = placeholder
        if size or size == 0:
            d['size'] = size
        if rows or rows == 0:
            d['rows'] = rows
        if cols or cols == 0:
            d['cols'] = cols
        if disabled:
            d['disabled'] = "disabled"
        if _class:
            d['class'] = _class
        d.update(html)

        return '<textarea %s>%s</textarea>' % (
                    ' '.join([ '%s="%s"' % (k, v) for k, v in d.items() ]),
                    value or ''
                )