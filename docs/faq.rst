==================================
 Frequently Asked Questions (FAQ)
==================================

.. contents::

How do I protect the gallery with a password?
---------------------------------------------

Sigal simply generates HTML pages, there is no server process that
could handle a password protection. So the password has to be handled
in your web server (Apache, Nginx, etc). A complete treatise on
webserver configuration is beyond the scope of this document, but, for
example, you may get started with Apache with the `official
documentation
<https://httpd.apache.org/docs/2.2/en/howto/auth.html#gettingitworking>`_.

Here is an example Apache configuration, assuming your gallery was
built in ``/var/www/sigal/_build``::

  <Directory /var/www/sigal/_build>
      AuthType Basic
      AuthName "Restricted Content"
      AuthUserFile /etc/apache2/htpasswd
      Require valid-user
  </Directory>

You will then need to create username/password combinations in the
``/etc/apache2/htpasswd`` using the `htpasswd command
<https://httpd.apache.org/docs/2.4/programs/htpasswd.html>`_.

How do I protect only *some* folders of the gallery with a password?
--------------------------------------------------------------------

This is more complicated than the above. Assuming you want to protect
only the ``foo/`` subdirectory, the following will unfortunately not
do what you expect::

  <Directory /var/www/sigal/_build/foo>
      AuthType Basic
      AuthName "Restricted Content"
      AuthUserFile /etc/apache2/htpasswd
      Require valid-user
  </Directory>

It *will* protect the folder with a password, but, because of the
thumbnails shown on the main page, the web browser will prompt the
user for a password on the parent directory as well, which will
confuse users and is probably not what you want.

The trick is then to whitelist the thumbnail files. Here we'll assume
you will name the thumbnail files ``public.jpg`` and then configure
those files to be visible even in the private section, like so::

  <Directory /var/www/sigal/_build/foo>
      AuthType Basic
      AuthName "Restricted Content"
      AuthUserFile /etc/apache2/htpasswd
      Require valid-user
  </Directory>

  <Files "public.jpg">
      Satisfy any
  </Files>

Then just make sure, through the album information mechanism, that the
right image is chosen as a thumbnail for that album, for example, in
``foo/index.md``::

  Title: Private section
  Thumbnail: public.jpg

Et voilà! You now have a hybrid private/public gallery. This is not
recommended for highly sensitive pictures; because other parts of
Sigal may (eventually?) leak information about filenames, thumbnails
or even contents without your knowledge in the future. But it's a good
simple way to add basic snooping protection over certain areas with
minimal configuration.

How to regenerate the gallery when something changes ?
------------------------------------------------------

It can be convenient to build continuously the gallery when adding or removing
pictures in the albums, however Sigal does not provide currently a buitin
"autoreload" feature. This can be achieved with external tool like `peat
<https://github.com/sjl/peat>`_::

    peat --dynamic 'find pictures/' 'sigal build'

will watch changes inside the ``pictures/`` directory and rebuild the gallery in
this case. Many other tools do similar things, here is the equivalent
command with `entr <http://entrproject.org/>`_::

    while true; do  find pictures/ | entr -d sigal build; done

How to automatically build the gallery on a remote git server?
--------------------------------------------------------------

Another way to handle this is by storing your files on a remote `git
<https://git-scm.com/>`_ repository, optionally with `git-annex
<https://git-annex.branchable.com/>`_ or `git-lfs
<https://git-lfs.github.com/>`_ to avoid managing large image files
directly with git.

Then Sigal can be triggered using `git hook
<https://git-scm.com/docs/githooks>`_ to update the repository on
push. The hook can be as simple as this::

  #!/bin/sh
  sigal build

But a `more robust implementation
<https://gitlab.com/anarcat/git-hooks/blob/master/sigal-git-hook>`_ is
also available. The hook should be installed in
``.git/hooks/post-receive``. If you are using git-annex, this hook
will already be present, so you'll need to add the sigal hook at the
end of the file, like so::

  #!/bin/sh
  # automatically configured by git-annex
  git annex post-receive

  /home/foo/src/git-hooks/sigal-git-hook

This assumes, of course, that you are running your own Git server;
this will not work with commercial providers like GitHub or GitLab
unless you setup a periodic job to automatically *pull* from those
server, in which case the above hook would be installed as an
``update`` hook.
