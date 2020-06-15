""" Sets all configuration parameters in pristine WordPress core files
Args:
    root-path: Path to the WordPress installation.
    environment-path: Path to the environment JSON file.
    environment-name: Environment name.
    db-user_password: Database user password

"""
import argparse
import tools
import wordpress.wptools as wp_tools


def main(root_path: str, environment: (str, str), db_user_pwd: str):
    """ Sets all configuration parameters in pristine WordPress core files
    Args:
        root-path: Path to the WordPress installation.
        environment: Tuple
        db-user_password: Database user password

    """
    # Add constants
    wp_constants = wp_tools.get_constants(root_path)
    # Parse site configuration
    site_config = wp_tools.get_site_configuration_path_from_environment(environment[0], environment[1])
    # Create wp-config.php file

    # Set config values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("environment-path", action=tools.argument_validators.PathValidator)
    parser.add_argument("environment-name")
    parser.add_argument("db-user-pwd")
    args, args_unknown = parser.parse_known_args()

    tools.cli.print_title(literals.get("wp_title_wordpress_files"))
    environment = {args.environment_name, args.environment_path}
    main(args.root_path, environment, args.db_user_pwd)
