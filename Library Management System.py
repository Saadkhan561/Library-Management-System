import pandas as pd
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyDUxTzmV3YU6_ugbIcZDO0o5WOYaJT1UCk",
    'authDomain': "librarymanagement-51f33.firebaseapp.com",
    'projectId': "librarymanagement-51f33",
    'storageBucket': "librarymanagement-51f33.appspot.com",
    'messagingSenderId': "211196055518",
    'appId': "1:211196055518:web:a2f18f10c10ce914f2d74f",
    'measurementId': "G-YDY560KHQZ",
    'databaseURL': "https://librarymanagement-51f33-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


class lib():
    def __init__(self):
        self.user=None
        self.logged_in = False
        self.users = []
        self.userDetails = {}
        self.books = 15
        self.available_books = [1, 2, 3, 4, 5,
                                6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def display(self):
        self.books_DB = {'Serial': [], 'Title': [],
                         'Author': [], 'Description': []}
        for i in self.available_books:
            books = db.child("Books").get()
            for j in books.each():
                if j.val().get('serial') == i:
                    self.books_DB['Serial'].append(j.val().get('serial'))
                    self.books_DB['Title'].append(j.val().get('title'))
                    self.books_DB['Author'].append(j.val().get('author'))
                    self.books_DB['Description'].append(
                        j.val().get('description'))
        self.df = pd.DataFrame(self.books_DB)
        self.df.index = [i for i in range(1, len(self.df.values)+1)]
        return self.df

    def register(self):
        self.name = input('Enter your username :')
        self.pwd = input('Enter your password :')
        self.email = input('Enter your email :')
        self.users.append(self.name)
        self.users.append(self.pwd)
        self.users.append(self.email)
        self.userDetails = {'name': self.users[0],
                            'password': self.users[1], 'email': self.users[2]}
        db.child('Users').child(self.name).set(self.userDetails)

    def login(self):
        self.username = input('Enter your username :')
        self.pwd = input('Enter your password :')
        snapshot = db.child('Users').get()

        try:
            lst_U=[]
            lst_P=[]
            for i in snapshot.each():
                lst_U.append(i.val().get('name'))
                lst_P.append(i.val().get('password'))
            if (self.username in lst_U) and (self.pwd in lst_P):
                self.logged_in = True
                self.user = self.username
                print()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print('Enter Valid Credentials!!!')
            n = input('Do you want to create a new account? ')
            if n == 'YES' or n == 'Yes' or n == 'yes':
                self.register()
            else:
                self.login()
        
        if self.logged_in == True:
            print(self.username + ' logged in...')
        else:
            print('Wrong User!!!')

    def search(self):
        print('How do you want to search the book?' +
              '\n1: By title' + '\n2: By author name')
        choice = int(input('Enter your choice :'))
        if choice == 1:
            title = input('Enter title of the book : ')
            try:
                name = db.child('Books').get()
                for i in name.each():
                    if i.val().get('title') == title:
                        print('Serial No : ' + str(i.val().get('serial')))
                        print('Title : ' + i.val().get('title'))
                        print('Author : ' + i.val().get('author'))
                        print('Description : ' + i.val().get('description'))
            except:
                print('No Results!!!')

        elif choice == 2:
            author = input('Enter author of the book : ')
            name = db.child('Books').get()
            for i in name.each():
                if i.val().get('author') == author:
                    print('Serial No : ' + i.val().get('serial'))
                    print('Title : ' + i.val().get('title'))
                    print('Author : ' + i.val().get('author'))
                    print('Description : ' + i.val().get('description'))

        print('Do you want to borrow this book?')
        choice1 = input('Enter your choice : ')
        if choice1 == 'yes':
            self.checkout_book()

    def remove_book(self):
        n = int(input('Enter serial no. of the book :'))
        book = db.child('Books').get()
        for i in book.each():
            if i.val().get('serial') == n:
                name = i.val().get('name')
        db.child('Books').child(name).remove()

    def add_book(self):
        title = input('Enter title of the book :')
        author = input('Enter author of the book :')
        description = input('Enter description :')
        book = {'serial': self.books+1, 'title': title,
                'author': author, 'description': description}
        db.child('Books').child(title).set(book)
        self.books += 1
        self.available_books.append(self.books)

    def checkout_book(self):
        n = int(input('Enter serial no of the book :'))
        if n in self.available_books:
            self.available_books.remove(n)
            db.child('Users').child(self.user).update(
                {'borrowed book serial no': n})
        else:
            print('This book has already been borrowed!!!')
            print('Do you want to reserve this book (YES/NO)')
            choice = input('Enter your choice : ').lower()
            if choice=='yes':
                library.reserve_book()

    def renew_book(self):
        n = int(input('Enter serial no of the book : '))
        book = db.child('Users').get()
        for i in book.each():
            if i.val().get('borrowed book serial no') == n:
                print('You renewed this book!!!')
        else:
            print('You first need to borrow this book!!!')

    def reserve_book(self):
        n = int(input('Enter serial no of the book : '))
        reserved = db.child('Users').get()
        for i in reserved.each():
            if i.val().get('reserved book serial no') == n:
                print('You already reserved this book!!!')
            else:
                book1 = {'reserved book serial no': n}
                db.child('Users').child(self.user).update(book1)


    def return_book(self):
        n = int(input('Enter serial no of the book :'))
        if self.available_books == 15:
            print('Maximum limit is reached!!!')
        else:
            self.available_books.append(n)
            db.child('Users').child(self.user).child('borrowed book serial no').remove()

        # -----(SORTING ALGORITHM)-----
        # -----(   BUBBLE SORT  )-----
        for i in range(len(self.available_books)-1, 0, -1):
            for j in range(i):
                if self.available_books[j] > self.available_books[j+1]:
                    temp = self.available_books[j]
                    self.available_books[j] = self.available_books[j+1]
                    self.available_books[j+1] = temp

        x = db.child('Users').get()
        for i in x.each():
            if i.val().get('reserved book serial no') == n:
                user = i.val().get('name')
                db.child('Users').child(user).child(
                    'reserved book serial no').remove()
                db.child('Users').child(user).update(
                    {'borrowed book serial no': n})

    def logout(self):
        self.user = None


library = lib()

print('*'*75)
print('**********************  TREASURE OF KNOWLEDGE LIBRARY  **********************')
while True:
    print('Do you want to...'+'\n1: CREATE A NEW ACCOUNT' +
          '\n2: LOGIN'+'\nPress e to exit')
    choice = input('Enter your choice : ')
    if choice == '1':
        library.register()
    elif choice == '2':
        library.login()
        print()
        while True:
            print(
                '**********************  WELCOME TO TREASURE OF KNOWLEDGE LIBRARY  **********************')
            print()
            print(library.display())
            print()
            print('1: Add a book'+'\n2: Remove a book'+'\n3: Search a book' +
                  '\n4: Borrow a book'+'\n5: Reserve a book'+'\n6: Return a book'+'\n7: Renew Book'+'\n8: Log Out')
            choice = int(input('Enter your choice : '))
            if choice == 1:
                library.add_book()
            elif choice == 2:
                library.remove_book()
            elif choice == 3:
                library.search()
            elif choice == 4:
                library.checkout_book()
            elif choice == 5:
                library.reserve_book()
            elif choice == 6:
                library.return_book()
            elif choice == 7:
                library.renew_book()
            elif choice == 8:
                library.logout()
                break
    elif choice == 'e':
        print('THANKS FOR COMING!!!')
        break
