<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<a name="readme-top"></a>

<div align="center">
  <h1 align="center">Vref Util</h3>

  <p align="center">
    Tools to work with vref files
    <br />
    <!-- <a href="https://github.com/jcuenod/vref_util"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jcuenod/vref_util">View Demo</a>
    · -->
    <a href="https://github.com/jcuenod/vref_util/issues">Report Bug</a>
    ·
    <a href="https://github.com/jcuenod/vref_util/issues">Request Feature</a>
    <!-- ·
    <a href="https://jcuenod.github.io/vref_util-examples/">Live Demo</a> -->
  </p>
</div>



<!-- GETTING STARTED -->
## Getting Started

### Installation

To install, use your favorite package manager and do the equivalent of:

```sh
pip install vref-util
```

<!-- USAGE EXAMPLES -->
### Usage

```python
from vref_util import Vref

niv = Vref("./en-NIV11.txt")

jhn3v16 = niv["JHN 3:16"][0]
print(jhn3v16)
# For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.
```

Note that `__get_item__` (the function called by `niv["JHN 3:16"]`) returns a `VerseList`. The `VerseList` class allows us to iterate through the verses using a generator, but we can also access elements using indices or slices. Here, we use `[0]` to get the first (and only) `Verse`.

```python
print(repr(jhn3v16))
# Verse(verse="JHN 3:16", text="For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.")
```

The `Verse` class supports the `__str__` and `__repr__` methods. So casting the first element to a string by printing it prints the text. You can also return the verse text using the `.text` attribute. Likewise, you can get the verse reference using the `.reference` attribute.

```python
print(jhn3v16.text)
# For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.

print(jhn3v16.reference)
# JHN 3:16
```

Printing the reference is not useful when there is only one verse, but you can select multiple verses using ranges like "JHN 3:16-JHN 3:17" or selections like "JHN 3:16,JHN 3:17" or a combination of both like "JHN 3:16,JHN 3:17-JHN 3:18".

```python
print(niv["JHN 3:16-JHN 3:17,JHN 3:18"])
# VerseList([
#   Verse(verse="JHN 3:16", text="For God so loved the world that he gave his one and only Son,..."),
#   Verse(verse="JHN 3:17", text="For God did not send his Son into the world to condemn the wo..."),
#   Verse(verse="JHN 3:18", text="Whoever believes in him is not condemned, but whoever does no...")
# ])
```

**Note:**

- Book names must be valid USFM book names.
- Chapter and verse numbers must be valid.
- Books and chapters must be specified in full for ranges/selections.
  - ❌ `JHN 1:1-2`
  - ❌ `JHN 1:1-1:2`
  - ✅ `JHN 1:1-JHN 1:2`

### Custom Versification Formats

By default, the `org` versification system is used (and packaged in `vref-util`). If you have vref files that use a different versification system, you can specify it when creating the `Vref` object.

```python
from vref_util import Vref

niv = Vref("./en-NIV11.txt", "custom_vref.txt")
# or, with named arguments:
niv = Vref("./en-MYBIBLE.txt", versification_vref_path="custom_vref.txt")
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/jcuenod/vref_util.svg?style=for-the-badge
[contributors-url]: https://github.com/jcuenod/vref_util/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jcuenod/vref_util.svg?style=for-the-badge
[forks-url]: https://github.com/jcuenod/vref_util/network/members
[stars-shield]: https://img.shields.io/github/stars/jcuenod/vref_util.svg?style=for-the-badge
[stars-url]: https://github.com/jcuenod/vref_util/stargazers
[issues-shield]: https://img.shields.io/github/issues/jcuenod/vref_util.svg?style=for-the-badge
[issues-url]: https://github.com/jcuenod/vref_util/issues
[license-shield]: https://img.shields.io/github/license/jcuenod/vref_util.svg?style=for-the-badge
[license-url]: https://github.com/jcuenod/vref_util/blob/master/LICENSE.txt