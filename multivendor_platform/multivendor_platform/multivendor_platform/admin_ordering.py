"""
Custom ordering for Django admin apps and models.

This module monkey-patches ``AdminSite.get_app_list`` to enforce
the desired grouping and ordering in the Django admin index and sidebar.

No external packages are used. Import this module once (e.g. from urls.py)
to activate the custom ordering on the default admin site.
"""

from typing import Any, Dict, List

from django.contrib.admin import AdminSite


# Desired app order by app_label
APP_ORDER: List[str] = [
    "products",
    "blog",
    "chat",
    "orders",
    "sms_newsletter",  # SMS newsletter for sellers
    "authtoken",  # rest_framework.authtoken
    "auth",
    "users",
    "pages",
]

APP_ORDER_INDEX: Dict[str, int] = {label: idx for idx, label in enumerate(APP_ORDER)}


# Desired model order per app by object_name (model class name)
MODEL_ORDER: Dict[str, List[str]] = {
    # Products group
    "products": [
        "Product",
        "Subcategory",
        "Category",
        "Department",
        "LabelManagementProxy",
        "LabelComboSeoPage",
        "LabelGroup",
        "Label",
        "ProductComment",
        "CategoryRequest",
    ],
    # Blog Management
    "blog": [
        "BlogCategory",
        "BlogComment",
        "BlogPost",
    ],
    # Chat System
    "chat": [
        "ChatMessage",
        "ChatParticipant",
        "ChatRoom",
        "GuestSession",
        "TypingStatus",
    ],
    # Orders
    "orders": [
        "Order",
    ],
    # SMS Newsletter
    "sms_newsletter": [
        "Seller",
    ],
    # Auth Token
    "authtoken": [
        "Token",
    ],
    # Authentication and Authorization
    "auth": [
        "Group",
        "User",
    ],
    # Users
    "users": [
        "BuyerProfile",
        "SupplierContactMessage",
        "OTP",
        "SupplierPortfolioItem",
        "ProductReview",
        "SellerAd",
        "SupplierComment",
        "VendorProfile",
        "Supplier",
        "SupplierTeamMember",
        "UserActivity",
        "UserProfile",
    ],
    # Static pages
    "pages": [
        "Redirect",
        "ContactPage",
        "AboutPage",
    ],
}


def _sort_models_for_app(app_dict: Dict[str, Any]) -> None:
    """
    Sort the ``models`` list inside a single app dict in-place
    according to MODEL_ORDER, falling back to alphabetical order.
    """
    app_label = app_dict.get("app_label")
    models: List[Dict[str, Any]] = app_dict.get("models", [])

    order_list = MODEL_ORDER.get(app_label, [])
    order_index = {name: idx for idx, name in enumerate(order_list)}
    base = len(order_list)

    def model_key(model: Dict[str, Any]) -> Any:
        object_name = model.get("object_name") or ""
        name = model.get("name") or ""
        if object_name in order_index:
            return (0, order_index[object_name])
        # Put unspecified models after the ordered ones, alphabetically
        return (1, name.lower())

    models.sort(key=model_key)


def _sort_apps(app_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return a new list of apps sorted according to APP_ORDER,
    with any remaining apps ordered alphabetically.
    """

    def app_key(app: Dict[str, Any]) -> Any:
        label = app.get("app_label") or ""
        name = app.get("name") or ""
        if label in APP_ORDER_INDEX:
            return (0, APP_ORDER_INDEX[label])
        # Unspecified apps go after the ordered ones, alphabetically
        return (1, name.lower())

    # First, sort models inside each app
    for app in app_list:
        _sort_models_for_app(app)

    # Then sort the apps themselves
    return sorted(app_list, key=app_key)


_original_get_app_list = AdminSite.get_app_list


def custom_get_app_list(self: AdminSite, request, app_label=None):
    """
    Replacement for AdminSite.get_app_list that applies custom ordering.
    Supports both full app list and single app list views.
    """
    app_list = list(_original_get_app_list(self, request, app_label))
    return _sort_apps(app_list)


# Apply monkey-patch so that the default admin site uses the custom ordering.
AdminSite.get_app_list = custom_get_app_list


