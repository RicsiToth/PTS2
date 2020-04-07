class LOG:
    def log_reserv_init(fn):
        @LOG._logger
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            self.message = F'Created a reservation with id {self._id} of {self._book}'
            self.message += F' from {self._from} to {self._to} for {self._for}.'
            return result
        return wrapper

    def log_reserv_overlap(fn):
        @LOG._logger
        def wrapper(self, other):
            result = fn(self, other)
            str = 'do'
            if not result:
                str = 'do not'
            self.message = F'Reservations {self._id} and {other._id} {str} overlap'
            return result
        return wrapper

    def log_reserv_includes(fn):
        @LOG._logger
        def wrapper(self, date):
            result = fn(self, date)
            str = 'includes'
            if not result:
                str = 'does not include'
            self.message = F'Reservation {self._id} {str} {date}'
            return result
        return wrapper

     def log_reserv_identify(fn):
        @LOG._logger
        def wrapper(self, date, book, for_):
            result = fn(self, date, book, for_)
            if book != self._book: 
                self.message = F'Reservation {self._id} reserves {self._book} not {book}.'
                return result
            if for_!=self._for:
                self.message = F'Reservation {self._id} is for {self._for} not {for_}.'
                return result
            if not self.includes(date):
                self.message = F'Reservation {self._id} is from {self._from} to {self._to} which '
                self.message += F'does not include {date}.'
                return result
            self.message = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
            return result
        return wrapper 

    def log_reserv_change_for(fn):
        @LOG._logger
        def wrapper(self, for_):
            result = fn(self, for_)
            self.message = F'Reservation {self._id} moved from {self._for} to {for_}'
            return result
        return wrapper      


    
    def _logger(fn):
        def wrapper(self, *arg, **kwarg):
            result = fn(self, *arg, **kwarg)
            print(self.message)
            return result
        return wrapper
