import tw2.core as twc
import tw2.forms as twf


class ContainerForm(twf.Form):
    class child(twf.TableLayout):
        container_id = twf.TextField()
        status = twf.TextField()
        author_user_id = twf.NumberField()

    action = '/save_record'
    submit = twf.SubmitButton(value='Submit')
