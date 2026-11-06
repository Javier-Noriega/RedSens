from SistemaRedSens.sistema_redsens import SistemaRedSens
from Menu.menu import Menu


def main():

    sistema = SistemaRedSens()

    menu = Menu(sistema)

    menu.mostrar()


if __name__ == "__main__":
    main()