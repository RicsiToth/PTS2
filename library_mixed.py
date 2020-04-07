from itertools import count
from logger import MsgCreate

class Reservation(object):
    _ids = count(0)
    
    @MsgCreate.log_reserve_init
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0

    @MsgCreate.log_reserve_overlap
    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from 
                 and self._from <= other._to)

    @MsgCreate.log_reserve_includes        
    def includes(self, date):
        return (self._from <= date <= self._to)       
    
    @MsgCreate.log_reserve_identify    
    def identify(self, date, book, for_):
        if book != self._book: 
            return False
        if for_!=self._for:
            return False
        if not self.includes(date):
            return False
        return True        
    
    @MsgCreate.log_reserve_change_for    
    def change_for(self, for_):
        self._for = for_
        

class Library(object):
    
    @MsgCreate.log_library_init
    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from
    
    @MsgCreate.log_library_add_user            
    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    @MsgCreate.log_library_add_book 
    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    @MsgCreate.log_library_reserve
    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return False
        if date_from > date_to:
            return False
        if book_count == 0:
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return False
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        return True

    @MsgCreate.log_library_check_reserve
    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])       

    @MsgCreate.log_library_change_reserve
    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)]
        if not relevant_reservations:        
            return False
        if new_user not in self._users:
            return False      
        relevant_reservations[0].change_for(new_user)
        return True  
