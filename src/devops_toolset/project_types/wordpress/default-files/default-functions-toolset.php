<?php
/**
 * @param $relativeFontPath string Font relative path
 * @return string Image URI
 */
function {{theme-name}}GetFontPath(string $relativeFontPath): string
{
    return get_stylesheet_directory_uri() . '/assets/font/' . $relativeFontPath;
}

/**
 * @param $relativeImagePath string Image relative path
 * @return string Image URI
 */
function {{theme-name}}GetImagePath(string $relativeImagePath): string
{
    return get_stylesheet_directory_uri() . '/assets/images/' . $relativeImagePath;
}
