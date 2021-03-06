class MsgCreate:
    def msg_reserve_init(fn):
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            Log.message = F'Created a reservation with id {self._id} of {self._book}'
            Log.message += F' from {self._from} to {self._to} for {self._for}.'
            return result
        return wrapper

    def msg_reserve_overlap(fn):
        def wrapper(self, other):
            result = fn(self, other)
            str = 'do'
            if not result:
                str = 'do not'
            Log.message = F'Reservations {self._id} and {other._id} {str} overlap'
            return result
        return wrapper

    def msg_reserve_includes(fn):
        def wrapper(self, date):
            result = fn(self, date)
            str = 'includes'
            if not result:
                str = 'does not include'
            Log.message = F'Reservation {self._id} {str} {date}'
            return result
        return wrapper

    def msg_reserve_identify(fn):
        def wrapper(self, date, book, for_):
            result = fn(self, date, book, for_)
            if result:
                Log.message = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
            else:
                if book != self._book: 
                    Log.message = F'Reservation {self._id} reserves {self._book} not {book}.'
                elif for_!=self._for:
                    Log.message = F'Reservation {self._id} is for {self._for} not {for_}.'
                elif not self.includes(date):
                    Log.message = F'Reservation {self._id} is from {self._from} to {self._to} which '
                    Log.message += F'does not include {date}.'
            return result
        return wrapper 

    def msg_reserve_change_for(fn):
        def wrapper(self, for_):
            tmp = self._for
            result = fn(self, for_)
            Log.message = F'Reservation {self._id} moved from {tmp} to {for_}'
            return result
        return wrapper

    def msg_library_init(fn):
        def wrapper(self):
            result = fn(self)
            Log.message = F'Library created.'
            return result
        return wrapper 

    def msg_library_add_user(fn):
        def wrapper(self, name):
            result = fn(self, name)
            if result:
                Log.message = F'User {name} created.'
            else:
                Log.message = F'User not created, user with name {name} already exists.'
            return result
        return wrapper

    def msg_library_add_book(fn):
        def wrapper(self, name):
            result = fn(self, name)
            Log.message = F'Book {name} added. We have {self._books[name]} coppies of the book.'
            return result
        return wrapper

    def msg_library_reserve(fn):
        def wrapper(self, user, book, date_from, date_to):
            result = fn(self, user, book, date_from, date_to)
            if result >= 0:
                Log.message = F'Reservation {result} included.'
                return result
            else:
                Log.message = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '
                if user not in self._users:
                    Log.message += F'User does not exist.'
                elif date_from > date_to:
                    Log.message += F'Incorrect dates.'
                elif self._books.get(book, 0) == 0:
                    Log.message += F'We do not have that book.'
                else:
                    Log.message += F'We do not have enough books.'
                return result
        return wrapper

    def msg_library_check_reserve(fn):
        def wrapper(self, user, book, date):
            result = fn(self, user, book, date)
            str = 'exists'
            if not result:
                str = 'does not exist'
            Log.message = F'Reservation for {user} of {book} on {date} {str}.'
            return result
        return wrapper

    def msg_library_change_reserve(fn):
        def wrapper(self, user, book, date, new_user):
            result = fn(self, user, book, date, new_user)
            if result:
                Log.message = F'Reservation for {user} of {book} on {date} changed to {new_user}.'
            else:
                if new_user not in self._users:
                    Log.message = F'Cannot change the reservation as {new_user} does not exist.'
                else:
                    Log.message = F'Reservation for {user} of {book} on {date} does not exist.'
            return result
        return wrapper


class Log:
    message = "" 

    def logger(fn):
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            print(Log.message)
            return result
        return wrapper

def enable_logging(cls):
    for name, value in vars(cls).items():
        if callable(value):
            setattr(cls, name, Log.logger(value))
    return cls
