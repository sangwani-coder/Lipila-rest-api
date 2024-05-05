"""
Helper Functions
"""
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_list_or_404
from business.models import BusinessUser
from patron.models import CreatorUser, Patron
from lipila.models import (
    ContactInfo, HeroInfo, CustomerMessage, UserTestimonial, AboutInfo)
from django.contrib.auth.models import User
from functools import wraps
from django.test import TestCase


def get_lipila_contact_info() -> dict:
    """ Gets the lipila contact info and
    returns a dict object.
    """
    data = {'contact':''}
    try:
        contact_info = ContactInfo.objects.latest()
        data['contact'] = contact_info
    except ContactInfo.DoesNotExist:
        pass
    return data


def get_user_emails():
    """
    Get all user messages.
    """
    data = {'user_messages':''}
    try:
        user_messages = CustomerMessage.objects.all()
        data['user_messages'] = user_messages
    except CustomerMessage.DoesNotExist:
        pass
    return data


def get_lipila_index_page_info() -> dict:
    """
    Get the index page info.
    """
    data = {'lipila':''}
    try:
        lipila_index_info = HeroInfo.objects.latest()
        data['lipila'] = lipila_index_info
    except HeroInfo.DoesNotExist:
        pass
    return data

def get_lipila_about_info() -> dict:
    """
    Get the about info.
    """
    data = {'about':''}
    try:
        lipila_about_info = AboutInfo.objects.latest()
        data['about'] = lipila_about_info
    except AboutInfo.DoesNotExist:
        pass
    return data

def get_testimonials() -> dict:
    """
    Get testimonials and return a dict object.
    """
    data = {'testimonials':''}
    try:
        results = UserTestimonial.objects.all()
        data['testimonials'] = results
    except UserTestimonial.DoesNotExist:
        pass
    return data


def get_patrons(user: str):
    """
    Gets a users patrons

    Args:
        user_type: The user category
        user: The user object to get patrons for.

    Returns:
        A patron_object.
    """
    try:
        creator_object = User.objects.filter(creator=user)
        return creator_object.count()
    except Patron.DoesNotExist:
        return 0


def get_user_object(user: str):
    """
    Gets a user object from the database.

    Args:
        user: The user object to check.

    Returns:
        A user_object instance(BusinessUser or CreatorUser or LipilauSE or)
         otherwise returns 404.
    """
    data = {}
    try:
        user_object = User.objects.get(username=user)
        return user_object
    except User.DoesNotExist:
        return None


def check_if_user_is_patron(user, creator):
    """Checks if a user is already a patron of a specific creator.

    Args:
        user: A User object representing the user to check.
        creator: A User object representing the creator to check against.

    Returns:
        True if the user is a patron of the given creator, False otherwise.
    """

    try:
        # Check if the user has a corresponding Patron instance
        patron = user.patron

    except User.DoesNotExist:
        # Handle the case where the user doesn't exist
        return False

    except Patron.DoesNotExist:
        # Handle the case where the user exists but doesn't have a Patron
        return False

    else:
        # If the user has a Patron, check if it's associated with the creator
        return patron.patron.filter(pk=creator.pk).exists()


def apology(request, data=None, user=None):
    """
    Renders a custom error page with the provided data.

    Args:
        request: The Django request object.
        data: A dictionary of data variables to pass to the template.

    Returns:
        An HttpResponseNotFound object with the rendered 404 template.
    """

    template_name = 'pages_error.html'

    if data is None:
        data = {}

    if data['status'] == 404:
        return HttpResponseNotFound(
            render(request, template_name, data)
        )
    elif data['status'] == 400:
        return HttpResponseBadRequest(
            render(request, template_name, data)
        )
