import spyral
import types
import sys
import functools
import math
import string
import pygame
from bisect import bisect_right

class BaseWidget(spyral.AggregateSprite):
    """
    The BaseWidget is the simplest possible widget that all other widgets
    must subclass. It handles tracking its owning form and the styling that
    should be applied.
    """
    def __init__(self, form, name):
        self.__style__ = form.__class__.__name__ + '.' + name
        self.form = form
        spyral.AggregateSprite.__init__(self, form)

# Widget Implementations

class MultiStateWidget(BaseWidget):
    """
    The MultiStateWidget is an abstract widget with multiple states. It is can
    be subclassed and implemented to have different behavior based on its
    states.
    
    In addition, it supports having a Nine Slice image; it will cut a given
    image into a 3x3 grid of images that can be stretched into a button. This
    is a boolean property.
    
    *states* should be a list of the possible states that the widget can be in.
    """
    def __init__(self, form, name, states):
        self._states = states
        self._state = self._states[0]
        
        BaseWidget.__init__(self, form, name)
                
        self._images = {}
        self._content_size = (0, 0)
        
    def _render_images(self):
        """
        Recreates the cached images of this widget (based on the 
        **self._image_locations** internal variabel) and sets the widget's image
        based on its current state.
        """
        for state in self._states:
            if self._nine_slice:
                size = self._padding + self._content_size
                nine_slice_image = spyral.Image(self._image_locations[state])
                self._images[state] = spyral.Image.render_nine_slice(nine_slice_image, size)
            else:
                self._images[state] = spyral.Image(self._image_locations[state])
        self.image = self._images[self._state]
        self._on_state_change()
    
    def _set_state(self, state):
        old_value = self.value
        self._state = state
        if self.value != old_value:
            e = spyral.Event(name="changed", widget=self, form=self.form, value=self._get_value())
            self.scene._queue_event("form.%(form_name)s.%(widget)s.changed" %
                                        {"form_name": self.form.__class__.__name__, 
                                         "widget": self.name}, 
                                    e)
        self.image = self._images[state]
        self._on_state_change()
        
    def _get_value(self):
        return self._state
        
    def _get_state(self):
        return self._state
        
    def _set_nine_slice(self, nine_slice):
        self._nine_slice = nine_slice
        self._render_images()
        
    def _get_nine_slice(self):
        return self._nine_slice
        
    def _set_padding(self, padding):
        if isinstance(padding, spyral.Vec2D):
            self._padding = padding
        else:
            self._padding = spyral.Vec2D(padding, padding)
        self._render_images()
        
    def _get_padding(self):
        """
        TODO: _get_padding documentation
        """
        return self._padding
        
    def _set_content_size(self, size):
        """
        TODO: _set_content_size documentation
        """
        self._content_size = size
        self._render_images()
        
    def _get_content_size(self):
        return self._get_content_size
        
    def _on_size_change(self):
        pass
    
    value = property(_get_value)
    padding = property(_get_padding, _set_padding)
    nine_slice = property(_get_nine_slice, _set_nine_slice)
    state = property(_get_state, _set_state)
    content_size = property(_get_content_size, _set_content_size)
    
    def __stylize__(self, properties):
        self._padding = properties.pop('padding', 4)
        self._nine_slice = properties.pop('nine_slice', False)
        self._image_locations = {}
        for state in self._states:
            # TODO: try/catch to ensure that the property is set?
            self._image_locations[state] = properties.pop('image_%s' % (state,))
        spyral.AggregateSprite.__stylize__(self, properties)


class ButtonWidget(MultiStateWidget):
    """
    A ButtonWidget is a simple button that can be pressed. It can have some
    text. If you don't specify an explicit width, then it will be sized
    according to it's text.
    """
    def __init__(self, form, name, text = "Okay"):
        MultiStateWidget.__init__(self, form, name, ['up', 'down', 'down_focused', 'down_hovered', 'up_focused', 'up_hovered'])
        
        self._text_sprite = spyral.Sprite(form)
        self.add_child(self._text_sprite)

        self.text = text
    
    def _get_value(self):
        if "up" in self._state:
            return "up"
        else:
            return "down"
        
    def _get_text(self):
        return self._text
    
    def _set_text(self, text):
        self._text = text
        self._text_sprite.image = self.font.render(self._text)
        self._content_size = self._text_sprite.image.get_size()
        self._render_images()
        
    def _on_state_change(self):
        self._text_sprite.pos = spyral.Vec2D(self._padding, self._padding) / 2
    
    value = property(_get_value)
    text = property(_get_text, _set_text)
    
    def handle_mouse_up(self, event):
        if self.state.startswith('down'):
            self.state = self.state.replace('down', 'up')
        
    def handle_mouse_down(self, event):
        if self.state.startswith('up'):
            self.state = self.state.replace('up', 'down')
        
    def handle_mouse_out(self, event):
        if "_hovered" in self.state:
            self.state = self.state.replace('_hovered', '')
        
    def handle_mouse_over(self, event):
        if not "_hovered" in self.state:
            self.state = self.state.replace('_focused', '') + "_hovered"
        
    def handle_mouse_motion(self, event):
        pass
        
    def handle_focus(self, event):
        if self.state in ('up', 'down'):
            self.state+= '_focused'
    
    def handle_blur(self, event):
        if self.state in ('up_focused', 'down_focused'):
            self.state = self.state.replace('_focused', '')
            
    def handle_key_down(self, event): pass
    def handle_key_up(self, event): pass
        
        
    def __stylize__(self, properties):
        self.font = spyral.Font(*properties.pop('font'))
        self._text = properties.pop('text', "Button")

        MultiStateWidget.__stylize__(self, properties)
    
        
class ToggleButtonWidget(ButtonWidget):
    """
    A ToggleButtonWidget is similar to a Button, except that it will stay down
    after it's been clicked, until it is clicked again.
    """
    def __init__(self, form, name, text = "Okay"):
        ButtonWidget.__init__(self, form, name, text)
        
    def handle_mouse_up(self, event):
        pass
        
    def handle_mouse_down(self, event):
        if self.state.startswith('down'):
            self.state = self.state.replace('down', 'up')
        elif self.state.startswith('up'):
            self.state = self.state.replace('up', 'down')
        

class CheckboxWidget(ToggleButtonWidget):
    """
    A CheckboxWidget is similar to a ToggleButtonWidget, only it doesn't have text.
    """
    def __init__(self, form, name):
        ToggleButtonWidget.__init__(self, form, name, "")

class RadioButtonWidget(ToggleButtonWidget):
    """
    A RadioButton is similar to a CheckBox, except it is to be placed into a
    RadioGroup, which will ensure that only one RadioButton in it's group is
    selected at a time.
    """
    def __init__(self, form, name, group):
        ToggleButtonWidget.__init__(self, form, name, _view_x)
        
class RadioGroupWidget(object):
    """
    Only one RadioButton in a RadioGroup can be selected at a time.
    """
    def __init__(self, buttons, selected = None):
        pass


class TextInputWidget(BaseWidget):            
    def __init__(self, form, name, width, value = '', default_value = True, text_length = None, validator = None):
        BaseWidget.__init__(self, form, name)
        view = form
    
        child_anchor = (self._padding, self._padding)
        self._cursor = spyral.Sprite(view)
        self._cursor.anchor = child_anchor
        self._text = spyral.Sprite(view)
        self._text.pos = child_anchor
        self.add_child(self._cursor)
        self.add_child(self._text)
        
        self._focused = False
        self._cursor.visible = False
        self._selection_pos = 0
        self._selecting = False
        self._shift_was_down = False
        self._mouse_is_down = False
        
        self._cursor_time = 0.
        self._cursor_blink_interval = self._cursor_blink_interval
        
        self.default_value = default_value
        self._default_value_permanant = default_value

        self._view_x = 0
        self.box_width = width - 2*self._padding
        self.text_length = text_length
        
        self._box_height = int(math.ceil(self.font.get_linesize()))

        self._cursor.image = spyral.Image(size=(2,self._box_height))
        self._cursor.image.fill(self._cursor_color)

        if validator is None:
            self.validator = string.printable
        else:
            self.validator = validator
        
        if text_length is not None and len(value) < text_length:
            value = value[:text_length]
        self._value = None
        self.value = value
        
        self._render_backs()
        self.image = self._image_plain
        
    def _render_backs(self):
        padding = self._padding
        width = self.box_width + 2 * padding
        self._image_plain = spyral.Image(self._image_locations['focused'])
        self._image_focused = spyral.Image(self._image_locations['unfocused'])
        if self._nine_slice:
            self._image_plain = spyral.Image.render_nine_slice(self._image_plain, (width, self._box_height + 2*padding))
            self._image_focused = spyral.Image.render_nine_slice(self._image_focused, (width, self._box_height + 2*padding))
        
    def __stylize__(self, properties):
        self._padding = properties.pop('padding', 4)
        self._nine_slice = properties.pop('nine_slice', False)
        self._image_locations = {}
        self._image_locations['focused'] = properties.pop('image_focused')
        self._image_locations['unfocused'] = properties.pop('image_unfocused')
        self._cursor_blink_interval = properties.pop('cursor_blink_interval', .5)
        self._cursor_color = properties.pop('cursor_color', (0, 0, 0))
        self._highlight_color = properties.pop('highlight_color', (0, 140, 255))
        self._highlight_background_color = properties.pop('highlight_background_color', (0, 140, 255))
        self.font = spyral.Font(*properties.pop('font'))

        spyral.AggregateSprite.__stylize__(self, properties)
            
    def _compute_letter_widths(self):
        self._letter_widths = []
        running_sum = 0
        for index in range(len(self._value)+1):
            running_sum= self.font.get_size(self._value[:index])[0]
            self._letter_widths.append(running_sum)
            
    def _insert_char(self, position, char):
        if position == len(self._value):
            self._value += char
            new_width= self.font.get_size(self._value)[0]
            self._letter_widths.append(new_width)
        else:
            self._value = self._value[:position] + char + self._value[position:]
            self._compute_letter_widths()
        self._render_text()
        e = spyral.Event(name="changed", widget=self, form=self.form, value=self._value)
        self.scene._queue_event("form.%(form_name)s.%(widget)s.changed" %
                                    {"form_name": self.form.__class__.__name__, 
                                     "widget": self.name}, 
                                e)
        
    def _remove_char(self, position, end = None):
        if end is None:
            end = position+1
        if position == len(self._value): 
            pass
        else:
            self._value = self._value[:position]+self._value[end:]
            self._compute_letter_widths()
        self._render_text()
        self._render_cursor()
        e = spyral.Event(name="changed", widget=self, form=self.form, value=self._value)
        self.scene._queue_event("form.%(form_name)s.%(widget)s.changed" %
                                    {"form_name": self.form.__class__.__name__, 
                                     "widget": self.name}, 
                                e)
                
            
    def _compute_cursor_pos(self, mouse_pos):
        x = mouse_pos[0] + self._view_x - self.x - self._padding
        index = bisect_right(self._letter_widths, x)
        if index >= len(self._value):
            return len(self._value)
        elif index:
            diff = self._letter_widths[index] - self._letter_widths[index-1]
            x -= self._letter_widths[index-1]
            if diff > x*2:
                return index-1
            else:
                return index
        else:
            return 0
            
    def _stop_blinking(self):
        self._cursor_time = 0
        self._cursor.visible = True
        
    def _get_value(self):
        return self._value
        
    def _set_value(self, value):
        if self._value is not None:
            e = spyral.Event(name="changed", widget=self, form=self.form, value=value)
            self.scene._queue_event("form.%(form_name)s.%(widget)s.changed" %
                                        {"form_name": self.form.__class__.__name__, 
                                         "widget": self.name}, 
                                    e)
        self._value = value
        self._compute_letter_widths()
        self._cursor_pos = 0#len(value)
        self._render_text()
        self._render_cursor()
    
    def _get_cursor_pos(self):
        return self._cursor_pos
    
    def _set_cursor_pos(self, position):
        self._cursor_pos = position
        self._move_rendered_text()
        self._render_cursor()
        
    def validate(self, char):
        valid_length = self.text_length is None or (self.text_length is not None and len(self._value) < self.text_length)
        valid_char = str(char) in self.validator
        return valid_length and valid_char
    
    def _set_nine_slice(self, nine_slice):
        self._nine_slice = nine_slice
        self._render_backs()
        
    def _get_nine_slice(self):
        return self._nine_slice
        
    def _set_padding(self, padding):
        self._padding = padding
        self._render_backs()
        
    def _get_padding(self):
        return self._padding

    value = property(_get_value, _set_value)
    cursor_pos = property(_get_cursor_pos, _set_cursor_pos)
    padding = property(_get_padding, _set_padding)
    nine_slice = property(_get_nine_slice, _set_nine_slice)
        
    def _render_text(self):
        if self._selecting and (self._cursor_pos != self._selection_pos):
            start, end = sorted((self._cursor_pos, self._selection_pos))
            
            pre = self.font.render(self._value[:start])
            highlight = self.font.render(self._value[start:end], color=self._highlight_color)
            post = self.font.render(self._value[end:])
            
            pre_missed = self.font.get_size(self._value[:end])[0] - pre.get_width() - highlight.get_width() + 1
            if self._value[:start]:
                post_missed = self.font.get_size(self._value)[0] - post.get_width() - pre.get_width() - highlight.get_width() - 1
                self._rendered_text = spyral.Image.from_sequence((pre, highlight, post), 'right', [pre_missed, post_missed])
            else:
                post_missed = self.font.get_size(self._value)[0] - post.get_width() - highlight.get_width()
                self._rendered_text = spyral.Image.from_sequence((highlight, post), 'right', [post_missed])

        else:
            self._rendered_text = self.font.render(self._value)
        self._move_rendered_text()
        
    def _move_rendered_text(self):
        width = self._letter_widths[self.cursor_pos]
        max_width = self._letter_widths[len(self._value)]
        cursor_width = 2
        x = width - self._view_x
        if x < 0: 
            self._view_x += x
        if x+cursor_width > self.box_width:
            self._view_x += x + cursor_width - self.box_width
        if self._view_x+self.box_width> max_width and max_width > self.box_width:
            self._view_x = max_width - self.box_width
        image = self._rendered_text.copy()
        image.crop((self._view_x, 0), 
                   (self.box_width, self._box_height))
        self._text.image = image
        # if highlighting
        #   print first segment of non-highlight
        #   print highlight text
        #   print second segment of non-highlight
        # else:
        #   print regular text
        
    def _render_cursor(self):
        self._cursor.x = min(max(self._letter_widths[self.cursor_pos] - self._view_x, 0), self.box_width)
        self._cursor.y = 0
        
    _non_insertable_keys =(spyral.keys.up, spyral.keys.down, 
                           spyral.keys.left, spyral.keys.right,
                           spyral.keys.home, spyral.keys.end, 
                           spyral.keys.pageup, spyral.keys.pagedown,
                           spyral.keys.numlock, spyral.keys.capslock,
                           spyral.keys.scrollock, spyral.keys.rctrl,
                           spyral.keys.rshift, spyral.keys.lshift,
                           spyral.keys.lctrl, spyral.keys.rmeta,
                           spyral.keys.ralt, spyral.keys.lalt,
                           spyral.keys.lmeta, spyral.keys.lsuper, 
                           spyral.keys.rsuper, spyral.keys.mode)
    _non_skippable_keys = (' ', '.', '?', '!', '@', '#', '$',
                           '%', '^', '&', '*', '(', ')', '+',
                           '=', '{', '}', '[', ']', ';', ':',
                           '<', '>', ',', '/', '\\', '|', '"',
                           "'", '~', '`')
    _non_printable_keys = ('\t', '')+_non_insertable_keys
                           
    def _find_next_word(self, text, start=0, end=None):
        if end is None:
            end = len(text)
        for index, letter in enumerate(text[start:end]):
            if letter in self._non_skippable_keys:
                return start+(index+1)
        return end

    def _find_previous_word(self, text, start=0, end=None):
        if end is None:
            end = len(text)
        for index, letter in enumerate(reversed(text[start:end])):
            if letter in self._non_skippable_keys:
                return end-(index+1)
        return start
        
    def _delete(self, by_word = False):
        if self._selecting:
            start, end = sorted((self.cursor_pos, self._selection_pos))
            self.cursor_pos = start
            self._remove_char(start, end)
        elif by_word:
            start = self.cursor_pos
            end = self._find_next_word(self.value, self.cursor_pos, len(self._value))
            self._remove_char(start, end)
        else:
            self._remove_char(self.cursor_pos)
        
    def _backspace(self, by_word = False):
        if self._selecting:
            start, end = sorted((self.cursor_pos, self._selection_pos))
            self.cursor_pos = start
            self._remove_char(start, end)
        elif not self._cursor_pos:
            pass
        elif by_word:
            start = self._find_previous_word(self.value, 0, self.cursor_pos-1)
            end = self.cursor_pos
            self.cursor_pos= start
            self._remove_char(start, end)
        elif self._cursor_pos:
            self.cursor_pos-= 1
            self._remove_char(self.cursor_pos)
    
    def _move_cursor_left(self, by_word = False):
        if by_word:
            self.cursor_pos = self._find_previous_word(self.value, 0, self.cursor_pos)
        else:
            self.cursor_pos= max(self.cursor_pos-1, 0)
    
    def _move_cursor_right(self, by_word = False):
        if by_word:
            self.cursor_pos = self._find_next_word(self.value, self.cursor_pos, len(self.value))
        else:
            self.cursor_pos= min(self.cursor_pos+1, len(self.value))
            
    def update(self, dt):
        if self._focused:
            self._cursor_time += dt
            if self._cursor_time > self._cursor_blink_interval:
                self._cursor_time -= self._cursor_blink_interval
                self._cursor.visible = not self._cursor.visible
    
    def handle_key_down(self, event):
        key = event.key
        mods = event.mod
        shift_is_down= (mods & spyral.mods.shift) or (key in (spyral.keys.lshift, spyral.keys.rshift))
        shift_clicked = not self._shift_was_down and shift_is_down
        self._shift_was_down = shift_is_down
        
        if shift_clicked or (shift_is_down and not 
                             self._selecting and 
                             key in TextInputWidget._non_insertable_keys):
            self._selection_pos = self.cursor_pos
            self._selecting = True
            
        if key == spyral.keys.left:
            self._move_cursor_left(mods & spyral.mods.ctrl)
        elif key == spyral.keys.right: 
            self._move_cursor_right(mods & spyral.mods.ctrl)
        elif key == spyral.keys.home:
            self.cursor_pos = 0
        elif key == spyral.keys.end:
            self.cursor_pos = len(self.value)
        elif key == spyral.keys.delete:
            self._delete(mods & spyral.mods.ctrl)
        elif key == spyral.keys.backspace:
            self._backspace(mods & spyral.mods.ctrl)
        else:
            if key not in TextInputWidget._non_printable_keys:
                if self._selecting:
                    self._delete()
                unicode = chr(event.key)
                if self.validate(unicode):
                    self._insert_char(self.cursor_pos, unicode)
                    self.cursor_pos+= 1
                
        if not shift_is_down or (shift_is_down and key not in TextInputWidget._non_insertable_keys):
            self._selecting = False
            self._render_text()
        if self._selecting:
            self._render_text()
    
    def handle_mouse_over(self, event): pass
    def handle_mouse_out(self, event): pass
    def handle_key_up(self, event): pass
    
    def handle_mouse_up(self, event):
        self.cursor_pos = self._compute_cursor_pos(event.pos)
    def handle_mouse_down(self, event):
        if not self._selecting:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self._selection_pos = self.cursor_pos
                self._selecting = True
        elif not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            self._selecting = False
        self.cursor_pos = self._compute_cursor_pos(event.pos)
        # set cursor position to mouse position
        if self.default_value: 
            self.value = ''
            self.default_value = False
        self._render_text()
        self._stop_blinking()
    def handle_mouse_motion(self, event):
        left, center, right = event.buttons
        if left:
            if not self._selecting:
                self._selecting = True
                self._selection_pos = self.cursor_pos
            self.cursor_pos = self._compute_cursor_pos(event.pos)
            self._render_text()
            self._stop_blinking()
    def handle_focus(self, event):
        self._focused = True
        self.image = self._image_focused
        if self.default_value:
            self._selecting = True
            self._selection_pos = 0
        else:
            self._selecting = False
        self.cursor_pos= len(self._value)
        self._render_text()
    def handle_blur(self, event):
        self.image = self._image_plain
        self._focused = False
        self._cursor.visible = False
        self.default_value = self._default_value_permanant  


# Module Magic

old = sys.modules[__name__]

class _WidgetWrapper(object):
    creation_counter = 0
    def __init__(self, cls, *args, **kwargs):
        _WidgetWrapper.creation_counter += 1
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def __call__(self, form, name):
        return self.cls(form, name, *self.args, **self.kwargs)

class module(types.ModuleType):
    def register(self, name, cls):
        setattr(self, name, functools.partial(_WidgetWrapper, cls))

# Keep the refcount from going to 0
widgets = module(__name__)
sys.modules[__name__] = widgets
widgets.__dict__.update(old.__dict__)

widgets.register('TextInput', TextInputWidget)
widgets.register('RadioButton', RadioButtonWidget)
widgets.register('Checkbox', CheckboxWidget)
widgets.register('ToggleButton', ToggleButtonWidget)
widgets.register('Button', ButtonWidget)