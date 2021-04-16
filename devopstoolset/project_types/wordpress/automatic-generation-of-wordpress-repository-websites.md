# Automatic generation of WordPress repository websites

WordPress automated demo site.<br><br>
![Logo](../../.media/WordPress-logotype-simplified-site-100px.png)

# Description

This site is generated automatically:
* WordPress core files
* wp-config.php settings
* Database creation and customization
* Theme
* Plugins

After the automatic generation you customize your child theme, add your plugins and set everything as you like. That is what you commit to your repository.

# Getting started

## Step by step

1. [Install PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell) if you don't have it on your machine (available for Windows, Linux, MacOS and ARM platforms).
2. Get the latest version of the file [Bootstrap-WordPressRepository.ps1](https://raw.githubusercontent.com/aheadlabs/devops-toolset/master/wordpress/Bootstrap-WordPressRepository.ps1) and place it on your repository root (empty directory).
3. If you have `*site-environments.json`, `*site.json` and `*project-structure.json` files you can copy them to the root of the repository as well. **This is optional**. You have sample files here: [environments](https://github.com/aheadlabs/devops-toolset/blob/master/wordpress/default-site-environments.json), [site](https://github.com/aheadlabs/devops-toolset/blob/master/wordpress/default-localhost-site.json) and [structure](https://github.com/aheadlabs/devops-toolset/blob/master/wordpress/default-wordpress-project-structure.json).
4. Place your theme and child-theme in the your repository root if it is in zip format (you will need a custom `site.json` file for that).
5. Call the `Bootstrap-WordPressRepository.ps1` script and follow the on-screen instructions.
6. Update `.gitignore` according to your needs.
7. Update `project.xml` to match your project values.
8. Update `README.md` files according to your needs.
