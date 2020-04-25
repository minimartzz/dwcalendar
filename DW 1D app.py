import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from libdw import pyrebase
import datetime
import RPi.GPIO as GPIO
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock

############################# Firebase Initialisation ####################################################
url = 'https://test-firebase-95e43.firebaseio.com/'
apikey = 'AIzaSyDDzT4FSVfdXLocVNLyio0vwFlWRkhmnTQ'

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
##########################################################################################################

############################# GPIO Initialization ########################################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, GPIO.PUD_DOWN)
black = 25 # Subject Buttons
green = 12
red = 16
yellow = 20
white = 21  # Starts the Application

##########################################################################################################

calendar_info = {}


class description_selection(GridLayout):
    def __init__(self, **kwargs):
        super(description_selection, self).__init__(**kwargs)
        self.cols = 1

        l1 = Label(text="Please select description below",
                   font_size=20)
        self.add_widget(l1)
        self.desc = Spinner(text="Homework", values=(
        'Homework', 'Quiz', 'Project Due Time', 'Exam', 'Pre-class Activity', 'MCQ', 'Submission Due', 'Other'))
        self.add_widget(self.desc)


class date_selection(GridLayout):
    def __init__(self, **kwargs):
        super(date_selection, self).__init__(**kwargs)
        self.cols = 3

        l1 = Label(text="day",
                   font_size=20)
        self.add_widget(l1)
        l2 = Label(text="month",
                   font_size=20)
        self.add_widget(l2)
        l3 = Label(text="year",
                   font_size=20)
        self.add_widget(l3)

        self.day = Spinner(text="12", values=(
        "1", "2", "3", '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'))
        self.day.size_hint = (0.333, 1.0)
        self.add_widget(self.day)

        self.month = Spinner(text="1", values=("1", "2", "3", '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        self.month.size_hint = (0.333, 1.0)
        self.add_widget(self.month)

        now = datetime.datetime.now()
        self.year_now = now.year
        self.year = Spinner(text="%s" % str(self.year_now),
                            values=("%s" % str(self.year_now), "%s" % str(self.year_now + 1)))
        self.year.size_hint = (0.333, 1.0)
        self.add_widget(self.year)


class time_selection(GridLayout):
    def __init__(self, **kwargs):
        super(time_selection, self).__init__(**kwargs)
        self.cols = 1

        self.hour = Slider(min=00, max=23, value=00)
        self.add_widget(self.hour)
        self.hour.bind(value=self.get_hour_value)

        self.min = Slider(min=00, max=59, value=00)
        self.add_widget(self.min)
        self.min.bind(value=self.get_hour_value)

        self.time_label = Label(text="%s" % int(self.hour.value) + ' : ' + "%s" % int(self.min.value))
        self.add_widget(self.time_label)
        self.time_label.pos_hint = {'x': .1, 'y': .3}

    def get_hour_value(self, slider, value):
        self.time_label.text = "%s" % int(self.hour.value) + ' : ' + "%s" % int(self.min.value)


class MyLabel(Label):
    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        self.bind(size=self.setter('text_size'))
        self.padding = (20, 20)


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.superlayout = GridLayout(rows=2)
        self.banner = Label(text='Please Select a Subject', font_size=72)

        self.blackbut = Button(text='Digital World', background_color=[0.46, 0.49, 0.49, 1])
        self.greenbut = Button(text='Intro to Biology', background_color=[0.38, 0.166, 0.91, 1])
        self.redbut = Button(text='Physical World', background_color=[0.242, 0.38, 0.19, 1])
        self.yellowbut = Button(text='Systems World', background_color=[0.254, 0.241, 0.96, 1])

        self.layout = GridLayout(cols=4)
        self.layout.add_widget(self.blackbut)
        self.layout.add_widget(self.greenbut)
        self.layout.add_widget(self.redbut)
        self.layout.add_widget(self.yellowbut)

        self.superlayout.add_widget(self.banner)
        self.superlayout.add_widget(self.layout)

        self.add_widget(self.superlayout)
        Clock.schedule_interval(self.checker, 1.0/10.0)

    def change_screen(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'event_add'

    def checker(self,instance):
        if GPIO.input(black) == GPIO.HIGH:
            self.change_screen()
            calendar_info['colour'] = '8'
        elif GPIO.input(green) == GPIO.HIGH:
            self.change_screen()
            calendar_info['colour'] = '10'
        elif GPIO.input(red) == GPIO.HIGH:
            self.change_screen()
            calendar_info['colour'] = '11'
        elif GPIO.input(yellow) == GPIO.HIGH:
            self.change_screen()
            calendar_info['colour'] = '5'


class GUIScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        superBox = BoxLayout(orientation='vertical')

        # 1st row : Subject
        horizontalBox1 = BoxLayout(orientation='horizontal')
        l1 = MyLabel(text="Subject",
                     font_size=24, halign='center', valign='middle')
        horizontalBox1.add_widget(l1)

        self.subject = Label(text="Changed?",
                             font_size=20)
        horizontalBox1.add_widget(self.subject)

        # 2nd row : Description
        horizontalBox2 = BoxLayout(orientation='horizontal')
        l2 = MyLabel(text="Description",
                     font_size=24, halign='center', valign='middle')
        horizontalBox2.add_widget(l2)

        self.description = description_selection()
        horizontalBox2.add_widget(self.description)

        # 3rd row : Due Date
        horizontalBox3 = BoxLayout(orientation='horizontal')
        l3 = MyLabel(text="Due Date",
                     font_size=24, halign='center', valign='middle')
        horizontalBox3.add_widget(l3)

        self.due_date = date_selection()
        horizontalBox3.add_widget(self.due_date)

        # 4th row : Due Time
        horizontalBox4 = BoxLayout(orientation='horizontal')
        l4 = MyLabel(text="Due Time",
                     font_size=24, halign='center', valign='middle')
        horizontalBox4.add_widget(l4)

        self.due_time = time_selection()
        horizontalBox4.add_widget(self.due_time)

        # 5th row :Upload button
        verticalBox = BoxLayout(orientation='vertical')
        btn = Button(text="Upload", font_size=24)
        btn.bind(on_press=self.upload)  # on_press
        verticalBox.add_widget(btn)

        superBox.add_widget(horizontalBox1)
        superBox.add_widget(horizontalBox2)
        superBox.add_widget(horizontalBox3)
        superBox.add_widget(horizontalBox4)
        superBox.add_widget(verticalBox)

        self.add_widget(superBox)
        Clock.schedule_interval(self.subject_change, 1.0/10.0)

    def subject_change(self, instance):
        if GPIO.input(black) == GPIO.HIGH:
            self.subject.text = 'Digital World'
        elif GPIO.input(green) == GPIO.HIGH:
            self.subject.text = 'Intro to Biology'
        elif GPIO.input(red) == GPIO.HIGH:
            self.subject.text = 'Physical World'
        elif GPIO.input(yellow) == GPIO.HIGH:
            self.subject.text = 'Systems World'

    # upload-to-firebase function
    def upload(self, *args):
        calendar_info['event_name'] = '{}'.format(self.description.desc.text)
        calendar_info['start_date'] = '{}-{}-{}T{}:{}:00'.format(self.due_date.year.text,
                                                                        self.due_date.month.text,
                                                                        self.due_date.day.text,
                                                                        int(self.due_time.hour.value),
                                                                        int(self.due_time.min.value))
        calendar_info['end_date'] = '{}-{}-{}T{}:{}:00'.format(self.due_date.year.text, self.due_date.month.text,
                                                                      self.due_date.day.text,
                                                                      int(self.due_time.hour.value),
                                                                      int(self.due_time.min.value))
        db.child('DW').update(calendar_info)
        App.get_running_app().stop()
        main()


class FinalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GUIScreen(name='event_add'))

        return sm

def main():
    while True:
        if GPIO.input(white) == GPIO.HIGH:
            FinalApp().run()
            break

main()

