<?php
/**
 * Register CSS
 * More info: https://developer.wordpress.org/themes/advanced-topics/child-themes/#3-enqueue-stylesheet
 */
function {{theme-name}}RegisterStyles()
{
    // TODO Enqueue your styles here. Note that W74 framework is enqueuing theme styles so you don't need to do it here.
}
add_action('wp_enqueue_scripts', '{{theme-name}}RegisterStyles');

/**
 * Register scripts
 */
function {{theme-name}}RegisterScripts()
{
    wp_enqueue_script(
        'template-scripts',
        get_stylesheet_directory_uri() . '/assets/js/main.js',
        array(),
        wp_get_theme()->get('Version'),
        true
    );
}
add_action('wp_enqueue_scripts', '{{theme-name}}RegisterScripts');

/*
 * Hide admin bar
 * If you want your admin bar to be showed remove this line of code
 */
add_filter('show_admin_bar', '__return_false');


// NOTE You can add other *.php files in this directory that contain functions. All of them will be parsed as one
// functions.php file, one after another.
