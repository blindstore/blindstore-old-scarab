import argparse

from server import app


parser = argparse.ArgumentParser(description="Start a Blindstore server.")
parser.add_argument('-d', '--debug', action='store_true',
                    help="enable Flask debug mode. DO NOT use in production.")
args = parser.parse_args()


if __name__ == '__main__':
    app.run(debug=args.debug)
