import unittest
from library_mixed import Library
from itertools import count

class Reservation_Mock_True(object):
    _ids = count(0)
    
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation_Mock_True._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return True
  
    def includes(self, date):
        return True       
    
    def identify(self, date, book, for_):
        return (True, "")        
  
    def change_for(self, for_):
        pass


class Reservation_Mock_False(Reservation_Mock_True):
    def overlapping(self, other):
        return False
  
    def includes(self, date):
        return False       
    
    def identify(self, date, book, for_):
        return (False, "")


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.libraryTrue = Library(Reservation_Mock_True)
        self.libraryFalse = Library(Reservation_Mock_False)
        Reservation_Mock_True._ids = count(0)
        self.libraryTrue.add_user("Richard")
        self.libraryTrue.add_user("Tomas")
        self.libraryTrue.add_book("book1")
        self.libraryTrue.reserve_book("Richard", "book1", 21, 30)
        self.libraryFalse.add_user("Richard")
        self.libraryFalse.add_user("Tomas")
        self.libraryFalse.add_book("book1")
        self.libraryFalse.reserve_book("Richard", "book1", 21, 30)
        
    def test_init(self):
        self.assertEqual(len(self.libraryTrue._users), 2)
        self.assertEqual(len(self.libraryTrue._books), 1)
        self.assertEqual(len(self.libraryTrue._reservations), 1)

    def test_add_user(self):
        self.assertTrue(self.libraryTrue.add_user("Feri"))	
        self.assertTrue(len(self.libraryTrue._users), 1)
        self.assertFalse(self.libraryTrue.add_user("Tomas"))

    def test_add_book(self):
        self.assertEqual(self.libraryTrue._books.get("book1", 0), 1)
        self.assertEqual(len(self.libraryTrue._books), 1)
        self.libraryTrue.add_book("book2")
        self.assertEqual(len(self.libraryTrue._books), 2)

    def test_reserve_book_succes(self):
        self.assertEqual(self.libraryFalse.reserve_book("Richard", "book1", 21, 30), (True, 2))
        self.assertEqual(len(self.libraryFalse._reservations), 2)

    def test_reserve_book_for_not_a_user(self):
        self.assertEqual(self.libraryTrue.reserve_book("Feri", "book1", 15, 20), (False, "user"))

    def test_reserve_book_with_no_books(self):
        self.libraryTrue.add_user("Richard")
        self.assertEqual(self.libraryTrue.reserve_book("Richard", "book2", 15, 20), (False, "book_count"))

    def test_reserve_book_mixed_dates(self):
        self.assertEqual(self.libraryTrue.reserve_book("Richard", "book1", 30, 20), (False, "date"))

    def test_reserve_book_more_reserved_books_in_date_than_book_count(self):     
        self.assertEqual(self.libraryTrue.reserve_book("Tomas", "book1", 16, 17), (False, "reserved"))

    def test_reserve_book_2_different_books_on_the_same_date(self):
        self.libraryFalse.add_book("book2")
        self.assertEqual(self.libraryFalse.reserve_book("Richard", "book1", 21, 30), (True, 2))
        self.assertEqual(self.libraryFalse.reserve_book("Richard", "book2", 21, 30), (True, 3))

    def test_check_reservation(self):
        self.libraryTrue.reserve_book("Richard", "book1", 21, 30)
        self.assertTrue(self.libraryTrue.check_reservation("Richard", "book1", 25))
        self.assertTrue(self.libraryTrue.check_reservation("Richard", "book1", 30))
        self.assertTrue(self.libraryTrue.check_reservation("Richard", "book1", 21))
        self.assertFalse(self.libraryFalse.check_reservation("Richard", "book1", 20))

    def test_change_reservation(self):
        self.assertEqual(self.libraryFalse.change_reservation("Richard", "book", 25, "Tomas"), (False, "not_relevant"))
        self.assertEqual(self.libraryTrue.change_reservation("Richard", "book", 25, "Fero"), (False, "user"))
        self.assertEqual(self.libraryTrue.change_reservation("Richard", "book1", 25, "Tomas"), (True, ""))

if __name__ == '__main__':
    unittest.main()
