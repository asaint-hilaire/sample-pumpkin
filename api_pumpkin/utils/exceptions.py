class DoesNotExist(Exception):
    def __str__(self):
        return 'Object does not exist'
