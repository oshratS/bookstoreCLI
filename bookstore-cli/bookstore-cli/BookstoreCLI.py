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
                'uid': args[0],     
                'created': str(datetime.datetime.now()),                                             
            })

            print('Sucessfully created new user: {0}'.format(user.uid))
            return user
        except Exception as e:
            print('User {0} already exist in the db'.format(args[0]))    
            return 'user already exist'
        
        return

    def do_deleteUser (self, args):
        "deletes one user by it's id, i.e: deleteUser username"

        args = args.split()
        
        try:
            auth.delete_user(args[0])
                    
            self.users_ref.child(args[0]).delete()            
            print('Sucessfully deleted user: {0}'.format(args[0]))
            
        except Exception:
            print('an error has occured: %s' % e)            
                        
        return

    def do_printUserList (self, args):
        "prints our users names, i.e: printUserList"        

        data = self.users_ref.order_by_key().get()
        for key, val in data.items():
            print(key)
        
        return

    def do_getUser (self, args):
        "checks if a user exist, i.e: getUser username"

        args = args.split()
       
        try:  
            user = auth.get_user(args[0])        
      
            print('User {0} exist in the db'.format(user.uid))
            return user
        except Exception:
            print('User {0} does not exist in the db'.format(args[0]))    
            return 'not found'
        
    def do_deleteAllUsers (self, args):
        "deletes all users from the system, i.e: deleteAllUsers"

        try:
            data = self.users_ref.order_by_key().get()
            for key, val in data.items():
                self.do_deleteUser(key) 

            print('All users were deleted successfully')
        except Exception as e:
            print('an error has occured: %s' % e)  

        return
 
    def do_inputExtraUserDetails (self, args):
        args = args.split()
        username = args[0]
        email = args[1]
        phone = args[2]

        try:
            user = auth.update_user(
                uid=username,
                email=email,
                phone_number=phone)

            self.users_ref.child(args[0]).update({
                'email': email,
                'phone_number': phone
            })
    
            print('Sucessfully updated user: {0}'.format(user.uid))
        except Exception as e:            
            print('an error has occured: %s' % e)  

        return

    def do_exit(self, line):
        "enter 'exit' in order to close this interface"
        return True

if __name__ == '__main__':    
    BookstoreCLI().cmdloop('BookstoreCLI - welcome admin, shall we start? (enter "help" at any time)')