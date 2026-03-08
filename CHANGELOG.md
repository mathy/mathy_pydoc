# CHANGELOG


## v0.7.31 (2026-03-08)

### Chores

- Drop launch file
  ([`38f47be`](https://github.com/mathy/mathy_pydoc/commit/38f47be2b0c58edf6ed829a7ba829dcc8ca7153d))

### Documentation

- Readme cleanup
  ([`426bfee`](https://github.com/mathy/mathy_pydoc/commit/426bfee0a7b92f42c4769acf7a8eb8f26f1e3edc))

### Features

- Support python 3.13 and modernize with pyproject.toml
  ([`62c118f`](https://github.com/mathy/mathy_pydoc/commit/62c118fadec66159038a5b21c89bab8250dcdcc8))

- also replace NodeJS with python-semantic-release

### Refactoring

- **project**: Use python semantic release and pyproject.toml
  ([`9e21a8d`](https://github.com/mathy/mathy_pydoc/commit/9e21a8d11d60104832703efbfc5b816e443d2ddc))


## v0.7.30 (2023-12-14)

### Features

- **pypi**: Loosen typer range
  ([`6f5ad4d`](https://github.com/mathy/mathy_pydoc/commit/6f5ad4d9b9690a32963220dfe9c67edfe3bdd85a))


## v0.7.29 (2023-12-14)

### Chores

- **ci**: Add weekly cron job build
  ([`1dee771`](https://github.com/mathy/mathy_pydoc/commit/1dee771bc3a639d6f918dd24500cd8a12a91b80a))

### Features

- **cli**: Add "plain" flag
  ([`263d378`](https://github.com/mathy/mathy_pydoc/commit/263d378bf41915e64f413b8f8c2f13cdd40c0b24))

- removes (doc) from docblock and <kbd> tag


## v0.7.28 (2023-01-05)

### Chores

- Use ubuntu 20.04 for build
  ([`8170288`](https://github.com/mathy/mathy_pydoc/commit/8170288ae11b5265e090440886690db31dd6525d))

### Features

- **requirements**: Loosen typer requirement
  ([`6ca0c33`](https://github.com/mathy/mathy_pydoc/commit/6ca0c33661692f767ab5e867e738c08c4b51b717))


## v0.7.27 (2022-05-16)

### Features

- Make typer range larger
  ([`fd59273`](https://github.com/mathy/mathy_pydoc/commit/fd592737d9c68d6fc5a6650d573367e023dd4ae9))


## v0.7.26 (2022-05-16)

### Bug Fixes

- Deploy updated package on merge
  ([`8ff1f84`](https://github.com/mathy/mathy_pydoc/commit/8ff1f8463eafe6d1effe5e4a06507678e15b4627))

- semantic release commit doesn't trigger a github action run


## v0.7.25 (2022-05-16)

### Features

- Ridiculous change
  ([`9e92b12`](https://github.com/mathy/mathy_pydoc/commit/9e92b1291467ca2ba3a65f8b8434088505826d0b))

what the heck, deploy runs with the old version.

I don't want to fix it rn 😭


## v0.7.24 (2022-05-16)

### Features

- Update typer to 0.4.x
  ([`65e1ce3`](https://github.com/mathy/mathy_pydoc/commit/65e1ce3dad1ebad9478f80d74892f6dd4638756c))


## v0.7.23 (2022-05-16)

### Chores

- Add install deps to deploy script
  ([`5f59128`](https://github.com/mathy/mathy_pydoc/commit/5f59128cf4feb4e973229e1cd11e60139064d681))

- Fix test script
  ([`2ec5477`](https://github.com/mathy/mathy_pydoc/commit/2ec547753d59eb463694e3b2af413028e224868c))

- Fix typo
  ([`a3c4b3a`](https://github.com/mathy/mathy_pydoc/commit/a3c4b3aaafc738f17e331554736b43a42bd56089))

- Remove travis script
  ([`6e34e86`](https://github.com/mathy/mathy_pydoc/commit/6e34e8602e36a42d1e90fc9040c07bf43dc5f96e))

### Features

- Add github actions for CI build
  ([`e41a309`](https://github.com/mathy/mathy_pydoc/commit/e41a309a9e3f2e297d0d9f47c8b415e8e8c30573))

- drop travis ci script


## v0.7.22 (2020-11-22)

### Features

- Mark python doc pseudo-code blocks with a tag
  ([`1562fa8`](https://github.com/mathy/mathy_pydoc/commit/1562fa890911ec20590391804dd28b4fbb85f0bb))

- if you're looking at ```python blocks in a file, it can be easy to end up thinking these doc blocs
  represent runnable code, when in fact they're just pseudocode that looks nice with syntax
  highlighting.


## v0.7.21 (2020-08-23)

### Features

- Add function types to api docs
  ([`75bc770`](https://github.com/mathy/mathy_pydoc/commit/75bc770188e0db6e3fe07d913c3ae3a08b243940))

- refactor app to use typer for command-line - drop some restructured text code - move license into
  License file and out of each individual source file


## v0.7.20 (2020-08-21)

### Bug Fixes

- **markdown**: Issue where return types were not cleaned up on short functions
  ([`b0e9f0f`](https://github.com/mathy/mathy_pydoc/commit/b0e9f0f08356ac983d0a280cefc4f740717d65ba))

- the logic for printing the cleaned up return type was bypassed by the length check immediate
  return


## v0.7.19 (2020-08-21)

### Bug Fixes

- **markdown**: Support ForwardRef stripping
  ([`a4f44a8`](https://github.com/mathy/mathy_pydoc/commit/a4f44a8db8ccf9223f5845758b5c02449eb3f63a))

- it used to be that _ForwardRef was output, but now (version change on my part maybe?) I see
  ForwardRef without the underscore. Adjust the regex to support both flavors.


## v0.7.18 (2020-07-19)

### Bug Fixes

- **ci**: Bump version after pypi step
  ([`69bfd5f`](https://github.com/mathy/mathy_pydoc/commit/69bfd5f164cf633df6a3466c656014c96a314a5a))

- **ci**: Do version increment during deploy step
  ([`be7be55`](https://github.com/mathy/mathy_pydoc/commit/be7be55bd3eab4dad6cea34d8e333f58bec21d62))


## v0.7.17 (2020-07-19)

### Bug Fixes

- **ci**: Remove json file version incrementing
  ([`4f78333`](https://github.com/mathy/mathy_pydoc/commit/4f7833385e942f4f12da43d4dd1f8a8673395b89))


## v0.7.16 (2020-07-19)


## v0.7.15 (2020-07-19)

### Bug Fixes

- **ci**: Wrong repo was used in set-build-version
  ([`608869b`](https://github.com/mathy/mathy_pydoc/commit/608869b0880bedd3a36bfe62b353a69552338d2f))

### Chores

- Add missing build script
  ([`3effbfb`](https://github.com/mathy/mathy_pydoc/commit/3effbfb98e9dab8193235db58d4f737cc942fa19))

- Fix travis script
  ([`a85dd44`](https://github.com/mathy/mathy_pydoc/commit/a85dd44d33d2b29121ae42928497c852ba406888))

- Invoke semantic-release in deploy script
  ([`7a679a5`](https://github.com/mathy/mathy_pydoc/commit/7a679a554a3f5e43408e02ae6b16d62c4f7d6f41))

- Try using python 3 generic
  ([`f698a09`](https://github.com/mathy/mathy_pydoc/commit/f698a0988517c1082e96f9cc0666cae1285d55c6))

- Update package.json version
  ([`bbd3e52`](https://github.com/mathy/mathy_pydoc/commit/bbd3e523b59887d3bd68437a940813a779f2fd08))

- and push tag

### Features

- **mathy_pydoc**: Import from https://github.com/justindujardin/mathy
  ([`2f384a0`](https://github.com/mathy/mathy_pydoc/commit/2f384a098cbded2a0c027d2422464b25c93f3127))


## v0.7.14 (2020-07-18)

### Chores

- Cleanup and remove cruft
  ([`134de1b`](https://github.com/mathy/mathy_pydoc/commit/134de1bd46d9640cd039bf2cebc08bd6d03e0a32))

- Initial commit
  ([`c0454b9`](https://github.com/mathy/mathy_pydoc/commit/c0454b9834202fb98a376aec48c1377cf99d61a2))

- imported from mathy monorepo
