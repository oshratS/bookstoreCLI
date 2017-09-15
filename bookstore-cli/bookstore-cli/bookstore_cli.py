import cmd, datetime, json
from firebase_admin import auth, credentials, db, initialize_app

import cmd

class BookstoreCLI(cmd.Cmd):
    cred = credentials.Certificate('bookstore-d9058-firebase-adminsdk-bb0vo-a1fefbda0b.json')

    # Initialize the app with a service account, granting admin privileges
    initialize_app(cred, {
        'databaseURL': 'https://bookstore-d9058.firebaseio.com'
    })

    ref = db.reference('/')
    users_ref = ref.child('users')
    
    def do_createUser (self, args):        
        "creates a new user, i.e: createUser username password"        

        args = args.split()
        
        try:
            user = auth.create_user(
                uid=args[0],
                email='{0}@bookstore.com'.format(args[0]),
                password=args[1],
            )                  
                     
            self.users_ref.child(args[0]).set({               
                'created': str(datetime.datetime.now()),                             
            })

            print('Sucessfully created new user: {0}'.format(user.uid))
            
        except Exception as e:
            print('an error has occured: %s' % e)            
        
        return

    def do_deleteUser (self, args):
        args = args.split()

        auth.delete_user(args[0])
        print('Successfully deleted user')
        return

    def do_printUserList (context):
        # only name
        return

    def do_getUser (self, args):
        args = args.split()
        #user = auth.get_user(uid)
        #print 'Successfully fetched user data: {0}'.format(user.uid)
        return

    def do_deleteAllUsers (context):

        return
 
    def do_inputExtraUserDetails (self, args):
        args = args.split()
        username = args[0]
        email = args[1]
        phone = args[2]

        user = auth.update_user(
            uid=username,
            email=email,
            phone_number=phone)
    
        print('Sucessfully updated user: {0}'.format(user.uid))
        retrun

    def do_EXIT(self, line):
        "enter EXIT in order to close this interface"
        return True

if __name__ == '__main__':    
    BookstoreCLI().cmdloop('BookstoreCLI - welcome admin, shall we start? (enter "help" at any time)')