"""Kisaan Voice v2 core: dictionaries, dual encoding, segment counting."""
from .dictionary import load_dictionary, select_dictionary, validate, Dictionary, DictionaryError
from .encoding import (encode_sms, decode_sms, encode_binary, decode_binary, EncodingError)
from .segments import count_segments, is_gsm7
from .templates import validate_and_render, SlotError
__version__ = "2.0.0"
__all__ = ["load_dictionary", "select_dictionary", "validate", "Dictionary", "DictionaryError",
           "encode_sms", "decode_sms", "encode_binary", "decode_binary", "EncodingError",
           "count_segments", "is_gsm7", "validate_and_render", "SlotError"]
