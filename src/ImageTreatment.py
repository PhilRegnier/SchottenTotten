# Image pretreatment

from PIL import ImageDraw, Image, ImageQt

from src.Style import MainGeometry, GlobalStyle


class ImageTreatment:

    # rounding corners
    @staticmethod
    def round_corners(image, r):
        w, h = image.size
        circle = Image.new('L', (r * 2, r * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, r * 2, r * 2), fill=255)
        alpha = Image.new('L', image.size, 255)
        alpha.paste(circle.crop((0, 0, r, r)), (0, 0))
        alpha.paste(circle.crop((0, r, r, r * 2)), (0, h - r))
        alpha.paste(circle.crop((r, 0, r * 2, r)), (w - r, 0))
        alpha.paste(circle.crop((r, r, r * 2, r * 2)), (w - r, h - r))
        image.putalpha(alpha)
        return image

    # frame & thickness
    @staticmethod
    def enluminure(im, r=MainGeometry.r_bound, t=1, ow=1, oh=1):
        im = ImageTreatment.round_corners(im, int(r))

        cadre = Image.new('RGBA', (im.width + 2 * t, im.height + 2 * t), GlobalStyle.cadre_color)
        cadre = ImageTreatment.round_corners(cadre, int(r + t))
        cadre.paste(im, (t, t), im)

        trame = Image.new('RGBA', (cadre.width + ow, cadre.height + oh), (0, 0, 0, 0))
        relief = Image.new('RGBA', (cadre.width, cadre.height), GlobalStyle.relief_color)
        relief = ImageTreatment.round_corners(relief, int(r + t))
        trame.paste(relief, (ow, oh), relief)
        trame.paste(cadre, (0, 0), cadre)
        image = ImageQt.ImageQt(trame)

        return image
