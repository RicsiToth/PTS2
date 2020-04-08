import unittest
from library_mixed import Library, Reservation
from itertools import count

class TestLibrary(unittest.TestCase):
    
    def setUp(self):
        self.library = Library()
        Reservation._ids = count(0)
        
    def test_init(self):
        self.assertEqual(len(self.library._users), 0)
        self.assertEqual(len(self.library._books), 0)
        self.assertEqual(len(self.library._reservations), 0)

    def test_add_user(self):
        self.assertTrue(self.library.add_user("Tomas"))	
        self.assertTrue(len(self.library._users), 1)
        self.assertFalse(self.library.add_user("Tomas"))
        self.assertTrue(len(self.library._users), 1) 
        
    def test_add_book(self):
        self.library.add_book("book1")
        self.assertEqual(self.library._books.get("book1", 0), 1)
        self.assertEqual(len(self.library._books), 1)
        self.library.add_book("book2")
        self.assertEqual(len(self.library._books), 2)

    def test_reserve_book_succes(self):
        self.library.add_user("Richard")
        self.library.add_book("book1")
        self.assertEqual(self.library.reserve_book("Richard", "book1", 15, 20), 0)
        self.assertEqual(len(self.library._reservations), 1)
        self.assertEqual(self.library.reserve_book("Richard", "book1", 21, 30), 1)
        self.assertEqual(len(self.library._reservations), 2)

    def test_reserve_book_for_not_a_user(self):
        self.library.add_book("book1")
        self.assertEqual(self.library.reserve_book("Richard", "book1", 15, 20), -1)

    def test_reserve_book_with_no_books(self):
        self.library.add_user("Richard")
        self.assertEqual(self.library.reserve_book("Richard", "book1", 15, 20), -1)

    def test_reserve_book_mixed_dates(self):
        self.library.add_user("Richard")
        self.library.add_book("book1")
        self.assertEqual(self.library.reserve_book("Richard", "book1", 20, 15), -1)

    def test_reserve_book_more_reserved_books_in_date_than_book_count(self):
        self.library.add_user("Richard")
        self.library.add_user("Tomas")
        self.library.add_book("book1")
        self.library.reserve_book("Richard", "book1", 15, 20)
        self.library.reserve_book("Richard", "book1", 30, 40)
        self.assertEqual(self.library.reserve_book("Tomas", "book1", 16, 17), -1)

    def test_reserve_book_2_different_books_on_the_same_date(self):
        self.library.add_user("Richard")
        self.library.add_book("book1")
        self.library.add_book("book2")
        self.assertEqual(self.library.reserve_book("Richard", "book1", 21, 30), 0)
        self.assertEqual(self.library.reserve_book("Richard", "book2", 21, 30), 1)

    def test_check_reservation(self):
        self.library.add_user("Richard")
        self.library.add_book("book1")
        self.library.reserve_book("Richard", "book1", 21, 30)
        self.assertTrue(self.library.check_reservation("Richard", "book1", 25))
        self.assertTrue(self.library.check_reservation("Richard", "book1", 30))
        self.assertTrue(self.library.check_reservation("Richard", "book1", 21))
        self.assertFalse(self.library.check_reservation("Richard", "book1", 20))

    def test_change_reservation(self):
        self.library.add_user("Richard")
        self.library.add_user("Tomas")
        self.library.add_book("book1")
        self.library.reserve_book("Richard", "book1", 21, 30)
        self.assertFalse(self.library.change_reservation("Richard", "book", 25, "Tomas"))
        self.assertFalse(self.library.change_reservation("Richard", "book", 25, "Fero"))
        self.assertTrue(self.library.change_reservation("Richard", "book1", 25, "Tomas"))

if __name__ == '__main__':
    unittest.main()
