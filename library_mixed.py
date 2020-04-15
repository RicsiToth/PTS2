from itertools import count

class Reservation(object):
    _ids = count(0)
    
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from 
                 and self._from <= other._to)
  
    def includes(self, date):
        return (self._from <= date <= self._to)       
    
    def identify(self, date, book, for_):
        if book != self._book: 
            return (False, "book")
        if for_!=self._for:
            return (False, "for")
        if not self.includes(date):
            return (False, "date")
        return (True, "")        
  
    def change_for(self, for_):
        self._changes += 1
        self._for = for_


class Reservation_Messages(Reservation): 
    def __init__(self, from_, to, book, for_):
        super().__init__(from_, to, book, for_)
        message = F'Created a reservation with id {self._id} of {self._book}'
        message += F' from {self._from} to {self._to} for {self._for}.'

    def overlapping(self, other):
        result = super().overlapping(other)
        str = 'do'
        if not result:
            str = 'do not'
        message = F'Reservations {self._id} and {other._id} {str} overlap'
        return result
     
    def includes(self, date):
        result = super().includes(date)
        str = 'includes'
        if not result:
            str = 'does not include'
        message = F'Reservation {self._id} {str} {date}'
        return result       

    def identify(self, date, book, for_):
        result = super().identify(date, book, for_)
        if result[0]:
            message = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
        else:
            if result[1] == "book": 
                message = F'Reservation {self._id} reserves {self._book} not {book}.'
            elif result[1] == "for":
                message = F'Reservation {self._id} is for {self._for} not {for_}.'
            elif result[1] == "date":
                message = F'Reservation {self._id} is from {self._from} to {self._to} which '
                message += F'does not include {date}.'
        return result      
     
    def change_for(self, for_):
        old_for = self._for
        result = super().change_for(for_)
        message = F'Reservation {self._id} moved from {old_for} to {for_}'
        return result


class Reservation_Logging_Messages(ReservationMessages):
    def __init__(self, from_, to, book, for_):
        super().__init__(from_, to, book, for_)
        print(super().message)

    def overlapping(self, other):
        result = super().overlapping(other)
        print(super().message)
        return result
     
    def includes(self, date):
        result = super().includes(date)
        print(super().message)
        return result       

    def identify(self, date, book, for_):
        result = super().identify(date, book, for_)
        print(super().message)
        return result      
     
    def change_for(self, for_):
        result = super().change_for(for_)
        print(super().message)
        return result


@enable_logging
class Library(object):
   
    @MsgCreate.msg_library_init
    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from
  
    @MsgCreate.msg_library_add_user            
    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    @MsgCreate.msg_library_add_book 
    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    @MsgCreate.msg_library_reserve
    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return -1
        if date_from > date_to:
            return -1
        if book_count == 0:
            return -1
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return -1
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        return desired_reservation._id

    @MsgCreate.msg_library_check_reserve
    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])       

    @MsgCreate.msg_library_change_reserve
    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)]
        if not relevant_reservations:        
            return False
        if new_user not in self._users:
            return False      
        relevant_reservations[0].change_for(new_user)
        return True  
