## Icons

Icons are used by plugins to visually identify the plugin in the web interface.

### Generation

Plugins icons are created by Gwen, our designer.
Send a request to @gwen in Slack for an icon with some details:

* If the plugin is for an online service, provide a link to the website
* If the plugin is for a *nix command or protocol, let her know that.
* If you have any ideas for what it should look like suggest that

### Configuring

Once an icon is available, complete the following steps.

1. Place the icon in your plugins directory e.g. `plugins/myplugin` with the filename `icon.png`
2. Run `make icon`
3. Add the updated spec file and the icon to the repository

Full example,
```
cd plugins/myplugin
mv ~/Downloads/plugin-myplugin.png icon.png
make icon
git add icon.png plugin.spec.yaml
git commit -m "add icon"
git push origin myplugin
```
