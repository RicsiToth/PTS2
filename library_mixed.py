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
        self._message = F'Created a reservation with id {self._id} of {self._book}'
        self._message += F' from {self._from} to {self._to} for {self._for}.'

    def overlapping(self, other):
        result = super().overlapping(other)
        str = 'do'
        if not result:
            str = 'do not'
        self._message = F'Reservations {self._id} and {other._id} {str} overlap'
        return result
     
    def includes(self, date):
        result = super().includes(date)
        str = 'includes'
        if not result:
            str = 'does not include'
        self._message = F'Reservation {self._id} {str} {date}'
        return result       

    def identify(self, date, book, for_):
        result = super().identify(date, book, for_)
        if result[0]:
            self._message = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
        else:
            if result[1] == "book": 
                self._message = F'Reservation {self._id} reserves {self._book} not {book}.'
            elif result[1] == "for":
                self._message = F'Reservation {self._id} is for {self._for} not {for_}.'
            elif result[1] == "date":
                self._message = F'Reservation {self._id} is from {self._from} to {self._to} which '
                self._message += F'does not include {date}.'
        return result      
     
    def change_for(self, for_):
        old_for = self._for
        result = super().change_for(for_)
        self._message = F'Reservation {self._id} moved from {old_for} to {for_}'
        return result


class Reservation_Logging_Messages(Reservation_Messages):
    def __init__(self, from_, to, book, for_):
        super().__init__(from_, to, book, for_)
        print(super()._message)

    def overlapping(self, other):
        result = super().overlapping(other)
        print(super()._message)
        return result
     
    def includes(self, date):
        result = super().includes(date)
        print(super()._message)
        return result       

    def identify(self, date, book, for_):
        result = super().identify(date, book, for_)
        print(super()._message)
        return result      
     
    def change_for(self, for_):
        result = super().change_for(for_)
        print(super()._message)
        return result


class Library(object):
    def __init__(self, reservations_factory = Reservation):
        self._users = set()
        self._books = {}
        self._reservations = []
        self._reservations_factory = reservations_factory
            
    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return (False, "user")
        if date_from > date_to:
            return (False, "date")
        if book_count == 0:
            return (False, "book_count")
        desired_reservation = self._reservations_factory(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return (False, "reserved")
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from)
        return (True, desired_reservation._id)

    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user)[0] for res in self._reservations])       

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)[0]]
        if not relevant_reservations:        
            return (False, "not_relevant")
        if new_user not in self._users:
            return (False, "user")      
        relevant_reservations[0].change_for(new_user)
        return (True, "")  


class Library_Messages(Library):
    def __init__(self, reservations_factory = Reservation):
        super().__init__(reservations_factory)
        self._message = F'Library created.'
            
    def add_user(self, name):
        result = super().add_user(name)
        if result:
            self._message = F'User {name} created.'
        else:
            self._message = F'User not created, user with name {name} already exists.'
        return result

    def add_book(self, name):
        result = super().add_book(name)
        self._message = F'Book {name} added. We have {self._books[name]} coppies of the book.'
        return result

    def reserve_book(self, user, book, date_from, date_to):
         result = super().reserve_book(user, book, date_from, date_to)
         if result[0]:
            self._message = F'Reservation {result[1]} included.'
         else:
            self._message = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '
            if result[1] == "user":
                self._message += F'User does not exist.'
            elif result[1] == "date":
                self._message += F'Incorrect dates.'
            elif result[1] == "book_count":
                self._message += F'We do not have that book.'
            elif result[1] == "reserved":
                self._message += F'We do not have enough books.'
         return result

    def check_reservation(self, user, book, date):
        result = super().check_reservation(user, book, date)
        str = 'exists'
        if not result:
            str = 'does not exist'
        self._message = F'Reservation for {user} of {book} on {date} {str}.'
        return result       

    def change_reservation(self, user, book, date, new_user):
        result = super().change_reservation(user, book, date, new_user)
        if result[0]:
            self._message = F'Reservation for {user} of {book} on {date} changed to {new_user}.'
        else:
            if result[1] == "user":
                self._message = F'Cannot change the reservation as {new_user} does not exist.'
            elif result[1] == "not_relevant":
                self._message = F'Reservation for {user} of {book} on {date} does not exist.'
        return result 

class Library_Logging_Messages(Library_Messages):
    def __init__(self, reservations_factory = Reservation):
        super().__init__(reservations_factory)
        print(super()._message)
            
    def add_user(self, name):
        result = super().add_user(name)
        print(super()._message)
        return result

    def add_book(self, name):
        result = super().add_book(name)
        print(super()._message)
        return result

    def reserve_book(self, user, book, date_from, date_to):
         result = super().reserve_book(user, book, date_from, date_to)
         print(super()._message)
         return result

    def check_reservation(self, user, book, date):
        result = super().check_reservation(user, book, date)
        print(super()._message)
        return result       

    def change_reservation(self, user, book, date, new_user):
        result = super().change_reservation(user, book, date, new_user)
        print(super()._message)
        return result 
