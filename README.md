# hide-layer-svg
A python script that reads a SVG file and creates based on specific attributes in the layers new files where the layers are or aren't shown. This might come in handy if you need different versions of your svg based on different layer visibilities.

## Getting Started
### Prerequisites

You need either python 2.7 or python 3.7 installed on your local machine; and also [Inkscape](https://inkscape.org/). Other than that you are good to go.

### Preparing your Inkscape svg

Add a custom node at layer level in the xml file of your inkscape file. For Example, in [https://github.com/ExtremOPS/hide-layer-svg/blob/ff216f32ccc3ac9b415244a6b0cb4ed2f06ae020/Test.svg#L87](https://github.com/ExtremOPS/hide-layer-svg/blob/ff216f32ccc3ac9b415244a6b0cb4ed2f06ae020/Test.svg#L87) I added the node with the identifiername `exercise` of the value `a,b-c,d-e` since I am using this feature mainly for creating exercises for students.

But no worries, you can choose whatever name you want for the custom node. It ist just important, that you seprated your values with a `,` since this is the default delimiter. But it can, as the name for the node, be changed.

If layers do not have this customnode, they will always be shown. If you want to have a layer just in your "Master" svg and nowhere else, put in the custom node the value `never` or `Never`.

### Example Usage

If a file has no instance of the custom node in all layers no operation will executed.
```
python hideAndShowLayers.py --help
```
displays the possible options you can set.
```
python hideAndShowLayers.py
```
runs the script in the current folder. It will search for `*.svg` files and then for their layers. The default node identifier at layer lever is `exercise`. If in the whole file no such node exist the program will skip the current `svg` file. As soon as there is one instance it will create new `svgs` with a `$combination_modLayer` suffix, where `$combination` represents the current combination of showing and hiding layers.

If you rerun the script, it will omit all files that contain `*modLayer*` in order to prevent creating too many files.

```
python hideAndShowLayers.py -a website -d ; -s modifiedLayer -o ./Output -f ./RawSVG
```
will run the script with all possible optinal arguments. It does the same as before but now the custom node identifier has the name `website`, the new delimter for the different versions is `;`, the suffix that will be added is `$combination_modifiedLayer`, all outputfiles will be saved in the folder `./Output`, and the programs searches for files in `./RawSVG`.

## Additional notes
This program was tested with `Python 2.7.15`, `Python 3.7.1` and `Inkscape 0.92.3`.

## Built With

* [xml.etree.ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) - The ElementTree XML API
* [argparse](https://docs.python.org/2.7/library/argparse.html) - Parser for command-line options, arguments and sub-commands

## Licensing

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
