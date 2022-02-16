from property import Property


def main():
    properties = [Property(
        "https://www.airbnb.co.uk/rooms/52395793")
    ]

    for property in properties:
        property.print_property()


if __name__ == "__main__":
    main()
