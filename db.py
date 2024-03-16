import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

engine = sql.create_engine(f'postgresql+psycopg2://postgres:{os.environ.get("DBPASS")}@{os.environ.get("DBIP")}/{os.environ.get("DBNAME")}')
Base = declarative_base()


class Categories(Base):
    __tablename__ = 'bsite_categories'
    cat_id = sql.Column(name='cat_id', type_=sql.Integer, primary_key=True)
    cat_name = sql.Column(name='cat_name', type_=sql.String)
    # cat_id = models.AutoField(primary_key=True)
    # cat_name = models.CharField(max_length=200, help_text='Добавь новую категорию')

    def __str__(self):
        return f'{self.cat_id},{self.cat_name}'


class Subcategories(Base):
    __tablename__ = 'bsite_subcategories'
    sub_id = sql.Column(name='sub_id', type_=sql.Integer, primary_key=True)
    sub_cat_id = sql.Column(name='sub_cat_id', type_=sql.Integer)
    sub_name = sql.Column(name='sub_name', type_=sql.String)

    def __str__(self):
        return f'{self.sub_id}, {self.sub_cat_id}, {self.sub_name}'


class Sub_Masters(Base):
    __tablename__ = 'bsite_masters_sub_master'
    id = sql.Column(name='id', type_=sql.Integer, primary_key=True)
    masters_id = sql.Column(name='masters_id', type_=sql.Integer, primary_key=True)
    subcategories_id = sql.Column(name='subcategories_id', type_=sql.Integer, primary_key=True)

    def __str__(self):
        return f'{self.id}, {self.master_id}, {self.subcategories_id}'


class Masters(Base):
    __tablename__ = 'bsite_masters'
    master_id = sql.Column(name='master_id',  type_=sql.Integer, primary_key=True)
#    sub_master = sql.Column(name='sub_master', type_=sql.Integer)
    name = sql.Column(name='name', type_=sql.String)
    info = sql.Column(name='info', type_=sql.String)
    phone = sql.Column(name='phone', type_=sql.String)
    address = sql.Column(name='address', type_=sql.String)
    tg = sql.Column(name='tg', type_=sql.String)
    wa = sql.Column(name='wa', type_=sql.String)
    ig = sql.Column(name='ig', type_=sql.String)
    vk = sql.Column(name='vk', type_=sql.String)
    password = sql.Column(name='password', type_=sql.String)
    username = sql.Column(name='username', type_=sql.String)
    visability = sql.Column(name='visability', type_=sql.String)
    need_moderation = sql.Column(name='need_moderation', type_=sql.Boolean)

    def __str__(self):
        return f'{self.master_id},  {self.name}, {self.phone}, {self.address}, {self.tg}, ' \
               f'{self.wa}, {self.ig}, {self.visability}'

    def tg_msg(self):
        msg = ''
        msg += f'{self.name}\n'
        if self.info is not None or self.info != '':
            msg += f'\n{self.info}\n'
        if self.address is not None or self.address != '':
            msg += f'Адрес: {self.address}\n'
        msg += '\nКонтакты\n\n'
        if self.tg is not None or self.tg != '':
            msg += f'Telegram: {self.tg}\n'

        if self.wa is not None or self.wa != '':
            msg += f'Whatsapp: {self.wa}\n'

        if self.vk is not None or self.vk != '':
            msg += f'VK: {self.vk}\n'

        if self.ig is not None or self.ig != '':
            msg += f'Instagram: {self.ig}\n'

        return msg


class Images(Base):
    __tablename__ = 'bsite_images'
    img_id = sql.Column(name='img_id',  type_=sql.Integer, primary_key=True)
    master_img_id = sql.Column(name='master_img_id',  type_=sql.Integer)
    img_url = sql.Column(name='img_url', type_=sql.String)
    file_id = sql.Column(name='file_id', type_=sql.String)
    telegram_file_id = sql.Column(name='telegram_file_id', type_=sql.String)
    description = sql.Column(name='description', type_=sql.String)

    def __str__(self):
        return f'{self.img_id}, {self.master_img}, {self.img_url}, {self.description}, {self.telegram_file_id}'


Session = sessionmaker(bind=engine)
session = Session()
