========
 Themes
========

Sigal themes are created using the `Jinja2`_ templating system.

.. _Jinja2: http://jinja.pocoo.org/docs/

Bundled themes
~~~~~~~~~~~~~~

Sigal comes with three themes, located in the ``sigal/themes`` folder:

**colorbox**:
    `source <http://www.jacklmoore.com/colorbox>`__, `demo
    <http://saimon.org/sigal-demo/colorbox/>`__. This theme uses a Swipe plugin
    to browse pictures on touch devices.

**galleria**:
    `source <http://galleria.io/>`__, `demo
    <http://saimon.org/sigal-demo/galleria/>`__. This theme is based on the
    classic theme, pictures can be browsed with left/right keys, fullscreen
    support is available with the `f` key, and a map can be shown with the `m`
    key if the ``show_map`` setting is True. The ``leaflet_provider`` setting
    can be used to customize the tile provider (using `Leaflet-providers
    <https://github.com/leaflet-extras/leaflet-providers#providers>`_).

**photoswipe**:
    `source <http://photoswipe.com/>`__, `demo
    <http://saimon.org/sigal-demo/photoswipe/>`__.

The ``themes`` folder also includes a ``default`` theme. This theme cannot be
used on its own, instead, it contains Jinja2 templates that are used by the
bundled themes to enable functionality such as the feeds and ZIP gallery
plugins, as well as settings such as Google Analytics.

Creating a theme
~~~~~~~~~~~~~~~~

Sigal requires the following two templates in order to generate a gallery.
These templates must be located in ``THEME_DIR/templates``:

- ``album_list.html``: Generates the album list, if you have multiple albums
- ``album.html``: Generates each individual album page

Themes may also include static content such as CSS and JavaScript by placing
this content in the ``THEME_DIR/static`` folder. You can then access this
content in your template by using the ``theme.url`` variable.

Custom themes may also include the templates available in the ``default``
theme.

Variables
~~~~~~~~~

You can use the following variables in your template:

``album``
    The current album that is rendered in the HTML file, represented by an
    :class:`~sigal.gallery.Album` object.  ``album.medias`` contains the list
    of all medias in the album (represented by the
    :class:`~sigal.gallery.Image` and :class:`~sigal.gallery.Video` objects,
    inherited from :class:`~sigal.gallery.Media`).

``index_title``
    Name of the index. This is either the directory name or the title specified
    in the ``index.md`` of the ``source`` directory.

``settings``
    The entire dictionary from ``sigal.conf.py``.

``sigal_link``
    URL to the Sigal homepage.

``theme.name``, ``theme.url``
    Name and url of the currently used theme.

Filters
~~~~~~~

You can define custom jinja filters for your template by creating a ``filters.py`` script
at the root of your template directory.

This script will then be imported and all defined functions will be available as jinja filters
with the same names in your templates.

Documentation of sigal's main classes
-------------------------------------

.. autoclass:: sigal.gallery.Album
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: sigal.gallery.Media
   :members:
   :undoc-members:

.. autoclass:: sigal.gallery.Image
   :members:
   :undoc-members:
   :inherited-members:

.. autoclass:: sigal.gallery.Video
   :members:
   :undoc-members:
   :inherited-members:

.. _simple-exif-data:

Simpler EXIF data output
~~~~~~~~~~~~~~~~~~~~~~~~

Because the tags in the ``media.raw_exif`` dictionary are a little bit
cumbersome to use, some common tags are extracted and formatted for easy use in
templates. If available, you can use:

``media.exif.iso``
    The ISO speed rating.

``media.exif.focal``
    The focal length, formatted as a decimal number.

``media.exif.exposure``
    The exposure time formatted as a fractional number, e.g. "1/500".

``media.exif.fstop``
    The aperture value given as an F-number and formatted as a decimal.

``media.exif.datetime``
    The time the image was *taken*. It is formatted with the
    ``datetime_format`` setting, which is ``%c`` by default.
    See Python's `datetime documentation`_ for a list of all possible values.

``media.exif.dateobj``
    The time the image was *taken*. It is a datetime object, that can be
    formatted with ``strftime``:

    .. code-block:: jinja

        {% if media.exif.dateobj %}
            {{ media.exif.dateobj.strftime('%A, %d. %B %Y') }}
        {% endif %}

    This will output something like "Monday, 25. June 2013", depending on your
    locale.

``media.exif.gps``
    If not None, the dict contains two keys ``lat`` and ``lon`` denoting the
    GPS coordinates of the location where the image was taken. ``lat`` will
    always be referenced to the north pole whereas ``lon`` will be referenced to
    east to the prime meridan. To provide a link on an OpenStreetMap you could
    write a template like this:

    .. code-block:: jinja

        {% if media.exif.gps %}
            <a href="https://www.openstreetmap.org/?mlat={{
                media.exif.gps.lat }}&mlon={{
                media.exif.gps.lon }}#map=18/{{
                media.exif.gps.lat }}/{{
                media.exif.gps.lon }}">Go to location (OpenStreetMap)</a>
        {% endif %}


.. _datetime documentation: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
