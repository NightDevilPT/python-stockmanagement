from tkinter import messagebox
from PIL import Image,ImageTk,ImageDraw,ImageFont


def Call_ID_Template1(data=None):
    size = (200,200)
    ID = Image.open("ID Templates/ID1.png").convert("RGBA")
    Draw = ImageDraw.Draw(ID)

    mask = Image.open("ID Templates/mask.png").convert("L").resize(size)
    img2 = Image.new("RGBA",size)

    employe = data[4].convert("RGBA").resize(size)

    im = Image.composite(employe,img2,mask)

    logo = Image.open("icons/logo.png").resize((100,100))
    ID.paste(logo,(880,30),logo)
    ID.paste(logo,(30,30),logo)

    BF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=70)
    SF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=40)
    VSF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=32)
    VVSF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=18)

    Draw.text((180,20),text="NightDevil PT Store",font=BF,fill="white",stroke_fill="black",stroke_width=3)
    Draw.text((250,100),text="Sonia Vihar, Delhi - 110094",font=SF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.ellipse((50,220,260,430),fill="white")
    ID.paste(im,(55,225),im)

    Draw.text((350,200),text="Name ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((520,200),text=f"-  {data[0]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,280),text="Gender ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((520,280),text=f"-  {data[1]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,360),text="Phone No ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((520,360),text=f"-  {data[2]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,440),text="Email-ID ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((520,440),text=f"-  {data[3]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((40,590),text=f"NightDevil PT Store, Sonia-Vihar Delhi-110094, Contact-No : 9999999999, Email-ID : nightdevilpt@gmail.com",font=VVSF,fill="white",stroke_fill="black",stroke_width=1)
    
    return ID


def Call_ID_Template2(data=None):
    size = (220,220)
    ID = Image.open("ID Templates/ID2.png").convert("RGBA")
    Draw = ImageDraw.Draw(ID)

    mask = Image.open("ID Templates/mask.png").convert("L").resize(size)
    img2 = Image.new("RGBA",size)

    employe = data[4].convert("RGBA").resize(size)
    # employe = Image.open("icons/logo.png").convert("RGBA").resize(size)

    im = Image.composite(employe,img2,mask)

    logo = Image.open("icons/logo.png").resize((100,100))
    ID.paste(logo,(880,30),logo)
    ID.paste(logo,(30,30),logo)

    BF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=70)
    SF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=40)
    VSF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=32)
    VVSF = ImageFont.truetype("/usr/share/fonts/ARIALBD.TTF",size=18)

    Draw.text((180,20),text="NightDevil PT Store",font=BF,fill="white",stroke_fill="black",stroke_width=3)
    Draw.text((250,100),text="Sonia Vihar, Delhi - 110094",font=SF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.ellipse((50,210,280,440),fill="white")
    ID.paste(im,(55,215),im)

    Draw.text((350,200),text="Name ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((500,200),text=f"-  {data[0]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,280),text="Gender ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((500,280),text=f"-  {data[1]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,360),text="Phone No ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((500,360),text=f"-  {data[2]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((350,440),text="Email-ID ",font=VSF,fill="white",stroke_fill="black",stroke_width=2)
    Draw.text((500,440),text=f"-  {data[3]}",font=VSF,fill="white",stroke_fill="black",stroke_width=2)

    Draw.text((40,590),text=f"NightDevil PT Store, Sonia-Vihar Delhi-110094, Contact-No : 9999999999, Email-ID : nightdevilpt@gmail.com",font=VVSF,fill="white",stroke_fill="black",stroke_width=1)
    
    return ID

