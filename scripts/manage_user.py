import argparse

from rasax.community import config
from rasax.community.database.utils import session_scope
from rasax.community.initialise import create_project_and_settings
from rasax.community.services.domain_service import DomainService
from rasax.community.services.role_service import RoleService
from rasax.community.services.settings_service import SettingsService
from rasax.community.services.user_service import (
    UserService,
    UserException,
    AuthMechanisms,
    RoleException,
    ADMIN,
    TESTER,
    ANNOTATOR,
)


def create_argparser():
    parser = argparse.ArgumentParser(
        description="Create a new user or change a user's password, "
        "list users or delete a user"
    )

    subparsers = parser.add_subparsers(dest="mode", description="create, delete, list")

    subparser_create(subparsers)
    subparser_delete(subparsers)
    subparser_list(subparsers)

    return parser


def subparser_create(subparsers):
    parser_create = subparsers.add_parser("create", description="create a new user")
    parser_create.add_argument("username", help="username")
    parser_create.add_argument("password", help="password")
    parser_create.add_argument(
        "role", choices=[ADMIN, ANNOTATOR, TESTER], help="account role"
    )
    parser_create.add_argument(
        "--update", action="store_true", help="update the password of an existing user"
    )


def subparser_delete(subparsers):
    parser_delete = subparsers.add_parser("delete", description="delete a user")
    parser_delete.add_argument("username", help="username")


def subparser_list(subparsers):
    subparsers.add_parser("list", description="list all users")


def initialise_services(_session):
    return (
        UserService(_session),
        SettingsService(_session),
        DomainService(_session),
        RoleService(_session),
    )


def change_password(userservice, username, password):
    try:
        userservice.admin_change_password(username, password)
    except UserException as e:
        print(
            "User {} does not exist. To create a new user please run "
            "`sudo python rasa_x_commands.py create {} "
            "<pw> admin`".format(e, e)
        )


def create_user(userservice, username, password, role, team):
    try:
        userservice.create_user(
            username, password, team, role, AuthMechanisms.username_password
        )
    except UserException as e:
        print(
            "User '{}' already exists. You can update the password by "
            "running `sudo python rasa_x_commands.py create --update "
            "{} admin <new_pw>`".format(e, e)
        )
    except RoleException as e:
        print("Role '{}' does not exist. Please select a valid role.".format(role))


def delete_user(userservice, username):
    try:
        userservice.delete_user(username)
    except UserException as e:
        print(
            "User {} does not exist. To create a new user please run "
            "`sudo python rasa_x_commands.py create --update admin {} "
            "<pw>`".format(e, e)
        )


def print_user_table(users, format_template):
    print(format_template.format("#", "username", "role", "created at"))
    print("-" * 42)

    for i, u in enumerate(users):
        _id = u.get("_id")
        if _id:
            created_at = _id.generation_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            created_at = "ObjectID not found"

        print(
            format_template.format(i + 1, u.get("username"), u.get("role"), created_at)
        )

    print("-" * 42)


def list_users(userservice, team_name):
    users = userservice.fetch_all_users(team_name)
    format_template = "{:<3}{:12}{:8}{:20}"
    print("Found {} user{}".format(len(users), "" if len(users) == 1 else "s"))

    if len(users):
        print_user_table(sorted(users), format_template)


if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()

    with session_scope() as session:

        user_service, settings_service, domain_service, role_service = initialise_services(
            session
        )

        team_name = config.team_name

        if args.mode == "create":
            create_project_and_settings(settings_service, role_service, team_name)

            if args.update:
                change_password(user_service, args.username, args.password)
            else:
                create_user(
                    user_service, args.username, args.password, args.role, team_name
                )
        elif args.mode == "delete":
            delete_user(user_service, args.username)
        elif args.mode == "list":
            list_users(user_service, team_name)