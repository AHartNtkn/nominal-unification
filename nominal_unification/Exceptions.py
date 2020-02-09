# Unification related exceptions.
class AAMismatchError(Exception): # (Clo Atom) (Clo Atom)
   """Raised when ..."""
   pass

class NameCaptureError(Exception): # Atom BinderMap
   """Raised when ..."""
   pass

class NoMatchingBinderError(Exception): # Int BinderMap
   """Raised when ..."""
   pass

class EEMismatchError(Exception): # (Clo Expr) (Clo Expr)
   """Raised when ..."""
   pass