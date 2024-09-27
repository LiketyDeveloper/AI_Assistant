import sys

from bot.database.models import Users, Operators, register_models

# Type >> python models.py <model_name1> <model_name2> ... <model_nameN>
register_models([getattr(sys.modules[__name__], model) for model in sys.argv[1:]] if sys.argv[1:] else [Users, Operators])

print("Models successfully registered")