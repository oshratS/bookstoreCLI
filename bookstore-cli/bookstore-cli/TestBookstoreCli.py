import unittest, os, sys
sys.path.append(os.path.abspath('.'))
from BookstoreCLI import BookstoreCLI 

class TestBookstoreCli(unittest.TestCase):

 #The test checks if a specific user exists or not.
    def test_getUser_not_found(self):  
        user = BookstoreCLI.do_getUser(self, 'banana')           
        self.assertEqual(user, 'not found')

    def test_getUser_found(self):  
        user = BookstoreCLI.do_getUser(self, 'sparta')           
        self.assertEqual(user.email, 'sparta@bookstore.com')

#The test check if a user that we try to create allready exists or not
    def test_createUser_already_exist(self):
        user = BookstoreCLI.do_createUser(self, 'sparta password')
        self.assertEqual(user, 'user already exist')

if __name__ == '__main__':
    unittest.main()