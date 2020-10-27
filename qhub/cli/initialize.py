import yaml

from qhub.initialize import render_config


def create_init_subcommand(subparser):
    subparser = subparser.add_parser("init")
    subparser.add_argument(
        "platform", help="Cloud to deploy qhub on",
        type=str, choices=['do', 'gcp', 'aws'],
    )
    subparser.add_argument(
        '--project', help='Namespace to assign to qhub resources'
    )
    subparser.add_argument(
        '--domain', help='Domain for jupyterhub clister to be deployed under'
    )
    subparser.add_argument(
        '--ci-provider', choices=['github-actions'],
        help='continuous integration to use for infrastructure as code'
    )
    subparser.add_argument(
        '--oauth-provider', choices=['github', 'auth0'],
        default='github',
        help='oauth provider to use for authentication'
    )
    subparser.add_argument(
        '--oauth-auto-provision', action='store_true',
        help='Attempt to automatically provision oauth. For Auth0 is requires environment variables AUTH0_DOMAIN, AUTH0_CLIENTID, AUTH0_CLIENT_SECRET',
    )
    subparser.set_defaults(func=handle_init)


def handle_init(args):
    config = render_config(
        project_name=args.project,
        qhub_domain=args.domain,
        cloud_provider=args.platform,
        ci_provider=args.ci_provider,
        oauth_provider=args.oauth_provider,
        oauth_auto_provision=args.oauth_auto_provision)

    with open('qhub-config.yaml', 'x') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
