class MsgCreate:
    def log_reserv_init(fn):
        @Log.logger
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            Log.message = F'Created a reservation with id {self._id} of {self._book}'
            Log.message += F' from {self._from} to {self._to} for {self._for}.'
            return result
        return wrapper

    def log_reserv_overlap(fn):
        @Log.logger
        def wrapper(self, other):
            result = fn(self, other)
            str = 'do'
            if not result:
                str = 'do not'
            Log.message = F'Reservations {self._id} and {other._id} {str} overlap'
            return result
        return wrapper

    def log_reserv_includes(fn):
        @Log.logger
        def wrapper(self, date):
            result = fn(self, date)
            str = 'includes'
            if not result:
                str = 'does not include'
            Log.message = F'Reservation {self._id} {str} {date}'
            return result
        return wrapper

    def log_reserv_identify(fn):
        @Log.logger
        def wrapper(self, date, book, for_):
            result = fn(self, date, book, for_)
            if book != self._book: 
                Log.message = F'Reservation {self._id} reserves {self._book} not {book}.'
                return result
            if for_!=self._for:
                Log.message = F'Reservation {self._id} is for {self._for} not {for_}.'
                return result
            if not self.includes(date):
                Log.message = F'Reservation {self._id} is from {self._from} to {self._to} which '
                Log.message += F'does not include {date}.'
                return result
            Log.message = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
            return result
        return wrapper 

    def log_reserv_change_for(fn):
        @Log.logger
        def wrapper(self, for_):
            result = fn(self, for_)
            Log.message = F'Reservation {self._id} moved from {self._for} to {for_}'
            return result
        return wrapper

    def log_library_init(fn):
        @Log.logger
        def wrapper(self):
            result = fn(self)
            Log.message = F'Library created.'
            return result
        return wrapper 

    def log_library_add_user(fn):
        @Log.logger
        def wrapper(self, name):
            result = fn(self, name)
            if not result:
                Log.message = F'User not created, user with name {name} already exists.'
                return result 
            Log.message = F'User {name} created.'
            return result
        return wrapper

    def log_library_add_book(fn):
        @Log.logger
        def wrapper(self, name):
            result = fn(self, name)
            Log.message = F'Book {name} added. We have {self._books[name]} coppies of the book.'
            return result
        return wrapper



class Log:
    def logger(fn):
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            print(Log.message)
            return result
        return wrapper
