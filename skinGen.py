from PIL import Image

def genSkins():
    main_image = Image.open("image.png")

    if main_image._size != (72,24):
        print("Image must be 72x24 pixels!")
        exit()

    output = []

    #the following is 

    #third row of skins
    output.append(main_image.crop((64,16,72,24)))
    output.append(main_image.crop((56,16,64,24)))
    output.append(main_image.crop((48,16,56,24)))
    output.append(main_image.crop((40,16,48,24)))
    output.append(main_image.crop((32,16,40,24)))
    output.append(main_image.crop((24,16,32,24)))
    output.append(main_image.crop((16,16,24,24)))
    output.append(main_image.crop((8,16,16,24)))
    output.append(main_image.crop((0,16,8,24)))

    #second row of skins
    output.append(main_image.crop((64,8,72,16)))
    output.append(main_image.crop((56,8,64,16)))
    output.append(main_image.crop((48,8,56,16)))
    output.append(main_image.crop((40,8,48,16)))
    output.append(main_image.crop((32,8,40,16)))
    output.append(main_image.crop((24,8,32,16)))
    output.append(main_image.crop((16,8,24,16)))
    output.append(main_image.crop((8,8,16,16)))
    output.append(main_image.crop((0,8,8,16)))

    #first row of skins
    output.append(main_image.crop((64,0,72,8)))
    output.append(main_image.crop((56,0,64,8)))
    output.append(main_image.crop((48,0,56,8)))
    output.append(main_image.crop((40,0,48,8)))
    output.append(main_image.crop((32,0,40,8)))
    output.append(main_image.crop((24,0,32,8)))
    output.append(main_image.crop((16,0,24,8)))
    output.append(main_image.crop((8,0,16,8)))
    output.append(main_image.crop((0,0,8,8)))

    num = 1
    for splice in output:
        base_skin = Image.open("base.png")
        base_skin.paste(splice,(8,8,16,16))
        base_skin.save(f"output/{num}.png")
        num += 1

genSkins()