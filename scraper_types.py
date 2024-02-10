from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


@dataclass
class Attributes:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        return Attributes()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class Completion:
    text: str
    relevance: float

    @staticmethod
    def from_dict(obj: Any) -> 'Completion':
        assert isinstance(obj, dict)
        text = from_str(obj.get("text"))
        relevance = from_float(obj.get("relevance"))
        return Completion(text, relevance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_str(self.text)
        result["relevance"] = to_float(self.relevance)
        return result


@dataclass
class Variant:
    key: str
    ticket: str
    attributes: Dict[str, List[str]]

    @staticmethod
    def from_dict(obj: Any) -> 'Variant':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        ticket = from_str(obj.get("ticket"))
        attributes = from_dict(lambda x: from_list(from_str, x), obj.get("attributes"))
        return Variant(key, ticket, attributes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["ticket"] = from_str(self.ticket)
        result["attributes"] = from_dict(lambda x: from_list(from_str, x), self.attributes)
        return result


@dataclass
class Product:
    key: str
    ticket: str
    variants: List[Variant]
    attributes: Dict[str, List[str]]

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        assert isinstance(obj, dict)
        key = from_str(obj.get("key"))
        ticket = from_str(obj.get("ticket"))
        variants = from_list(Variant.from_dict, obj.get("variants"))
        attributes = from_dict(lambda x: from_list(from_str, x), obj.get("attributes"))
        return Product(key, ticket, variants, attributes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["key"] = from_str(self.key)
        result["ticket"] = from_str(self.ticket)
        result["variants"] = from_list(lambda x: to_class(Variant, x), self.variants)
        result["attributes"] = from_dict(lambda x: from_list(from_str, x), self.attributes)
        return result


@dataclass
class Autocomplete:
    name: str
    ticket: str
    path: str
    description: str
    display_name: str
    attributes: Attributes
    result_type: str
    completions: Optional[List[Completion]] = None
    corrections: Optional[List[Any]] = None
    products: Optional[List[Product]] = None
    phrases: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Autocomplete':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        ticket = from_str(obj.get("ticket"))
        path = from_str(obj.get("path"))
        description = from_str(obj.get("description"))
        display_name = from_str(obj.get("displayName"))
        attributes = Attributes.from_dict(obj.get("attributes"))
        result_type = from_str(obj.get("resultType"))
        completions = from_union([lambda x: from_list(Completion.from_dict, x), from_none], obj.get("completions"))
        corrections = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("corrections"))
        products = from_union([lambda x: from_list(Product.from_dict, x), from_none], obj.get("products"))
        phrases = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("phrases"))
        return Autocomplete(name, ticket, path, description, display_name, attributes, result_type, completions, corrections, products, phrases)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["ticket"] = from_str(self.ticket)
        result["path"] = from_str(self.path)
        result["description"] = from_str(self.description)
        result["displayName"] = from_str(self.display_name)
        result["attributes"] = to_class(Attributes, self.attributes)
        result["resultType"] = from_str(self.result_type)
        if self.completions is not None:
            result["completions"] = from_union([lambda x: from_list(lambda x: to_class(Completion, x), x), from_none], self.completions)
        if self.corrections is not None:
            result["corrections"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.corrections)
        if self.products is not None:
            result["products"] = from_union([lambda x: from_list(lambda x: to_class(Product, x), x), from_none], self.products)
        if self.phrases is not None:
            result["phrases"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.phrases)
        return result


@dataclass
class Welcome:
    autocomplete: List[Autocomplete]
    non_product_suggestions: List[Autocomplete]
    product_suggestions: List[Autocomplete]
    top_searches: List[Autocomplete]
    did_you_mean: List[Autocomplete]

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        autocomplete = from_list(Autocomplete.from_dict, obj.get("autocomplete"))
        non_product_suggestions = from_list(Autocomplete.from_dict, obj.get("nonProductSuggestions"))
        product_suggestions = from_list(Autocomplete.from_dict, obj.get("productSuggestions"))
        top_searches = from_list(Autocomplete.from_dict, obj.get("topSearches"))
        did_you_mean = from_list(Autocomplete.from_dict, obj.get("didYouMean"))
        return Welcome(autocomplete, non_product_suggestions, product_suggestions, top_searches, did_you_mean)

    def to_dict(self) -> dict:
        result: dict = {}
        result["autocomplete"] = from_list(lambda x: to_class(Autocomplete, x), self.autocomplete)
        result["nonProductSuggestions"] = from_list(lambda x: to_class(Autocomplete, x), self.non_product_suggestions)
        result["productSuggestions"] = from_list(lambda x: to_class(Autocomplete, x), self.product_suggestions)
        result["topSearches"] = from_list(lambda x: to_class(Autocomplete, x), self.top_searches)
        result["didYouMean"] = from_list(lambda x: to_class(Autocomplete, x), self.did_you_mean)
        return result


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)


def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)
