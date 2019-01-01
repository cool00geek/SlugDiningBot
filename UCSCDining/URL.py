from CollegeName import get_dining_hall, get_dining_num

stevenson_num = "05"
crown_num = "20"
porter_num = "25"
rcc_num = "30"
c9_num = "40"

stevenson_name = "Cowell+Stevenson"
crown_name = "Crown+Merrill"
porter_name = "Porter+Kresge"
rcc_name = "Rachel+Carson+Oakes"
c9_name = "+Colleges+Nine+%26+Ten+"


def get_url(college, date):
    month,date,year = date.split("/")
    url="https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate={month}%2F{day}%2F{year}&locationNum={num}&locationName=%20{name}+Dining+Hall&naFlag=1"
    # CO https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=1%2F7%2F2019&locationNum=05&locationName=%20Cowell+Stevenson+Dining+Hall&naFlag=1
    # CR https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=1%2F7%2F2019&locationNum=20&locationName=%20Crown+Merrill+Dining+Hall&naFlag=1
    # PO https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=1%2F7%2F2019&locationNum=25&locationName=%20Porter+Kresge+Dining+Hall&naFlag=1
    # RC https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=1%2F7%2F2019&locationNum=30&locationName=%20Rachel+Carson+Oakes+Dining+Hall&naFlag=1
    # C9 https://nutrition.sa.ucsc.edu/menuSamp.asp?myaction=read&sName=&dtdate=1%2F7%2F2019&locationNum=40&locationName=%20+Colleges+Nine+%26+Ten+Dining+Hall&naFlag=1
    return url.format(num=get_dining_num(college), name=get_dining_hall(college), month=str(int(month)), day=str(int(date)), year=year)
