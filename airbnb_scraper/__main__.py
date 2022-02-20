from property.property import Property


def main():
    properties = [Property(
        "https://www.airbnb.co.uk/rooms/33090114"), Property("https://www.airbnb.co.uk/rooms/50633275")
    ]

    for property in properties:
        print(property)


if __name__ == "__main__":
    main()
