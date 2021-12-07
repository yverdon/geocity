## AtlasPrint: QGIS Server Plugin to export PDF from a QGIS Layout with atlas capabilities

### Description

This plugin adds a new service to QGIS 3 Server `ATLAS` which
allows to export a report or print layout with an atlas configured (by passing
an expression parameter to choose which feature is the current atlas feature).

![Logo of the plugin](icon.png)

### Versions

**Be careful**, if you use relation in your project and you use them in your layout, 
you should use 1.2.4 with QGIS < 3.10.1. A bug has been fixed in 3.10.2 about relation in a layout. 
Otherwise, you can use version 3 of the plugin.

### API

The layout must have an atlas enabled.

This plugin adds some new requests with the `ATLAS` service:
* `REQUEST=GETCAPABILITIES`: Return the plugin version
* `REQUEST=GETPRINT`
  * `TEMPLATE`: **required**, name of the layout to use.
  * `EXP_FILTER`: **required** for atlases, it must be HTML escaped.
    * For example, to request `fid=12`, it must be `&EXP_FILTER=fid%3D12`.
    * An expression returning many features can also be used, for instance `&EXP_FILTER=id in ('1','2')` will return a PDF with 2 pages.
  * `SCALE`: *optional*. If not provided, the default configuration in the atlas is used.
    * If set to an integer number, the scale will be fixed. Exclusive with `SCALES`.
  * `SCALES`: *optional*. If not provided, the default configuration in the atlas is used.
    * Comma separated list of values. If set, these predefined scales are used. Exclusive with `SCALE`.
    * For instance `SCALES=400,1000`.
  * `FORMAT`: PDF is by default.
    * Possible values from https://docs.qgis.org/latest/en/docs/server_manual/services.html#wms-getprint-format
    * SVG is not available.
  * Arbitrary key value pairs to manipulate item label text in composition. The key is the id (lower case) of the label text component and the value is the content that will override it default content. Example `&title=Municipality%20of%20Paris` will look for a label text item in the layout called `title` and will replace it with `Municipality of Paris`.

The only config that the plugin will not follow is the file pattern defined in QGIS Desktop, if it outputs many PDF.

This plugin also adds some new requests to the `WMS` service for backward compatibility:
* `REQUEST=GETCAPABILITIESATLAS` for `ATLAS` `GETCAPABILITIES`
* `REQUEST=GETPRINTATLAS` for `ATLAS` `GETPRINT`

### Installation with QGIS server

We assume you have a fully functional QGIS Server with Xvfb.
See [the QGIS3 documentation](https://docs.qgis.org/3.4/en/docs/user_manual/working_with_ogc/server/index.html).

We need to download the plugin, and tell QGIS Server where the plugins are
stored, then reload the web server.
For example on Debian:

```bash
# Create needed directory to store plugins
mkdir -p /srv/qgis/plugins

# Get last version
cd /srv/qgis/plugins
wget "https://github.com/3liz/qgis-atlasprint/archive/master.zip"
unzip master.zip
mv qgis-atlasprint-master/atlasprint atlasprint
rm -rf qgis-atlasprint-master master.zip
```

#### Configure plugin for QGIS server FCGI module:

If you are using Nginx, Apache or supervisor to run the QGIS FCGI module you will need
to define the `QGIS_PLUGINPATH` environment variable.

Example with Apache:

```bash
# Make sure correct environment variables are set in your web server configuration
# for example in Apache2 with mod_fcgid
nano /etc/apache2/mods-available/fcgid.conf
FcgidInitialEnv QGIS_PLUGINPATH "/srv/qgis/plugins/"

# Reload server, for example with Apache2
service apache2 reload
```

#### Configure the plugin path in [py-qgis-server](https://github.com/3liz/py-qgis-server)

You must define the `QGSRV_SERVER_PLUGINPATH` environment variable with Docker or the `pluginpath` setting
in the `server` section of the configuration file.
For more informations, see the [py-qgis-server](https://github.com/3liz/py-qgis-server/blob/master/README.md) documentation.
