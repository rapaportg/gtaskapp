from datetime import date, timedelta
from gtasks import Gtasks, task, tasklist
from lazyme import color_print
import sys

# to use this for yourself goto google apis and make an OAuth 2.0 credential for the Tasks API.
# then down load that file and place it where ever you want. The next step is to change the
# 'credentials_locations=' in the constructor below to where ever you save your credentials file
# from google. The first time you run it, a browser will popup with google asking for your approval of this action
# hit yes, then copy the code they give you and paste that into the terminal. thats it your done.

#self.gt = Gtasks(identifier='default', auto_push=True, auto_pull=False, open_browser=True, force_login=False, credentials_location='../.idsafe/credentials.json')
colors = ['red', 'yellow', 'green', 'blue', 'pink', 'cyan', 'white']

def due_date_print(task):
    if (date.today() != task.due_date):
        color_print(str(task.due_date), end='\t', color='cyan')
    elif (date.today() == task.due_date):
        color_print(str(task.due_date), end='\t', color='red', blink=True)
    elif (task.due_date == date.today() + timedelta(days=1)):
        color_print(str(task.due_date), end='\t', color='yellow')
    elif (task.due_date == date.today() + timedelta(days=2)):
        color_print(str(task.due_date), end='\t', color='pink')
    else:
        color_print(str(task.due_date), end='\t', color='white')


class GTaskApp(object):
    def __init__(self):
        self.gt = Gtasks(identifier='default', auto_push=True, auto_pull=False, open_browser=True, force_login=False, credentials_location='/home/gabe/Documents/.idsafe/credentials.json')
        self.task_lists = self.gt.get_lists()
        self.lists = {}
        self.num_of_list = 0
        self.margin = 60
        self.seperateLists()

    def seperateLists(self):
        for lst in self.task_lists:
            self.lists[self.num_of_list] =lst
            self.num_of_list += 1

    def printLists(self):
        i = 0
        for lst in range(len(self.lists)):
            if (self.lists[i] == None):
                color_print(str(i) + ". DELETED", color=colors[0], bold=False, italic=True)
            else:
                color_print(str(i) + ". " + self.lists[i].title, color=colors[i%7], bold=True)
                self.printList(self.lists[i].get_tasks())
            i += 1
        #self.home()

    def printList(self, lst):
        i = 1
        for task in lst:
            if task.complete:
                print('  (x)\t' + str(i) + '. ' + task.title + (' ' * (self.margin - len(task.title))) + 'Due: ',end=' ')
                due_date_print(task)
                print("\tNotes: " + str(task.notes))
            else:
                print('  ( )\t' + str(i) + '. ' + task.title + (' ' * (self.margin - len(task.title))) + 'Due: ',end=' ')
                due_date_print(task)
                print("\tNotes: " + str(task.notes))
            i += 1

    def make_new_list(self):
        name = str(input("Name your new list (enter 'cancel' to abort): "))
        if name == 'cancel':
            #finish later
            self.home()
        else:
            x = self.gt.new_list(name)
        self.lists[self.num_of_list] = x
        self.num_of_list += 1

        self.home()


    def home(self):
        self.gt.push_updates()
        self.printLists()
        #print("Enter 1 to show your lists")
        print("\nEnter 1 to make a new list")
        print("Enter 2 to edit a list")
        print("Enter 3 to delete a list")
        print("Enter 5 to exit")
        user_in = None
        try:
            user_in = int(input())
        except:
            print(Exception)

        if user_in == None:
            self.home()

        if user_in == 1:
            self.make_new_list()
            self.home()
        if user_in == 2:
            which_list = int(input("Which list (Number): "))
            self.edit_list(which_list)
            self.home()
        if user_in == 3:
            which_list = int(input("Which list (Number): "))
            try:
                self.lists[which_list].permanently_delete()
            except:
                print("weird")
            self.lists[which_list] = None
            #self.num_of_list -= 1
            self.home()
        if user_in == 5:
            sys.exit()
        self.home()


    def edit_list(self, index):
        color_print(self.lists[index].title, color=colors[(index)%7])
        self.printList(self.lists[index])
        items = []
        for item in self.lists[index]:
            items += [item]

        print("\n\nEnter 1 to add a task")
        print("Enter 2 to toggle completed")
        print("Enter 3 to delete a task")
        print("Enter 4 to add a note")
        print("Enter 5 to return to home menu")

        user_in = None
        try:
            user_in = int(input())
        except:
            print(Exception)

        if user_in == None:
            self.edit_list(index)
        if user_in == 1:
            x = True
            while (x == True):
                task = input("What is the new task: ")
                notes = input("Any notes to add: ")
                x = False
                if (len(task) > self.margin):
                    color_print("Too long (" + str(len(task)) + '/' + str(self.margin) + ' characters)', color='red')
                    x = True
            days = int(input("How many days do you have to do it: "))
            if days == None:
                days = 0
            self.lists[index].new_task(task, date.today() + timedelta(days=days), notes)
        if user_in == 2:

            task = int(input("which task: "))
            if  items[task-1].complete:
                items[task-1].complete = False
            else:
                items[task-1].complete = True
        if user_in == 3:
            task = int(input("which task: "))
            items[task-1].deleted = True

        if user_in == 4:
            self.home()
        if user_in == 5:
            self.home()

        self.edit_list(index)








if __name__=="__main__":
    app = GTaskApp()
    app.home()
