import ssl
import click


@click.command()
@click.argument("host", type=click.STRING, default="u.y.qq.com")
@click.option("--port", type=int, default=443)
def get_server_certificate(host, port):
    print(ssl.get_server_certificate((host, port)))



if __name__ == "__main__":
    get_server_certificate()
