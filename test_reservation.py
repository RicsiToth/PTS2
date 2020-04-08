import unittest
from library_mixed import Reservation
from itertools import count

class TestReservation(unittest.TestCase):

    def setUp(self):
        Reservation._ids = count(0)
        self.res1 = Reservation(20, 25, "First", "Richard")
        
    def test_init(self):
        self.assertEqual(self.res1._id, 0)
        self.assertEqual(self.res1._from, 20)
        self.assertEqual(self.res1._to, 25)
        self.assertEqual(self.res1._book, "First")
        self.assertEqual(self.res1._for, "Richard")
        self.assertEqual(self.res1._changes, 0)

    def test_overlapping(self):
        self.assertTrue(self.res1.overlapping(Reservation(15, 22, "First", "tmp")))
        self.assertTrue(self.res1.overlapping(Reservation(15, 20, "First", "tmp")))
        self.assertTrue(self.res1.overlapping(Reservation(25, 30, "First", "tmp")))
        self.assertFalse(self.res1.overlapping(Reservation(5, 10, "First", "tmp")))
        self.assertFalse(self.res1.overlapping(Reservation(15, 22, "Second", "tmp")))
  
    def test_includes(self):
        self.assertTrue(self.res1.includes(20))
        self.assertTrue(self.res1.includes(25))
        self.assertTrue(self.res1.includes(22))
        self.assertFalse(self.res1.includes(26))
    
    def test_identify(self):
        self.assertTrue(self.res1.identify(20, "First", "Richard"))
        self.assertFalse(self.res1.identify(20, "Second", "Richard"))
        self.assertFalse(self.res1.identify(20, "First", "Fero"))
        self.assertFalse(self.res1.identify(19, "First", "Richard"))

    def test_change_for(self):
        self.res1.change_for("Peto")
        self.assertEqual(self.res1._for, "Peto")
        self.assertEqual(self.res1._changes, 1)

        self.res1.change_for("Fero")
        self.assertEqual(self.res1._for, "Fero")
        self.assertEqual(self.res1._changes, 2)
    

if __name__ == '__main__':
    unittest.main()
