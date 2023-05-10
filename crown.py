KILOES_IN_IMPERIAL_STONE = 6.35
CROWN_WEIGHT_IN_KG = 2.23


def main():
    crown_weight_in_stones = convert_kiloes_to_stones(CROWN_WEIGHT_IN_KG)

    print(f"The crown weighs {crown_weight_in_stones} stones.")


def convert_kiloes_to_stones(kiloes):
    return kiloes / KILOES_IN_IMPERIAL_STONE


if __name__ == '__main__':
    main()
