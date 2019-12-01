from utils.parser import Parser


def main():
    with Parser('assets/4625792331945392032.html') as parser:
        parser.write_to_db()


if __name__ == '__main__':
    main()
