# Permanent Identifiers for the Web

This repository holds the website source code for <https://w3id.org/>.

[![Build Status](https://travis-ci.org/perma-id/w3id.org.svg)](https://travis-ci.org/perma-id/w3id.org)

#### Content

- [Purpose](#purpose)
- [Management](#management)
- [System Operations](#system-operations)
- [**Creating a New Identifier**](#new)
- [Naming Policy](#naming-policy)
- [W3ID Community](#w3id-community)
- [Disclaimer](#disclaimer)

### Purpose

The purpose of this website is to provide a secure, permanent
[URL](https://en.wikipedia.org/wiki/URL) re-direction service for Web
applications. This service is run by the
[W3C Permanent Identifier Community Group](https://www.w3.org/community/perma-id/).

Web applications that deal with
[Linked Data](https://en.wikipedia.org/wiki/Linked_data) often need to
specify and use URLs that are very stable. They utilize services such
as this one to ensure that applications using their URLs will always
be re-directed to a working website. This website operates like a
[switchboard](https://en.wikipedia.org/wiki/Telephone_switchboard),
connecting requests for information with the true location of the
information on the Web. The switchboard can be reconfigured to point
to a new location if the old location stops working.

### Management

There is a growing group of organizations in a consortium that have pledged
responsibility to ensure the operation of this website. These organizations
are:

- [Digital Bazaar](https://www.digitalbazaar.com/)
- [3 Round Stones](http://3roundstones.com/)
- [OpenLink Software](https://www.openlinksw.com/)
- [Applied Testing and Technology](https://www.aptest.com/)
- [Bosatsu Consulting](https://bosatsu.net/)
- [KurrawongAI](https://kurrawong.ai)

They are responsible for all
administrative tasks associated with operating the service. The social
contract between these organizations gives each of them full access to
all information required to maintain and operate the website. The
agreement is setup such that a number of these companies could fail,
lose interest, or become unavailable for long periods of time without
negatively affecting the operation of the site.

#### Joining the Management consortium

To join the management consortium, please make yourself known to the
W3ID community via participation in the mailing list (see the
[W3ID Community](#w3id-community) section below) and then, if you are
still keen to join, please submit an Issue to the
[GitHub Issue Tracker](https://github.com/perma-id/w3id.org/issues)
with the title _Seeking to join the W3ID Consortium_ and include
your details.

### System Operations

This website operates in HTTPS-only mode to ensure end-to-end security.
This means that it may be used for Linked Data applications that require
high levels of security such as those found in the financial, medical,
and public infrastructure sectors.

All identifiers associated with this website are intended to be around
for as long as the Web is around. This means decades, if not centuries.
If the final destination for popular identifiers used by this service
fail in such a way as to be a major inconvenience or danger to the Web,
the community will mirror the information for the popular identifier
and setup a working redirect to restore service to the rest of the Web.

<a id="new"></a>

## Creating a New Identifier

If you would like to add or update a permanent identifier of the form
`https://w3id.org/...`, the preferred procedure is to perform the
following steps:

1. _Fork_ [the _Repository_ for this system](https://github.com/perma-id/w3id.org)
   on GitHub.
2. Add or update a new redirect entry and commit your changes.
   1. If it does not yet exist, create a new directory with an intended permanent
      identifer name (see [Naming Policy](#naming-policy) below).
   2. If they do not yet exist, add `.htaccess` and `README.md` files to the directory.
      - `.htaccess` contains redirection rules, for computer to read and perform.
      - `README.md` contains more identifier info and contact info, for human to read.
      - See [w3id.org/examples](https://github.com/perma-id/w3id.org/tree/master/examples)
        for examples of `.htaccess` and `README.md`.
3. Submit a _Pull Request_ for your changes.

The maintainers of this system will then act on that _Pull Request_ and
merge it into this system's content. You will then be able to see your
changes in the repository and via resolution of the identifier you
created or edited.

If the terms _Fork_ and _Pull Request_ are new to you, you need to
familiarize yourself with the [Git](https://git-scm.com/) version
control system and [GitHub](https://github.com/), the platform used
to host this system. Please see this documentation:

- [Forking a Repository](https://docs.github.com/en/github-ae@latest/github/getting-started-with-github/fork-a-repo)
- [Creating a Pull Request across Forks](https://docs.github.com/en/github-ae@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)

#### Suitable PR content

Please help out the maintainers of the service with the following in your
Pull Requests:

- **Contact info** in a `README.md` or `.htaccess` comment.
- **Test your changes** with a local checkout of the site.
- **_Squash_ multiple commits** into one commit before a pull request
  if appropriate.
  - Here is information on _squashing_ commits:
    [How to Squash Commits in Git](https://www.git-tower.com/learn/git/faq/git-squash/)
- **Use descriptive commit messages**. In particular, include your project
  name in the commit message. For those using the GitHub interface, please
  modify the default "Create/Update/Delete `.htaccess`" message.

You can also send a request to add a redirect to the
[public-perma-id@w3.org](https://lists.w3.org/Archives/Public/public-perma-id/)
mailing list. Make sure to include the URL that you want on w3id.org, the
URL that you want to redirect to, and the HTTP code that you want to use
when redirecting. An administrator will then create the redirect for you.

### Naming Policy

There is no official policy on identifier names. The current practice
is to claim a top-level directory name and add project specific second
level identifiers. For instance, `https://w3id.org/PROJECT-ID/SUB-ID...`.
Shared top-levels are also available such as
`https://w3id.org/people/PERSON-ID`. There is no official list or policy
for reserved identifiers. However, the administrators may deny requests
for identifiers that are too generic, could cause confusion, are
inappropriate or offensive, or otherwise may be needed for future
service expansion.

### W3ID Community

If you wish to engage the community in discussion about this service for
your Web application, please send an e-mail to the
[public-perma-id@w3.org mailing list](https://lists.w3.org/Archives/Public/public-perma-id/).

---

### Disclaimer

The letters 'w3' in the domain name for this site stand for "World Wide
Web". Other than hosting the software for the Permanent Identifier
Community Group, the "World Wide Web Consortium" (W3C) is not involved
in the support or management of this website in any way.

---

## GC DFO Salmon (`/gcdfo/salmon/`) — What we need to configure

This section is project-specific to the GC DFO Salmon Ontology.

### Current status

- W3ID redirects are **configured and verified** (verified means the redirects return the expected HTTP 303 responses).
- No additional W3ID PRs are required per release unless the hosting base URL changes.

### Goal

- Make the “latest” ontology IRI resolve at `https://w3id.org/gcdfo/salmon`
- Make version IRIs resolve at `https://w3id.org/gcdfo/salmon/<version>`
- Add **content negotiation** (content negotiation means serving HTML vs RDF based on the HTTP `Accept` header) so tools can fetch Turtle / RDF/XML / JSON-LD directly from the ontology IRI.

### Where the redirects should point (current hosting)

- HTML docs (latest): `https://dfo-pacific-science.github.io/dfo-salmon-ontology/`
- Serializations (latest):
  - Turtle: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.ttl`
  - RDF/XML: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.owl`
  - JSON-LD: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.jsonld`
- Version snapshots (immutable, GitHub Pages):
  - HTML: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/releases/<version>/`
  - Turtle: `.../releases/<version>/gcdfo.ttl`
  - RDF/XML: `.../releases/<version>/gcdfo.owl`
  - JSON-LD: `.../releases/<version>/gcdfo.jsonld`

### What to edit in `perma-id/w3id.org`

- Update `gcdfo/salmon/.htaccess` with rewrite rules for:
  - default HTML redirect (303) for “latest”
  - content negotiation redirects (303) for Turtle / RDF/XML / JSON-LD
  - version-path redirects (303) for `/X.Y.Z` (SemVer)

### How to verify after merge/deploy

Run these from any machine:

- Latest (HTML):
  - `curl -I https://w3id.org/gcdfo/salmon`
- Latest (RDF via `Accept`):
  - `curl -I -H 'Accept: text/turtle' https://w3id.org/gcdfo/salmon/`
  - `curl -I -H 'Accept: application/rdf+xml' https://w3id.org/gcdfo/salmon/`
  - `curl -I -H 'Accept: application/ld+json' https://w3id.org/gcdfo/salmon/`
- Version path:
  - `curl -I https://w3id.org/gcdfo/salmon/0.0.999`
  - `curl -I -H 'Accept: text/turtle' https://w3id.org/gcdfo/salmon/0.0.999`

### When you do (and do not) need another W3ID PR

- **No new PR per release** as long as the redirect targets stay the same and you publish `docs/releases/X.Y.Z/` for each version.
- **Open a new PR** if the hosting base URL changes (for example, moving GitHub Pages to a new org or repo).

### Fork + PR workflow (what you actually need to do)

W3ID redirects are configured by Pull Request to the upstream repo:

1. Work in your fork (example fork): `https://github.com/dfo-pacific-science/w3id-GCDFOS`
2. Update these two files:
   - `gcdfo/salmon/.htaccess`
   - `gcdfo/salmon/readme.md`
3. Open a PR from your fork to: `https://github.com/perma-id/w3id.org` (target branch: `master`)
4. Wait for W3ID maintainers to merge + deploy, then run the curl checks above.

You generally only need to update the W3ID repo again if the hosting targets change (e.g., different GitHub Pages base URL) or if you add new representations.
