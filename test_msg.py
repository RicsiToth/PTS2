import unittest
from itertools import count
from library_mixed import Reservation_Messages, Library_Messages, Reservation

class TestReserveMsg(unittest.TestCase):
    
    def setUp(self):
        Reservation._ids = count(0)
        self.reserv = Reservation_Messages(20, 25, "First", "Richard")
 
    def test_reserve_init(self):
        self.assertEqual(self.reserv._message, "Created a reservation with id 0 of First from 20 to 25 for Richard.")

    def test_reserve_includes_message_does_include(self):
        self.reserv.includes(23)
        self.assertEqual(self.reserv._message, "Reservation 0 includes 23")

    def test_reserve_includes_message_does_not_include(self):
        self.reserv.includes(30)
        self.assertEqual(self.reserv._message, "Reservation 0 does not include 30")

    def test_reserve_overlap_do(self):
        reserv2 = Reservation_Messages(10, 20, "First", "Tomas")
        self.reserv.overlapping(reserv2)
        self.assertEqual(self.reserv._message, "Reservations 0 and 1 do overlap")

    def test_reserve_overlap_do_not(self):
        reserv2 = Reservation_Messages(10, 15, "First", "Tomas")
        self.reserv.overlapping(reserv2)
        self.assertEqual(self.reserv._message, "Reservations 0 and 1 do not overlap")

    def test_reserve_change_for(self):
        self.reserv.change_for("Tomas")
        self.assertEqual(self.reserv._message, "Reservation 0 moved from Richard to Tomas")

    def test_reserve_identify_bad_name(self):
        self.reserv.identify(23, "First", "Tomas")
        self.assertEqual(self.reserv._message, "Reservation 0 is for Richard not Tomas.")

    def test_reserve_identify_bad_book(self):
        self.reserv.identify(23, "Fist", "Richard")
        self.assertEqual(self.reserv._message, "Reservation 0 reserves First not Fist.")

    def test_reserve_identify_bad_date(self):
        self.reserv.identify(40, "First", "Richard")
        self.assertEqual(self.reserv._message, "Reservation 0 is from 20 to 25 which does not include 40.")

    def test_reserve_identify_good(self):
        self.reserv.identify(23, "First", "Richard")
        self.assertEqual(self.reserv._message, "Reservation 0 is valid Richard of First on 23.")

class TestLibraryMsg(unittest.TestCase):
    
    def setUp(self):
        self.library = Library_Messages()
        Reservation._ids = count(0)

    def test_library_init(self):
        self.assertEqual(self.library._message, "Library created.")

    def test_library_add_user_existing(self):
        self.library.add_user("Richard")
        self.library.add_user("Richard")
        self.assertEqual(self.library._message, "User not created, user with name Richard already exists.")

    def test_library_add_user_not_existing(self):
        self.library.add_user("Richard")
        self.assertEqual(self.library._message, "User Richard created.")

    def test_library_add_book(self):
        self.library.add_book("First")
        self.assertEqual(self.library._message, "Book First added. We have 1 coppies of the book.")

    def test_library_reserve_book_not_a_user(self):
        self.library.reserve_book("Richard", "First", 20, 25)
        self.assertEqual(self.library._message, "We cannot reserve book First for Richard from 20 to 25. User does not exist.")

    def test_library_reserve_book_mixed_dates(self):
        self.library.add_user("Richard")
        self.library.reserve_book("Richard", "First", 25, 20)
        self.assertEqual(self.library._message, "We cannot reserve book First for Richard from 25 to 20. Incorrect dates.")

    def test_library_reserve_book_no_book(self):
        self.library.add_user("Richard")
        self.library.reserve_book("Richard", "First", 20, 25)
        self.assertEqual(self.library._message, "We cannot reserve book First for Richard from 20 to 25. We do not have that book.")

    def test_library_reserve_book_not_enough_books(self):
        self.library.add_user("Richard")
        self.library.add_user("Tomas")
        self.library.add_book("First")
        self.library.reserve_book("Richard", "First", 20, 25)
        self.library.reserve_book("Tomas", "First", 23, 28)
        self.assertEqual(self.library._message, "We cannot reserve book First for Tomas from 23 to 28. We do not have enough books.")

    def test_library_reserve_good(self):
        self.library.add_user("Richard")
        self.library.add_book("First")
        self.library.reserve_book("Richard", "First", 20, 25)
        self.assertEqual(self.library._message, "Reservation 0 included.")

    def test_library_check_reservationk(self):
        self.library.add_user("Richard")
        self.library.reserve_book("Richard", "First", 20, 25)
        self.assertEqual(self.library._message, "We cannot reserve book First for Richard from 20 to 25. We do not have that book.")


if __name__ == '__main__':
    unittest.main()
