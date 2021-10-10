import pymysql
from PIL import Image, ImageFont, ImageDraw
from pypika import Table, Query
from flask import Flask, request, abort

app = Flask(__name__)

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

def addText2Image():
    dbSetting = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "17385",
        "db": "meme_project",
        "charset": "utf8"
    }
    try:
        conn = pymysql.connect(**dbSetting)
        with conn.cursor() as cursor:
            sql = "SELECT CONCAT(path, filename) file, number_of_blocks FROM meme WHERE id = 1"
            cursor.execute(sql)
            memeFile = cursor.fetchone()
            fileName = memeFile[0]
            numOfBlocks = memeFile[1]

            sql = "SELECT sequence, x_offset, y_offset FROM block_attributes WHERE block_attributes.meme_id = 1"
            cursor.execute(sql)
            memeData = cursor.fetchall()
            print(memeData)

            myMeme = Image.open(fileName)
            imageEditable = ImageDraw.Draw(myMeme)
            font = ImageFont.truetype('./font/font.otf', 30)
            textContent = (
                '四月的比特幣',
                '反抗奴役自由貨幣精神的銀行體系推翻資本主義的高牆',
                '五月的比特幣',
                '嗚嗚哪裏的公園還有位置'
            )
            for i in range(numOfBlocks):
                contentList = wrap(textContent[i], 15)
                print(contentList)
                for index, line in enumerate(contentList):
                    fontCoord = (memeData[i][1], memeData[i][2] + 50 * index)
                    imageEditable.text(
                        fontCoord,
                        line,
                        fill=(0, 0, 0),
                        font=font
                    )
            myMeme.save("./test.png")
            
    except Exception as ex:
        print(ex)
        return 400

    return 200

if __name__ == "__main__":
    app.run()
